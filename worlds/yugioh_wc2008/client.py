import asyncio
import logging
import os
import re
from dataclasses import dataclass
from typing import Optional, Set, Iterable, Tuple, Mapping, Dict, List

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

logger = logging.getLogger("Client")

from .addresses import DUELIST_FLAGS
from .addresses import EMBUST_GATE_FLAGS, SAVAN_GATE_FLAGS, GIGORI_GATE_FLAGS, SEFOLILE_CLEAR_FLAG
from .locations import LOCATION_NAME_TO_ID

# Memory / connector domains
ROM_DOMAIN = "ROM"
RAM_DOMAIN = "Main RAM"
BUS_DOMAIN = "ARM9 System Bus"

# ROM header expected bytes used for validation. some players load the
# unpatched "wc2008.nds" while others apply the patch beforehand.  to avoid
# confusing errors we accept both the original and patched headers here.
EXPECTED_ROM_HEADER = (
    b"YU-GI-OH!WC8YG8P",  # original dump
    b"YGO WC2008C8YG8P",  # patched header inserted by our seed patcher
)
ROM_HEADER_ADDR = 0x000000
ROM_HEADER_LEN = 16  # header is always 16 bytes long, tuple length is irrelevant

# Player name
PLAYER_NAME_ADDR = 0x114000
PLAYER_NAME_LEN = 16

# AP struct pointer location (common pattern used by AP clients)
AP_STRUCT_PTR_ADDRESS = 0x023DFFFC
AP_MAGIC_REPEATS = 3  # how many times the magic is repeated in memory

# AP version table (expand if you support multiple generator versions)
@dataclass(frozen=True)
class VersionData:
    savedata_ptr_offset: int
    recv_item_id_offset: int
    recv_item_count_offset_in_ap_save: int
    ap_save_offset: int
    vars_flags_offset_in_save: int
    vars_flags_size: int
    vars_offset_in_vars_flags: int
    flags_offset_in_vars_flags: int
    once_loc_flags_offset_in_ap_save: int
    once_loc_flags_count: int
    champion_flag: int

AP_VERSION_DATA: Mapping[int, VersionData] = {
    0: VersionData(
        savedata_ptr_offset=16,
        recv_item_id_offset=20,
        recv_item_count_offset_in_ap_save=0,
        ap_save_offset=0xCF60,
        vars_flags_offset_in_save=0xDC0,
        vars_flags_size=0x3E0,
        vars_offset_in_vars_flags=0,
        flags_offset_in_vars_flags=0x240,
        once_loc_flags_offset_in_ap_save=10,
        once_loc_flags_count=16,
        champion_flag=2404,
    ),
}

# Duel Points address
DP_ADDRESS = 0x114310

logger = logging.getLogger("YugiohWC2008Client")


@dataclass(frozen=True)
class VarsFlags:
    flags: bytes
    vars: bytes
    once_loc_flags: bytes

    def get_flag(self, flag_id: int) -> bool:
        idx = flag_id // 8
        if idx < len(self.flags):
            return (self.flags[idx] & (1 << (flag_id & 7))) != 0
        return False

    def get_once_flag(self, flag_id: int) -> bool:
        idx = flag_id // 8
        if idx < len(self.once_loc_flags):
            return (self.once_loc_flags[idx] & (1 << (flag_id & 7))) != 0
        return False

    def get_var(self, var_id: int) -> Optional[int]:
        # AP vars often start at 0x4000; adapt if your layout differs
        idx = var_id - 0x4000
        if idx >= 0 and 2 * (idx + 1) <= len(self.vars):
            return int.from_bytes(self.vars[2 * idx:2 * (idx + 1)], "little")
        return None


class YugiohWC2008Client(BizHawkClient):
    game = "Yu-Gi-Oh! World Championship 2008"
    system = "NDS"
    patch_suffix = ".apwc8"
    ram_mem_domain = RAM_DOMAIN

    def __init__(self) -> None:
        super().__init__()
        self.rom_slot_name: Optional[str] = None
        self.player_name: Optional[str] = None
        self.seed_verify: bool = False
        self.checked_locations: Set[int] = set()
        self.goal_complete: bool = False

        # AP struct discovery state
        self.ap_struct_address: int = 0
        self.rom_version: int = 0
        
        # Frame counter for throttling duelist flag reads
        self.frame_count: int = 0
        
        # Track how many items we've injected
        self.items_received_count: int = 0
        
        # Track previous flag states to detect changes (not just current state)
        self.previous_flags: Dict[str, int] = {}
        self.full_duelist_read_supported: Optional[bool] = None
        
        # Track previous gate guardian counts
        self.prev_embust_count: int = -1
        self.prev_savan_count: int = -1
        self.prev_gigori_count: int = -1
        self.prev_sefolile: int = -1
        
        # Split duelist flags into chunks for batch reading
        self.duelist_flag_chunks: list = []
        self._init_duelist_chunks()
        
        # Wait for emulator to initialize before reading memory
        self.startup_frames: int = 0

    def _init_duelist_chunks(self):
        """Split duelist flags into manageable chunks to avoid BizHawk connector timeouts."""
        chunk_size = 15  # Read 15 duelist flags per frame to avoid overwhelming BizHawk
        duelist_list = list(DUELIST_FLAGS.items())
        self.duelist_flag_chunks = [
            duelist_list[i:i + chunk_size] 
            for i in range(0, len(duelist_list), chunk_size)
        ]
        logger.info("Split %d duelist flags into %d chunks of ~%d each", 
                    len(duelist_list), len(self.duelist_flag_chunks), chunk_size)

    @staticmethod
    def _normalize_duelist_flag(flag_addr: int | tuple[int, int]) -> tuple[int, int | None]:
        """Return (address, bit_index_or_none) for duelist flag definitions."""
        if isinstance(flag_addr, tuple):
            return flag_addr[0], flag_addr[1]
        return flag_addr, None

    @staticmethod
    def _is_duelist_cleared(flag_byte: int, bit_index: int | None) -> bool:
        """Evaluate whether a duelist flag is set."""
        if bit_index is None:
            return flag_byte != 0
        return (flag_byte & (1 << bit_index)) != 0

    # -------------------------
    # Helpers
    # -------------------------
    async def _safe_read(self, ctx, reads, retries: int = 1):
        """Read memory with a small retry loop to reduce transient failures."""
        last_exc = None
        reads_list = list(reads)
        for attempt in range(retries + 1):
            try:
                return await bizhawk.read(ctx.bizhawk_ctx, reads_list)
            except bizhawk.RequestFailedError as exc:
                last_exc = exc
                await asyncio.sleep(0.03)
        raise last_exc


    # -------------------------
    # ROM VALIDATION
    # -------------------------
    async def validate_rom(self, ctx) -> bool:
        """Confirm the loaded ROM is the patched WC2008 ROM and initialize client context."""
        try:
            header_bytes = await self._safe_read(
                ctx,
                [(ROM_HEADER_ADDR, ROM_HEADER_LEN, ROM_DOMAIN)],
                retries=1,
            )
            header = header_bytes[0]  # raw 16-byte header
            # allow any of our known good headers
            expected_list = EXPECTED_ROM_HEADER if isinstance(EXPECTED_ROM_HEADER, tuple) else (EXPECTED_ROM_HEADER,)
            if not any(header.startswith(h) for h in expected_list):
                logger.warning("ROM header mismatch: %r (expected %r)", header, EXPECTED_ROM_HEADER)
                # if we have a patched ROM path available, we might be hooked to
                # an existing BizHawk instance; inform user and optionally restart.
                if getattr(ctx, "patched_rom", None):
                    logger.warning("Patched ROM created at %s; make sure BizHawk is loading that file or restart the emulator.", ctx.patched_rom)
                return False
        except Exception:
            logger.exception("Failed to read ROM header for validation")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        # Sanitize password from patch metadata (archipelago.gg may set it to literal string "None")
        if ctx.password == "None":
            logger.info("Correcting malformed password from patch metadata: 'None' -> empty")
            ctx.password = None

        try:
            self.rom_slot_name = header.decode("ascii", errors="ignore")
        except Exception:
            self.rom_slot_name = None

        try:
            name_bytes = (await self._safe_read(
                ctx,
                [(PLAYER_NAME_ADDR, PLAYER_NAME_LEN, self.ram_mem_domain)],
                retries=1,
            ))[0]
            self.player_name = bytes([b for b in name_bytes if b != 0]).decode("cp1252", errors="ignore")
        except Exception:
            logger.debug("Could not read player name from RAM")
            self.player_name = None

        # Safe-mode fallback: derive slot/player name from patched ROM filename
        # Handles multiple formats:
        #   - AP_123456789_P1_Player1.nds (full AP output format)
        #   - P2_Player2_vZjnJ96ITiyVzmZbI7EhUg.nds (archipelago.gg format)
        if not self.player_name:
            patched_rom = getattr(ctx, "patched_rom", None)
            if patched_rom:
                try:
                    rom_name = os.path.basename(patched_rom)
                    logger.debug("Patched ROM filename: %s", rom_name)
                    # Match P<slot>_<SlotName> with optional UUID suffix
                    match = re.search(r"P\d+_(.+?)(?:_[a-zA-Z0-9]+)?\.nds$", rom_name, re.IGNORECASE)
                    if match:
                        inferred_name = match.group(1)
                        # Output filenames often replace spaces with underscores.
                        # Normalize back for AP slot authentication.
                        self.player_name = inferred_name.replace("_", " ")
                        logger.info("Using inferred auth from patched ROM filename: %s", self.player_name)
                    else:
                        logger.warning(
                            "ROM filename does not match expected pattern 'P<slot>_<SlotName>[_UUID].nds'. "
                            "Filename: %s. Cannot determine slot name.", rom_name
                        )
                except Exception as e:
                    logger.debug("Could not infer player name from patched ROM path: %s", e)

        self.seed_verify = False
        return True


    async def set_auth(self, ctx) -> None:
        # Prefer explicit username from the connect URL (ws://<name>@host:port).
        if getattr(ctx, "username", None):
            ctx.auth = ctx.username
            return

        if self.player_name:
            ctx.auth = self.player_name
        else:
            logger.error(
                "Could not determine player name from ROM or filename, and no username was provided in /connect. "
                "The client will prompt for slot name. You can avoid this by connecting as "
                "ws://<SlotName>@archipelago.gg:<port> or using a ROM named like P<num>_<SlotName>[_id].nds"
            )
            # Leave auth unset so BizHawkClientContext.server_auth triggers the standard username prompt.
            ctx.auth = None

    async def discover_ap_struct(self, ctx) -> None:
        """Locate the AP struct pointer and validate the in-memory magic header."""
        try:
            ptr_bytes = (await self._safe_read(ctx, [(AP_STRUCT_PTR_ADDRESS, 4, BUS_DOMAIN)], retries=1))[0]
            addr = int.from_bytes(ptr_bytes, "little")
            if 0x02000000 < addr < AP_STRUCT_PTR_ADDRESS:
                magic_len = len(EXPECTED_ROM_HEADER) * AP_MAGIC_REPEATS
                header = (await self._safe_read(ctx, [(addr, magic_len, BUS_DOMAIN)], retries=1))[0]
                if header.startswith(EXPECTED_ROM_HEADER * AP_MAGIC_REPEATS):
                    self.ap_struct_address = addr
                    try:
                        ver_offset = len(EXPECTED_ROM_HEADER) * AP_MAGIC_REPEATS
                        ver_bytes = header[ver_offset:ver_offset + 4]
                        self.rom_version = int.from_bytes(ver_bytes, "little") if len(ver_bytes) == 4 else 0
                    except Exception:
                        self.rom_version = 0
                    logger.info("Found AP struct at 0x%X (version %d)", addr, self.rom_version)
        except bizhawk.RequestFailedError:
            pass
        except Exception:
            logger.exception("Error discovering AP struct")

    # -------------------------
    # MAIN WATCHER LOOP
    # -------------------------
    async def game_watcher(self, ctx) -> None:
        """Main loop called repeatedly by the BizHawk connector."""
        try:
            if ctx.server_seed_name is None or ctx.slot_data is None:
                return

            if not self.seed_verify:
                logger.info("WC2008 client connected and verified.")
                self.seed_verify = True

            # Using direct memory mode - AP struct discovery disabled
            # All location checking and item injection work via direct RAM reads/writes
            
            # Wait for emulator to fully initialize before reading memory (first 30 frames = 3 seconds)
            self.startup_frames += 1
            if self.startup_frames < 30:
                await asyncio.sleep(0.1)
                return

            # Increment frame counter for throttling
            self.frame_count += 1

            # Always check gate guardians and final boss (only 6 addresses, safe to read every frame)
            gate_reads = [
                (EMBUST_GATE_FLAGS["address"], 1, self.ram_mem_domain),  # Embust counter byte
                (SAVAN_GATE_FLAGS[0]["address"], 1, self.ram_mem_domain),  # Savan byte 1
                (SAVAN_GATE_FLAGS[1]["address"], 1, self.ram_mem_domain),  # Savan byte 2
                (GIGORI_GATE_FLAGS[0]["address"], 1, self.ram_mem_domain),  # Gigori byte 1
                (GIGORI_GATE_FLAGS[1]["address"], 1, self.ram_mem_domain),  # Gigori byte 2
                (SEFOLILE_CLEAR_FLAG, 1, self.ram_mem_domain),  # Final boss clear flag
            ]

            gate_results = await self._safe_read(ctx, gate_reads, retries=2)

            # Prefer full duelist scan each tick to catch duel completion immediately.
            # If BizHawk rejects large batches, automatically fall back to chunked reads.
            normalized_chunk = []
            duelist_results = []
            full_duelist_list = list(DUELIST_FLAGS.items())

            if full_duelist_list and self.full_duelist_read_supported is not False:
                full_normalized = [
                    (loc_name, *self._normalize_duelist_flag(flag_addr))
                    for loc_name, flag_addr in full_duelist_list
                ]
                full_reads = [(address, 1, self.ram_mem_domain) for _, address, _ in full_normalized]
                try:
                    duelist_results = await self._safe_read(ctx, full_reads, retries=1)
                    normalized_chunk = full_normalized
                    if self.full_duelist_read_supported is not True:
                        logger.info("Using full duelist RAM scan each tick (%d flags).", len(full_normalized))
                    self.full_duelist_read_supported = True
                except bizhawk.RequestFailedError:
                    if self.full_duelist_read_supported is not False:
                        logger.warning("Full duelist RAM scan failed; falling back to chunked reads.")
                    self.full_duelist_read_supported = False

            if not duelist_results and len(self.duelist_flag_chunks) > 0:
                chunk_index = self.frame_count % len(self.duelist_flag_chunks)
                current_chunk = self.duelist_flag_chunks[chunk_index]
                normalized_chunk = [
                    (loc_name, *self._normalize_duelist_flag(flag_addr))
                    for loc_name, flag_addr in current_chunk
                ]
                duelist_reads = [(address, 1, self.ram_mem_domain) for _, address, _ in normalized_chunk]
                duelist_results = await self._safe_read(ctx, duelist_reads, retries=2)
                if chunk_index == 0:
                    logger.debug("Reading duelist chunk 0/%d (frame %d)", len(self.duelist_flag_chunks), self.frame_count)

            # Process gate guardian checks
            embust_byte = gate_results[0][0]
            savan_byte1 = gate_results[1][0]
            savan_byte2 = gate_results[2][0]
            gigori_byte1 = gate_results[3][0]
            gigori_byte2 = gate_results[4][0]
            sefolile_byte = gate_results[5][0]

            # Count Embust gate clears (bits 0-4)
            embust_count = sum(1 for bit in EMBUST_GATE_FLAGS["bits"] if (embust_byte & (1 << bit)) != 0)
            if self.prev_embust_count == -1:
                self.prev_embust_count = embust_count  # Initialize on first read
            elif embust_count >= 3 and self.prev_embust_count < 3:
                loc_id = LOCATION_NAME_TO_ID.get("World 1 - Beat Guardian embust")
                if loc_id is not None and loc_id not in self.checked_locations:
                    self.checked_locations.add(loc_id)
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [loc_id]}])
                    logger.info("Checked: World 1 - Beat Guardian embust")
                self.prev_embust_count = embust_count
            elif embust_count != self.prev_embust_count:
                self.prev_embust_count = embust_count  # Update when changed

            # Count Savan gate clears (bits 5-7 of byte1, bits 0-1 of byte2)
            savan_count = 0
            for bit in SAVAN_GATE_FLAGS[0]["bits"]:
                if (savan_byte1 & (1 << bit)) != 0:
                    savan_count += 1
            for bit in SAVAN_GATE_FLAGS[1]["bits"]:
                if (savan_byte2 & (1 << bit)) != 0:
                    savan_count += 1
            if self.prev_savan_count == -1:
                self.prev_savan_count = savan_count  # Initialize on first read
            elif savan_count >= 3 and self.prev_savan_count < 3:
                loc_id = LOCATION_NAME_TO_ID.get("World 2 - Beat Savan")
                if loc_id is not None and loc_id not in self.checked_locations:
                    self.checked_locations.add(loc_id)
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [loc_id]}])
                    logger.info("Checked: World 2 - Beat Savan")
                self.prev_savan_count = savan_count
            elif savan_count != self.prev_savan_count:
                self.prev_savan_count = savan_count  # Update when changed

            # Count Gigori gate clears (bit 7 of byte1, bits 0-3 of byte2)
            gigori_count = 0
            for bit in GIGORI_GATE_FLAGS[0]["bits"]:
                if (gigori_byte1 & (1 << bit)) != 0:
                    gigori_count += 1
            for bit in GIGORI_GATE_FLAGS[1]["bits"]:
                if (gigori_byte2 & (1 << bit)) != 0:
                    gigori_count += 1
            if self.prev_gigori_count == -1:
                self.prev_gigori_count = gigori_count  # Initialize on first read
            elif gigori_count >= 3 and self.prev_gigori_count < 3:
                loc_id = LOCATION_NAME_TO_ID.get("World 4 - Beat Gigori/Moley")
                if loc_id is not None and loc_id not in self.checked_locations:
                    self.checked_locations.add(loc_id)
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [loc_id]}])
                    logger.info("Checked: World 4 - Beat Gigori/Moley")
                self.prev_gigori_count = gigori_count
            elif gigori_count != self.prev_gigori_count:
                self.prev_gigori_count = gigori_count  # Update when changed

            # Check Sefolile final boss clear
            if self.prev_sefolile == -1:
                self.prev_sefolile = sefolile_byte  # Initialize on first read
            elif sefolile_byte != 0 and self.prev_sefolile == 0:
                loc_id = LOCATION_NAME_TO_ID.get("World 5 - Beat Sky Guardian - Sefolile")
                if loc_id is not None and loc_id not in self.checked_locations:
                    self.checked_locations.add(loc_id)
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [loc_id]}])
                    logger.info("Checked: World 5 - Beat Sky Guardian - Sefolile (VICTORY!)")
                    if not self.goal_complete:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": 30}])  # CLIENT_GOAL
                        self.goal_complete = True
                self.prev_sefolile = sefolile_byte
            else:
                self.prev_sefolile = sefolile_byte

            # Process duelist flag checks
            if len(duelist_results) > 0:
                result_idx = 0
                checks_sent_this_frame = 0
                for loc_name, _address, bit_index in normalized_chunk:
                    flag_byte = duelist_results[result_idx][0]
                    flag_set = self._is_duelist_cleared(flag_byte, bit_index)
                    
                    # Check if this is first time seeing this flag
                    if loc_name not in self.previous_flags:
                        # First read: store current RAM state, don't send check
                        self.previous_flags[loc_name] = int(flag_set)
                        logger.debug("Baseline recorded for %s: %d", loc_name, int(flag_set))
                        result_idx += 1
                        continue
                    
                    # Check for 0->1 transition (duelist just defeated)
                    prev_state = self.previous_flags[loc_name]
                    if flag_set and prev_state == 0:
                        loc_id = LOCATION_NAME_TO_ID.get(loc_name)
                        if loc_id is not None and loc_id not in self.checked_locations:
                            self.checked_locations.add(loc_id)
                            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [loc_id]}])
                            checks_sent_this_frame += 1
                            logger.info("Checked: %s (Location ID: %d)", loc_name, loc_id)
                    
                    # Update current state for next comparison
                    self.previous_flags[loc_name] = int(flag_set)
                    result_idx += 1
                
                if checks_sent_this_frame > 0:
                    logger.info("Sent %d location check(s) this frame", checks_sent_this_frame)

            # Handle received items (batch inject DP and world keys)
            if len(ctx.items_received) > self.items_received_count:
                dp_to_add = 0
                
                # Process each new item
                for i in range(self.items_received_count, len(ctx.items_received)):
                    item = ctx.items_received[i]
                    try:
                        item_name = ctx.item_names.lookup_in_game(item.item, ctx.game)
                    except Exception:
                        item_name = "Unknown Item"
                    
                    # Handle DP items (100 DP or 1000 DP)
                    if "100 DP" in item_name:
                        dp_to_add += 100
                        logger.info("Received 100 DP")
                    elif "1000 DP" in item_name:
                        dp_to_add += 1000
                        logger.info("Received 1000 DP")
                
                # Batch write DP if any to add
                if dp_to_add > 0:
                    current_dp_bytes = (await self._safe_read(ctx, [(DP_ADDRESS, 4, self.ram_mem_domain)]))[0]
                    current_dp = int.from_bytes(current_dp_bytes, "little")
                    new_dp = min(current_dp + dp_to_add, 999999)  # Cap at max DP
                    await bizhawk.write(ctx.bizhawk_ctx, [(DP_ADDRESS, new_dp.to_bytes(4, "little"), self.ram_mem_domain)])
                    logger.info("Injected %d DP (total now: %d)", dp_to_add, new_dp)
                
                # Update counter
                self.items_received_count = len(ctx.items_received)

            await asyncio.sleep(0.1)  # Check 10 times per second

        except (bizhawk.RequestFailedError, bizhawk.ConnectorError) as  e:
            # Connection hiccups are expected; try again next tick
            logger.debug("BizHawk connector error: %s", str(e)[:100])
            return
        except asyncio.TimeoutError:
            logger.debug("Game watcher timeout - will retry")
            return
        except Exception as e:
            logger.exception("Unexpected error in game_watcher: %s", str(e)[:200])
            return

# rom_patcher.py
#
# Archipelago ROM patcher for Yu-Gi-Oh! World Championship 2008
#
# PATCHING MODE:
# --------------
# DIRECT MEMORY MODE:
#    - Uses clean ROM with minimal modifications (header patch only)
#    - Client reads/writes RAM addresses directly for location checking and item injection
#    - Fully functional with all features: 92 duelist checks, gate guardians, Sefolile boss,
#      DP injection, world key unlocking, and save/load support
#    - No ROM code modifications needed

from typing import Any, Dict
from .settings import get_settings
from worlds.Files import APAutoPatchInterface
import zipfile
import os

# MD5 of the clean WC2008 ROM (EU)
WC2008_MD5 = "81FA482CFA967D2468C4ED09F57CF7CB"

# Simple header patch so the client can recognize the ROM
HEADER_OFFSET = 0x000000
PATCHED_HEADER = b"YGO WC2008"


class YugiohWC2008Patch(APAutoPatchInterface):
    """
    MultiWorld patcher for Yu-Gi-Oh! World Championship 2008.
    Loads the clean ROM, applies the base BSDIFF patch,
    injects AP metadata into the filler block, and writes out
    a patched .nds file.
    """

    game = "Yu-Gi-Oh! World Championship 2008"
    patch_file_ending = ".apwc8"
    result_file_ending = ".nds"

    # Allowed clean ROM hashes
    hashes = [WC2008_MD5]

    # Files stored in the patch archive
    files: Dict[str, bytes] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._source_data: bytes | None = None

    # -----------------------------
    # Load clean ROM
    # -----------------------------
    def get_source_data(self) -> bytes:
        """
        Return the bytes of the clean ROM.
        Prefer self.path if AP provided it.
        Fall back to settings otherwise.
        """
        # The handler.path is the location of the patch archive itself, not the clean
        # ROM.  Older implementations incorrectly used it directly which caused the
        # patcher to read the tiny .apwc8 file instead of the real ROM.  Only treat
        # `self.path` as a ROM when it doesn't match our patch extension and actually
        # exists on disk.  Otherwise fall back to the global settings value.
        rom_path = get_settings().rom_file
        if hasattr(self, "path") and self.path:
            candidate = self.path
            if os.path.exists(candidate) and not candidate.lower().endswith(self.patch_file_ending):
                rom_path = candidate

        print(f"Reading ROM from: {rom_path}")

        if not rom_path or not os.path.exists(rom_path):
            raise FileNotFoundError(f"Clean ROM not found at {rom_path}")

        with open(rom_path, "rb") as infile:
            data = infile.read()

        if len(data) < 64 * 1024 * 1024:
            raise ValueError(f"ROM too small: {len(data)} bytes. Expected ~64MB.")

        if len(data) % 512 != 0:
            raise ValueError(f"ROM size not aligned: {len(data)} bytes. Must be multiple of 512.")

        return data

    def get_source_data_with_cache(self) -> bytes:
        if self._source_data is None:
            self._source_data = self.get_source_data()
        return self._source_data

    # -----------------------------
    # Apply patch
    # -----------------------------
    def patch(self, target: str) -> None:
        """
        Write the patched ROM to the given target path.
        Steps:
        1. Load clean ROM
        2. Apply header patch for client recognition
        3. Write final ROM
        """
        # 1. Load clean ROM
        source_data = self.get_source_data_with_cache()
        data = bytearray(source_data)

        # 2. Apply header patch so client can recognize the patched ROM
        data[HEADER_OFFSET:HEADER_OFFSET + len(PATCHED_HEADER)] = PATCHED_HEADER
        print(f"Applied header patch: {PATCHED_HEADER.decode('ascii')}")

        # 3. Ensure ROM size is 512-byte aligned (required by NDS emulators)
        if len(data) % 512 != 0:
            remainder = len(data) % 512
            print(f"Warning: ROM size {len(data)} not aligned. Trimming {remainder} bytes.")
            data = data[:len(data) - remainder]

        # 4. Write final ROM
        with open(target, "wb") as outfile:
            outfile.write(data)

        print(f"Patched ROM written to: {target} ({len(data)} bytes)")

    # -----------------------------
    # Patch manifest
    # -----------------------------
    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        manifest["result_file_ending"] = self.result_file_ending
        manifest["allowed_hashes"] = self.hashes
        return manifest

    # -----------------------------
    # Read files from .apwc2008
    # -----------------------------
    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        for file in opened_zipfile.namelist():
            if file != "archipelago.json":
                self.files[file] = opened_zipfile.read(file)
        return manifest

    # -----------------------------
    # Write files into .apwc2008
    # -----------------------------
    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        for file_name, data in self.files.items():
            opened_zipfile.writestr(file_name, data)

    # -----------------------------
    # Helpers
    # -----------------------------
    def get_file(self, file: str) -> bytes:
        if file not in self.files:
            self.read()
        return self.files[file]

    def write_file(self, file_name: str, file: bytes) -> None:
        self.files[file_name] = file

from __future__ import annotations

from typing import TYPE_CHECKING
from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import YugiohWC2008World


# TODO: Add WiFi-exclusive cards and content as progression items
# (e.g., tournament unlocks, WiFi-only cards, cosmetics, etc.)
# These were lost when Nintendo WiFi Connection shut down but can now be recovered for AP.
# Consider: Should WiFi exclusives be progression-tier (higher value) or filler?
#
# Item ideas:
# - Deck lists (competitive archetypes for different duelist matchups)
# - Duel disks (cosmetic variants)
# - Clothing/avatars (character cosmetics)
# - WC duelists (World Championship tournament opponents, WiFi exclusive duels)

# ---------------------------------------------------------
# ITEM DEFINITIONS
# ---------------------------------------------------------

ITEM_NAME_TO_ID = {
    # Filler items
    "100 DP":                 6,
    "1000 DP":                7,
}


# ---------------------------------------------------------
# ITEM CLASSIFICATIONS
# ---------------------------------------------------------

DEFAULT_ITEM_CLASSIFICATIONS = {
    "100 DP":                 ItemClassification.filler,
    "1000 DP":                ItemClassification.filler,
}


# ---------------------------------------------------------
# ITEM CLASS
# ---------------------------------------------------------

class YugiohWC2008Item(Item):
    game = "Yu-Gi-Oh! World Championship 2008"


# ---------------------------------------------------------
# FILLER GENERATION
# ---------------------------------------------------------

def get_random_filler_item_name(world: YugiohWC2008World) -> str:
    """Return a valid filler item name."""
    # 50/50 DP filler split
    if world.random.randint(0, 1) == 0:
        return "100 DP"
    return "1000 DP"


# ---------------------------------------------------------
# ITEM CREATION HELPERS
# ---------------------------------------------------------

def create_item_with_correct_classification(world: YugiohWC2008World, name: str) -> YugiohWC2008Item:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    item = YugiohWC2008Item(name, classification, ITEM_NAME_TO_ID[name], world.player)
    return item


# ---------------------------------------------------------
# MAIN ITEMPOOL CREATION
# ---------------------------------------------------------

def create_items(world: YugiohWC2008World) -> None:
    itempool = []

    # Fill remaining locations with filler
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_filler = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_filler)]

    # Add to AP itempool
    world.multiworld.itempool += itempool

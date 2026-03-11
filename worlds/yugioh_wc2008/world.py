from typing import ClassVar
from worlds.AutoWorld import World
import os
import json

from .settings import WC2008Settings
from .rom_patcher import YugiohWC2008Patch
from .options import WC2008Options
from .items import (
    ITEM_NAME_TO_ID,
    create_items,
    create_item_with_correct_classification,
    get_random_filler_item_name,
)
from .locations import LOCATION_NAME_TO_ID
from .regions import create_regions
from .rules import set_rules


class YugiohWC2008World(World):
    game = "Yu-Gi-Oh! World Championship 2008"

    settings_key = "yugioh_wc2008_settings"
    settings: ClassVar[WC2008Settings]

    options_dataclass = WC2008Options

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    patcher = YugiohWC2008Patch

    # ---------------------------------------------------------
    # REQUIRED AP METHODS
    # ---------------------------------------------------------

    def create_item(self, name: str):
        return create_item_with_correct_classification(self, name)

    def create_filler(self):
        name = get_random_filler_item_name(self)
        return create_item_with_correct_classification(self, name)

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        create_items(self)

    def set_rules(self):
        set_rules(self)

    def get_filler_item_name(self):
        return "DP"

    # ---------------------------------------------------------
    # ROM PATCHING
    # ---------------------------------------------------------

    def generate_output(self, output_directory: str):
        """
        Generate the .apwc8 patch archive.
        """
        patch = YugiohWC2008Patch(player=self.player, player_name=self.player_name)

        # Add AP metadata (info about this player in the multiworld)
        player_data = {
            "player": self.player,
            "player_name": self.player_name,
        }
        patch.write_file("ap.bin", json.dumps(player_data).encode('utf-8'))

        # Output patch archive (rom_patcher.py will apply header patch only)
        patch_out = os.path.join(
            output_directory,
            f"{self.multiworld.get_out_file_name_base(self.player)}.apwc8"
        )
        patch.write(patch_out)

        super().generate_output(output_directory)

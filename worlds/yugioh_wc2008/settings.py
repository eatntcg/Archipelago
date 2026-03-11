# settings.py
import settings

# MD5 of the clean WC2008 ROM (EU)
WC2008_MD5 = "81FA482CFA967D2468C4ED09F57CF7CB"


class WC2008Settings(settings.Group):
    """
    Settings for Yu-Gi-Oh! World Championship 2008.
    Currently only includes the ROM file selection.
    """

    class RomFile(settings.UserFilePath):
        description = "Yu-Gi-Oh! World Championship 2008 (EU) ROM File"
        copy_to = "wc2008.nds"
        md5s = [WC2008_MD5]

    # leave default blank so patcher will ask for the clean ROM on first use
    # (having wc2008.nds in the repo would otherwise pre‑fill this value and
    # bypass the dialog, which was causing confusion).
    rom_file: RomFile = RomFile("")


def get_settings():
    """
    Return the global settings object for this world.
    """
    return settings.get_settings().yugioh_wc2008_settings

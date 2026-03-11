DUELIST_FLAGS = {
    # World 1
    "World 1 - Beat Skull Servant": 0x115d60,
    "World 1 - Beat Sonic Shooter": 0x115e08,
    "World 1 - Beat Nightmare Penguin": 0x115d78,
    "World 1 - Beat Elemental Hero Knospe": 0x115df0,
    "World 1 - Beat Kai Ryushin": 0x115e98,
    "World 1 - Beat Vampire curse": 0x115e20,
    "World 1 - Beat Ebon Magician Curran": 0x115d90,
    "World 1 - Beat master of oz": 0x115dc0,

    # World 2
    "World 2 - Beat Warrior Lady of the Wasteland": 0x115f28,
    "World 2 - Beat Kabazauls": 0x115f10,
    "World 2 - Beat Legendary Fisherman": 0x115fb8,
    "World 2 - Beat Exxod, Master of the Guard": 0x115f70,
    "World 2 - Beat Don Zaloog": 0x116000,
    "World 2 - Beat Gravekeeper's Commandant": 0x115fe8,
    "World 2 - Beat Dark Dusk Spirit": 0x115fd0,
    "World 2 - Beat Spirit of the Pharaoh": 0x116018,
    "World 2 - Beat Sand Moth": 0x115f40,
    "World 2 - Beat Sea Serpent Warrior of Darkness": 0x115e80,
    "World 2 - Beat Abyss Soldier": 0x115ee0,
    "World 2 - Beat Maiden of the Aqua": 0x115eb0,
    "World 2 - Beat Otohime": 0x115ec8,
    "World 2 - Beat Ocean Dragon Lord Neo-Daedalus": 0x115ef8,
    "World 2 - Beat Mech Bass": 0x115fa0,
    "World 2 - Beat ojama green": 0x116030,

    # World 3
    "World 3 - Beat Fox Fire": 0x116090,
    "World 3 - Beat Great Angus": 0x116078,
    "World 3 - Beat Molten Behemoth": 0x1160a8,
    "World 3 - Beat Luster Dragon": 0x116138,
    "World 3 - Beat Stronghold the Moving Fortress": 0x116150,
    "World 3 - Beat VWXYZ-Dragon Catapult Cannon": 0x1160c0,
    "World 3 - Beat Inpachi": 0x1161c8,
    "World 3 - Beat Blazing Inpachi": 0x1161e0,
    "World 3 - Beat Woodborg Inpachi": 0x1161f8,
    "World 3 - Beat Spirit of the Six Samurai": 0x116108,
    "World 3 - Beat Volcanic Slicer": 0x1160d8,
    "World 3 - Beat Blazewing Butterfly": 0x1160f0,
    "World 3 - Beat Iron Blacksmith Kotetsu": 0x116120,
    "World 3 - Beat Giga Gagagigo": 0x116228,
    "World 3 - Beat Blowback Dragon": 0x116198,

    # Ferrario (bit flag)
    "World 3 - Beat Ferrario": (0x116929, 2),

    # World 4
    "World 4 - Beat Mythical Beast Cerberus/Darkblaze Dragon": 0x1163c0,
    "World 4 - Beat Goe Goe the Gallant Ninja/Lady Ninja Yae": 0x116420,
    "World 4 - Beat Vanity's Fiend/Vanity's Ruler": 0x1163f0,
    "World 4 - Beat Vennominaga, the Deity of Poisonous Snakes": 0x1163a8,
    "World 4 - Beat Kahkki, Guerilla of Dark World/Zure, Knight of Dark World": 0x1164e0,
    "World 4 - Beat Goldd, Wu-Lord of Dark World/Sillva, Warlord of Dark World": 0x1164b0,
    "World 4 - Beat Brron, Mad King of Dark World/Reign-Beaux, Overlord of Dark World": 0x116480,
    "World 4 - Beat Gogiga Gagagigo/Mobius the Frost Monarch": 0x116258,
    "World 4 - Beat Vampire Lord/Vampire Lady": 0x116288,
    "World 4 - Beat Harpie Queen/Harpie Girl": 0x1162d0,
    "World 4 - Beat Metal Shooter/Satellite Cannon": 0x116300,
    "World 4 - Beat Lich Lord, King of the Underworld/Alien Hypno": 0x116378,
    "World 4 - Beat Alien Infiltrator/Alien Shocktrooper": 0x116330,

    # World 5
    "World 5 - Beat Thunder Nyan Nyan": 0x1165d0,
    "World 5 - Beat Absorbing Kid from the Sky": 0x1165e8,
    "World 5 - Beat Kiabaman": 0x116660,
    "World 5 - Beat Layard the Liberator": 0x1166f0,
    "World 5 - Beat Royal Knight": 0x116630,
    "World 5 - Beat Freya, the Spirit of Victory": 0x116618,
    "World 5 - Beat Cloudian Poison Cloud": 0x116678,
    "World 5 - Beat Dancing Fairies": 0x116690,
    "World 5 - Beat Senju of the Thousand Hands": 0x1166c0,
    "World 5 - Beat Mokey Mokey": 0x1166a8,
    "World 5 - Beat Exodius, the Ultimate Forbidden Lord": 0x1166d8,
    "World 5 - Beat Radiant Jeral": 0x116708,
    "World 5 - Beat Guardian Angel Joan": 0x116570,
    "World 5 - Beat Marshmallon": 0x116588,
    "World 5 - Beat Voltanis the Adjudicator": 0x116738,
    "World 5 - Beat Harvest Angel of Wisdom": 0x116720,
    "World 5 - Beat Rainbow Dragon": 0x1165b8,
    "World 5 - Beat Alkana Knight Joker": 0x116750,
    "World 5 - Beat The End of Anubis!": 0x1167b0,
    "World 5 - Beat Arcana Force Extra - The Light Ruler": 0x116798,
    "World 5 - Beat White Night Dragon": 0x116780,
    "World 5 - Beat Beast King Barbaros": 0x116768,
    "World 5 - Beat Soul of Purity and Light": 0x116600,
}
REQUIRED_WORLD1_DUELISTS = [
    DUELIST_FLAGS["World 1 - Beat Skull Servant"],
    DUELIST_FLAGS["World 1 - Beat Sonic Shooter"],
    DUELIST_FLAGS["World 1 - Beat Nightmare Penguin"],
    DUELIST_FLAGS["World 1 - Beat Elemental Hero Knospe"],
    DUELIST_FLAGS["World 1 - Beat Kai Ryushin"],
]

# Gate win bit flags (need 3 wins each to clear)
# EMBUST (Grace/World 1 Guardian): Bits 0-4 at 0x116928
EMBUST_GATE_FLAGS = {
    "address": 0x116928,
    "bits": [0, 1, 2, 3, 4]  # Grace 1-5
}

# SAVAN (Sunlight/World 2): Bits 5-7 at 0x116928 and bits 0-1 at 0x116929
SAVAN_GATE_FLAGS = [
    {"address": 0x116928, "bits": [5, 6, 7]},  # Sunlight 1-3
    {"address": 0x116929, "bits": [0, 1]}       # Sunlight 4-5
]

# GIGORI (Darkness/World 4): Bit 7 at 0x116929 and bits 0-3 at 0x11692a
GIGORI_GATE_FLAGS = [
    {"address": 0x116929, "bits": [7]},         # Darkness 1
    {"address": 0x11692a, "bits": [0, 1, 2, 3]} # Darkness 2-5
]

# CIVILIZATION (World 3): Bit 2 at 0x116929
CIVILIZATION_FLAG = (0x116929, 2)

# Legacy single-address exports (deprecated - use bit flag dicts above)
EMBUST_COUNTER = 0x116928
SAVAN_COUNTER = 0x116928
GIGORI_COUNTER = 0x116929
SEFOLILE_CLEAR_FLAG = 0x1167e0  # Set to 1 when Sefolile is cleared, which is required to access the final boss and thus complete the game       


#wc and beat 5 needing added for all duelist for world champion ship unlock 
#all duelests beed adding 
#all cards or card collection need adding 
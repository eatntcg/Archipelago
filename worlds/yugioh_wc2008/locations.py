from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Location

if TYPE_CHECKING:
    from .world import YugiohWC2008World

LOCATION_NAME_TO_ID = {
    #World 1 
    "World 1 - Beat Skull Servant": 1,
    "World 1 - Beat Sonic Shooter": 2,
    "World 1 - Beat Nightmare Penguin": 3,
    "World 1 - Beat Elemental Hero Knospe": 4,
    "World 1 - Beat Kai Ryushin": 5,
    "World 1 - Beat Vampire curse": 6,
    "World 1 - Beat Guardian embust": 7,
    "World 1 - Beat Ebon Magician Curran": 8,
    "World 1 - Beat master of oz": 9, #sealstone
    "World 1 - Beat All Regular Duelists": None,
    "World 1 - Beat 3 Embust Decks": None,
   

    #world 2 locations
    "World 2 - Beat Warrior Lady of the Wasteland": 10,
    "World 2 - Beat Kabazauls": 11,
    "World 2 - Beat Legendary Fisherman": 12,
    "World 2 - Beat Exxod, Master of the Guard": 13, #seal stone
    "World 2 - Beat Guardian Sphinx": 14,
    "World 2 - Beat Don Zaloog": 15,
    "World 2 - Beat Gravekeeper's Commandant": 16,
    "World 2 - Beat Dark Dusk Spirit": 17,
    "World 2 - Beat Spirit of the Pharaoh": 18,
    "World 2 - Beat Sand Moth": 19,
    "World 2 - Beat Sea Serpent Warrior of Darkness": 20,
    "World 2 - Beat Abyss Soldier": 21,
    "World 2 - Beat Maiden of the Aqua": 22,
    "World 2 - Beat Otohime": 23,
    "World 2 - Beat Ocean Dragon Lord Neo-Daedalus":24, #seal stone 
    "World 2 - Beat Savan": 25,
    "World 2 - Beat Mech Bass":79,
    "World 2 - Beat ojama green": 80, #event during civilation 
    "World 2 - Beat Dark Mimc LV1":81,
    #world 3 locations
    "World 3 - Beat Fox Fire": 26 ,
    "World 3 - Beat Great Angus": 27,
    "World 3 - Beat Molten Behemoth": 28,
    "World 3 - Beat Luster Dragon": 29,
    "World 3 - Beat Stronghold the Moving Fortress": 30,
    "World 3 - Beat Blowback Dragon": 31,
    "World 3 - Beat VWXYZ-Dragon Catapult Cannon": 32, #seal stone 
    "World 3 - Beat Inpachi": 33,
    "World 3 - Beat Blazing Inpachi": 34,
    "World 3 - Beat Woodborg Inpachi": 35, 
    "World 3 - Beat Spirit of the Six Samurai": 36,
    "World 3 - Beat Volcanic Slicer": 37,
    "World 3 - Beat Blazewing Butterfly": 38,
    "World 3 - Beat Iron Blacksmith Kotetsu": 39, 
    "World 3 - Beat Giga Gagagigo": 40,
    "World 3 - Beat Ferrario":41,
    
    #world 4 locations 
    "World 4 - Beat Mythical Beast Cerberus/Darkblaze Dragon": 42,
    "World 4 - Beat Goe Goe the Gallant Ninja/Lady Ninja Yae": 43, 
    "World 4 - Beat Vanity's Fiend/Vanity's Ruler": 44,
    "World 4 - Beat Vennominaga, the Deity of Poisonous Snakes": 45, #seal stone
    "World 4 - Beat Kahkki, Guerilla of Dark World/Zure, Knight of Dark World": 46,
    "World 4 - Beat Goldd, Wu-Lord of Dark World/Sillva, Warlord of Dark World": 47,
    "World 4 - Beat Brron, Mad King of Dark World/Reign-Beaux, Overlord of Dark World": 48,
    "World 4 - Beat Gogiga Gagagigo/Mobius the Frost Monarch": 49,
    "World 4 - Beat Vampire Lord/Vampire Lady": 50,
    "World 4 - Beat Harpie Queen/Harpie Girl": 51,
    "World 4 - Beat Metal Shooter/Satellite Cannon": 52,
    "World 4 - Beat Lich Lord, King of the Underworld/Alien Hypno": 53,
    "World 4 - Beat Alien Infiltrator/Alien Shocktrooper": 54,
    "World 4 - Beat Gigori/Moley": 55,
    "World 4 - Beat Dark Mimic  LV3": 82,

    #world 5 locations
    "World 5 - Beat Thunder Nyan Nyan": 56,
    "World 5 - Beat Absorbing Kid from the Sky": 57,
    "World 5 - Beat Kiabaman": 58,
    "World 5 - Beat Layard the Liberator": 59,
    "World 5 - Beat Royal Knight": 60,
    "World 5 - Beat Freya, the Spirit of Victory": 61,
    "World 5 - Beat Cloudian Poison Cloud": 62,
    "World 5 - Beat Dancing Fairies": 63,
    "World 5 - Beat Senju of the Thousand Hands": 64,
    "World 5 - Beat Mokey Mokey": 65,
    "World 5 - Beat Exodius, the Ultimate Forbidden Lord": 66, #seal stone
    "World 5 - Beat Radiant Jeral": 67,
    "World 5 - Beat Guardian Angel Joan": 68,
    "World 5 - Beat Marshmallon": 69,
    "World 5 - Beat Voltanis the Adjudicator": 70,
    "World 5 - Beat Harvest Angel of Wisdom": 71,
    "World 5 - Beat Rainbow Dragon": 72,
    "World 5 - Beat Alkana Knight Joker": 73,
    "World 5 - Beat The End of Anubis!": 74,
    "World 5 - Beat Arcana Force Extra - The Light Ruler": 75, 
    "World 5 - Beat White Night Dragon": 76,
    "World 5 - Beat Beast King Barbaros": 77,
    "World 5 - Beat Sky Guardian - Sefolile": 78,   #← **campaign win conditon**

    # Event locations
    "World 1 Completion": None,
    "World 2 Completion": None,
    "World 3 Completion": None,
    "World 4 Completion": None,
    "World 5 Completion": None,
    }

class YugiohWC2008Location(Location):
    game = "Yu-Gi-Oh! World Championship 2008"



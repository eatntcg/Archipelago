from BaseClasses import Region, Location
from .locations import LOCATION_NAME_TO_ID

class YugiohWC2008Location(Location):
    game = "Yu-Gi-Oh! World Championship 2008"


def create_regions(world):
    menu = Region("Menu", world.player, world.multiworld)
    world1 = Region("World 1", world.player, world.multiworld)
    world2 = Region("World 2", world.player, world.multiworld)
    world3 = Region("World 3", world.player, world.multiworld)
    world4 = Region("World 4", world.player, world.multiworld)
    world5 = Region("World 5", world.player, world.multiworld)

    world.multiworld.regions += [menu, world1, world2, world3, world4, world5]

    # Menu-based access
    menu.connect(world1)
    menu.connect(world2)
    menu.connect(world3)
    menu.connect(world4)
    menu.connect(world5)

    # Assign locations to regions  ← NOW INSIDE THE FUNCTION
    for name in LOCATION_NAME_TO_ID:
        if name.startswith("World 1"):
            world1.locations.append(YugiohWC2008Location(world.player, name, LOCATION_NAME_TO_ID[name], world1))

        elif name.startswith("World 2"):
            world2.locations.append(YugiohWC2008Location(world.player, name, LOCATION_NAME_TO_ID[name], world2))
        elif name.startswith("World 3"):
            world3.locations.append(YugiohWC2008Location(world.player, name, LOCATION_NAME_TO_ID[name], world3))
       
        elif name.startswith("World 4"):
            world4.locations.append(YugiohWC2008Location(world.player, name, LOCATION_NAME_TO_ID[name], world4))
        
        elif name.startswith("World 5"):
            world5.locations.append(YugiohWC2008Location(world.player, name, LOCATION_NAME_TO_ID[name], world5))
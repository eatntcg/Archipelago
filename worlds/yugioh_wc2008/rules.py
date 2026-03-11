from worlds.generic.Rules import set_rule

def set_rules(world):
    player = world.player

    # All worlds are always accessible.
    set_rule(world.get_entrance("Menu -> World 1"), lambda state: True)
    set_rule(world.get_entrance("Menu -> World 2"), lambda state: True)
    set_rule(world.get_entrance("Menu -> World 3"), lambda state: True)
    set_rule(world.get_entrance("Menu -> World 4"), lambda state: True)
    set_rule(world.get_entrance("Menu -> World 5"), lambda state: True)

    # Beat all 5 regular duelists → unlock Vampire Curse
    set_rule(
        world.get_location("World 1 - Beat All Regular Duelists"),
        lambda state: all(
            state.can_reach(loc, "Location", player)
            for loc in [
                "World 1 - Beat Skull Servant",
                "World 1 - Beat Sonic Shooter",
                "World 1 - Beat Nightmare Penguin",
                "World 1 - Beat Elemental Hero Knospe",
                "World 1 - Beat Kai Ryushin",
            ]
        )
    )

    set_rule(
        world.get_location("World 1 - Beat Vampire curse"),
        lambda state: state.can_reach("World 1 - Beat All Regular Duelists", "Location", player)
    )

    # Potential future goal ideas:
    # - all worlds: clear every duelist across all worlds.
    # - all duelists: clear every duelist across all worlds, including bosses and gatekeepers.
    # - all duel disks + clothing: collect every duel disk and clothing cosmetic unlock.
    # - all stone monuments: clear every duelist required to fill all 7 stone monuments.
    # - All Cards: obtain the full card collection.

    set_rule(
        world.get_location("World 1 Completion"),
        lambda state: state.can_reach("World 1 - Beat 3 Embust Decks", "Location", player)
    )

    set_rule(
        world.get_location("World 2 Completion"),
        lambda state: state.can_reach("World 2 - Beat Savan", "Location", player)
    )

    set_rule(
        world.get_location("World 3 Completion"),
        lambda state: state.can_reach("World 3 - Beat Ferrario", "Location", player)
    )

    set_rule(
        world.get_location("World 4 Completion"),
        lambda state: state.can_reach("World 4 - Beat Gigori/Moley", "Location", player)
    )

    set_rule(
        world.get_location("World 5 Completion"),
        lambda state: state.can_reach("World 5 - Beat Sky Guardian - Sefolile", "Location", player)
    )

from classes.dungeonComponents.exit import Exit
from classes.dungeonComponents.room import Room

room_list = [
            Room("Dungeon Entrance", "Here's a short placeholder description about the Dungeon Entrance.", [Exit(0, Room("Go Home", "You decide not to explore the dungeon. Probably a good idea.", None)), Exit(1), Exit(2)]),
            Room("Pond Room", "A room with a small pond.", [Exit(0), Exit(1), Exit(2)]),
            Room("Glowing Crystals Room", "A room with some glowing crystals.", [Exit(0), Exit(1), Exit(2), Exit(3)]),
            Room("Hastily abandoned kitchen", "This room has a large cauldron suspended over a recently extinguished fire pit", [Exit(0), Exit(1), Exit(2)]),
            Room("Autumnal Forrest Room", "A small grove of maple trees, the leaves have changed color for the fall.", [Exit(0), Exit(1), Exit(2), Exit(3)]),
            Room("Sleeping Quarters", "A small room with a bedroll, an extinguished firepit, and some small trinkets on a short cut of a wide log.", [Exit(0), Exit(1), Exit(2)]),
            Room("Magma River", "A 5ft wide river of magma flows in your path. You could travel up to the source of the magma, or down to see where it leads, or cross it to continue onward.", [Exit(0), Exit(1), Exit(2), Exit(3)])
            ]
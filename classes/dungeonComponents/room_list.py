from classes.dungeonComponents.exit import Exit
from classes.dungeonComponents.room import Room

room_list = [
            Room("Dungeon Entrance", "Here's a short placeholder description about the Dungeon Entrance.", [Exit(0, Room("Go Home", "You decide not to explore the dungeon. Probably a good idea.", None)), Exit(1), Exit(2)]),
            Room("Pond Room", "A room with a small pond.", [Exit(0), Exit(1)]),
            Room("Glowing Crystals Room", "A room with some glowing crystals.", [Exit(0), Exit(1), Exit(2), Exit(3)]),
            Room("Hastily abandoned kitchen", "This room has a large cauldron suspended over a recently extinguished fire pit", [Exit(0), Exit(1), Exit(2)])
            ]
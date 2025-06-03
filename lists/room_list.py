from classes.dungeon.room_components import Exit, MonsterSpawning
from classes.dungeon.room import Room
from lists.monsters_list import Goblin, Skeleton
from lists.interactables_list import Pool, GlowingCrystal

room_list = { 
    "general_explorable" : [
        Room("Dungeon Entrance", "Here's a short placeholder description about the Dungeon Entrance.", [Exit(0, Room("Go Home", "You decide not to explore the dungeon. Probably a good idea.", None)), Exit(1), Exit(2)]),
        Room("Pond Room", "A room with a small pond.", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Goblin, 8, Skeleton),[Pool(1, ["SWIM", "THROW ROCKS"], "that doesn't look too deep.", action2_avail=True)]),
        Room("Glowing Crystals Room", "A room with some glowing crystals.", [Exit(0), Exit(1), Exit(2), Exit(3)], MonsterSpawning(5, Goblin, 8, Skeleton), [GlowingCrystal(1, [], " human baby."), GlowingCrystal(2, [], "chair."), GlowingCrystal(3, [], "n adult horse.")]),
        Room("Hastily abandoned kitchen", "This room has a large cauldron suspended over a recently extinguished fire pit", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        Room("Autumnal Forrest Room", "A small grove of maple trees, the leaves have changed color for the fall.", [Exit(0), Exit(1), Exit(2), Exit(3)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        Room("Sleeping Quarters", "A small room with a bedroll, an extinguished firepit, and some small trinkets on a raw wood table.", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Goblin, 8, "twice")),
        Room("Magma River", "A 5ft wide river of magma flows in your path. You could travel up to the source of the magma, or down to see where it leads, or cross it to continue onward.", [Exit(0), Exit(1), Exit(2), Exit(3)], MonsterSpawning(5, Goblin, 8, "twice")),
        Room("Trader's Camp", "A canvas tent opened in the front reveals a pleasent interior. Currently empty shelves as a woman in her 60's appears to be packing up.", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)]),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)]),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)]),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)]),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)]),
        # Room("Deadend", "Placeholder for a deadend", [Exit(0)]),
        # Room("Second Floor Tunnel", "A narrow tunnel softly spiraling downward. This is the path to the dungeon's second floor, necessary to finding the idol.", [Exit(0), Exit(1, (Room("Second Floor Landing", "The entrance chamber to the second floor is built of smooth, blue bricks. Decorative pillars dot the edges, and an archway leads to three exits leading deeper into the dungeon.", [Exit(0), Exit(1), Exit(2), Exit(3)])))])
        ],
    "placeholder_rooms_maxed" : Room("Placeholder Rooms Maxed", 'A deadend with a sign that reads "Sorry, more rooms will be added soon!"', [Exit(0), Exit(1)]) #the second exit needs to be removed when this room is updated (maybe)
}
from classes.dungeon.room_components import Exit, MonsterSpawning
from classes.dungeon.room import Room
from lists.monsters_list import Goblin, Skeleton, Wizard, MudGolem, Minotaur, Avatar, MagmaGoblin
from lists.interactables_list import Pool, GlowingCrystal, Chest, MagmaRiver

room_list = [ 
    [
        Room("Placeholder Rooms Maxed", 'A deadend with a sign that reads "Sorry, more rooms will be added soon!"', [Exit(0), Exit(1)]) #the second exit needs to be removed when this room is updated (maybe)
        ],
    [
        Room("Dungeon Entrance", 
            "Here's a short placeholder description about the Dungeon Entrance.", 
            [Exit(0, Room("Go Home", "You decide not to explore the dungeon. Probably a good idea.", None)), Exit(1), Exit(2)]),
        Room("Pond Room", 
            "A room with a small pond.", 
            [Exit(0), Exit(1), Exit(2)], 
            MonsterSpawning(5, Goblin, 8, Skeleton), 
            [Pool(0, ["SWIM", "THROW ROCKS"], "that doesn't look too deep.", action2_avail=True)]),
        #Room("Glowing Crystals Room", 
        #    "A room with some glowing crystals.", 
        #    [Exit(0), Exit(1), Exit(2), Exit(3)], 
        #    MonsterSpawning(5, Goblin, 8, Skeleton), 
        #    [GlowingCrystal(1, ["SHATTER", "INSPECT"], " human baby.", action1_avail=True, action2_avail=True), 
        #        GlowingCrystal(2, ["SHATTER", "INSPECT"], " chair.", action1_avail=True, action2_avail=True), 
        #        GlowingCrystal(3, ["SHATTER", "INSPECT"], "n adult horse.", action1_avail=True, action2_avail=True)]),
        #Room("Magma River", 
        #    "A 10ft wide river of magma flows in your path, blocking the exit opposite from you,", 
        #    [Exit(0)], 
        #    MonsterSpawning(5, MagmaGoblin, 8, "twice"),
        #    [MagmaRiver(0, ["JUMP", "BUILD BRIDGE"], "")]),
        #Room("Hastily abandoned kitchen", "This room has a large cauldron suspended over a recently extinguished fire pit", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        #Room("Autumnal Forrest Room", "A small grove of maple trees, the leaves have changed color for the fall.", [Exit(0), Exit(1), Exit(2), Exit(3)], MonsterSpawning(5, Goblin, 8, Skeleton)),
        #Room("Sleeping Quarters", "A small room with a bedroll, an extinguished firepit, and some small trinkets on a raw wood table.", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Goblin, 8, "twice")),
        #Room("Trader's Camp", "A canvas tent opened in the front reveals a pleasent interior. Currently empty shelves as a woman in her 60's appears to be packing up.", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Goblin, 8, "twice")),
        #Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        #Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        #Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
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
        Room("Second Floor Tunnel", "A narrow tunnel softly spiraling downward. This is the path to the dungeon's second floor, necessary to finding the idol.", [Exit(0), Exit(1, link=Room("Second Floor Landing", "The entrance chamber to the second floor is built of smooth, blue bricks. Decorative pillars dot the edges, and an archway leads to three exits leading deeper into the dungeon.", exits=[Exit(0), Exit(1), Exit(2), Exit(3)]))])
        ],
    [
        Room("Second Floor Test", "Second Floor test Room1", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(6, Wizard, 10, "twice")),
        Room("Second Floor Test", "Second Floor test Room2", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(6, Wizard, 9, MudGolem)),
        Room("Second Floor Test", "Second Floor test Room3", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(4, Skeleton, 8, "twice")),
        Room("Second Floor Test", "Second Floor test Room4", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Wizard)),
        Room("Second Floor Test", "Second Floor test Room5", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Wizard)),
        Room("Second Floor Test", "Second Floor test Room6", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Wizard)),
        # Room("Second Floor Test", "Second Floor test Room", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(7, MudGolem)),
        # Room("Second Floor Test", "Second Floor test Room", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, Wizard)),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        # Room("Hallway", "Placeholder for a hallway", [Exit(0), Exit(1)], MonsterSpawning(5, Goblin, 8, "twice")),
        Room("Final Floor Tunnel", "An ornate set of smoothly carved, stone, stairs descending downward for a mile. This is the path to the dungeon's final floor, where you can find the idol and the exit.", [Exit(0), Exit(1, (Room("Final Floor Landing", "The entrance chamber to the final floor is flooded with knee high, glowing, green, liquid. Wading into the chamber, you see the paths ahead are lined with rows of stone fangs.", [Exit(0), Exit(1), Exit(2), Exit(3)])))])
        ],
    [
        Room("Final Floor Test", "Final Floor test Room1", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(4, Wizard, 8, "twice")),
        # Room("Final Floor Test", "Final Floor test Room", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(1, Skeleton, 4, "twice"), [], [Skeleton(), Skeleton()]),
        Room("Final Floor Test", "Final Floor test Room3", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(7, Minotaur)),
        Room("Final Floor Test", "Final Floor test Room4", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(7, Minotaur)),
        Room("Final Floor Test", "Final Floor test Room5", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(5, MudGolem, 10, "twice")),
        Room("Final Floor Test", "Final Floor test Room6", [Exit(0), Exit(1), Exit(2)], MonsterSpawning(2, MudGolem)),


        ]

]
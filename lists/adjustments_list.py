import random

def add_to_interactable_and_description(room):
    if room.visits == room.adjustments[2]:
        room.interactables[0].action_words.append(room.adjustments[3])
        room.description += room.adjustments[4]

def sea_creature_defeated(room):
    for each_interactable in room.interactables:
        if each_interactable.type == "SEA CREATURE":
            print(" You can now move freely again.")
            room.interactables[0].action_words.append("SWIM")
            room.interactables[0].action_words.append("THROW ROCKS")
            room.exits = room.interactables[0].exit_hold
            room.description = "A room with a small pond, the corpse of a sea creature is floating in the water."
            room.adjustments.remove(1)

def tree_inspect_renew(room):
    for each_interactable in room.interactables:
        if each_interactable.type == "TREE":
            if each_interactable.challenge >= 6 and each_interactable.gift_given == False and "INSPECT" not in each_interactable.action_words and "APOLOGIZE" not in each_interactable.action_words:
                each_interactable.action_words.append("INSPECT")

def add_monsters(room):
    if room.visits == room.adjustments[2]:
        for x in range(0, room.adjustments[3]):
            room.spawn_monster(room.adjustments[4])

def change_monster_spawning(room): # **lets find another way to input these arguements
    if room.visits == room.adjustments[5]:
        room.monster_spawning = room.adjustments[6]
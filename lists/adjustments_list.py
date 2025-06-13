import random

def add_shadow_to_pool(room):
    if room.visits == 2:
        room.interactables[0].action_words.append("INSPECT SHADOW")
        room.description += ".. Wait- there's a shadow in the water that wasn't there before."

def sea_creature_defeated(room):
    for each_interactable in room.interactables:
        if each_interactable.type == "SEA CREATURE":
            print(" You can now move freely again.")
            room.interactables[0].action_words.append("SWIM")
            room.interactables[0].action_words.append("THROW ROCKS")
            room.exits = room.interactables[0].exit_hold
            room.description = "A room with a small pond, the corpse of a sea creature is floating in the water."
            room.adjustments.pop()
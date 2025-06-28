import random

# since these are called generically but have different perameters, 
# each room will have a dictionary for the arguements of its 
# specific adjustment functins

def add_to_interactable(room, dungeon):
    if room.visits == room.adjustments[2]["add_to_interactable"][0]:
        room.interactables[0].action_words.append(room.adjustments[2]["add_to_interactable"][1])

def add_to_description(room, dungeon):
    if room.visits == room.adjustments[2]["add_to_description"][0]:
        room.description += room.adjustments[2]["add_to_description"][1]

def add_monsters(room, dungeon):
    if room.visits == room.adjustments[2]["add_monsters"][0]:
        for x in range(0, room.adjustments[2]["add_monsters"][1]):
            room.spawn_monster(room.adjustments[2]["add_monsters"][2])

def change_monster_spawning(room, dungeon): ##
    if room.visits == room.adjustments[2]["change_monster_spawning"][0]:
        room.monster_spawning = room.adjustments[2]["change_monster_spawning"][1]

def tree_inspect_renew(room, dungeon):
    for each_interactable in room.interactables:
        if each_interactable.type == "TREE":
            if each_interactable.challenge >= 6 and each_interactable.gift_given == False and "INSPECT" not in each_interactable.action_words and "APOLOGIZE" not in each_interactable.action_words:
                each_interactable.action_words.append("INSPECT")

def shop_refresh(room, dungeon):
    dungeon_length = len(dungeon["1"]) + len(dungeon["2"]) + len(dungeon["3"])
    for each_interactable in room.interactables:
        if "BUY" in each_interactable.action_words:
            if room.visits == 1: each_interactable.refresh_requirement = dungeon_length
            elif dungeon_length >= each_interactable.refresh_requirement + room.adjustments[2]["shop_refresh"][0]:
                each_interactable.inventory = room.adjustments[2]["shop_refresh"][1]
                room.adjustments[2]["shop_refresh"][0] += 1
                each_interactable.refresh_requirement = dungeon_length
                each_interactable.convo[0] = room.adjustments[2]["shop_refresh"][2]
            else: each_interactable.convo[0] = room.adjustments[2]["shop_refresh"][3]


def check_for_heavy_armor(room, player):
    if player.inventory.armor.rating == 3 or player.inventory.armor.rating==4:
        damage_player(room, player)

def damage_player(room, player):
    print(f""" {room.adjustments[2]["damage_player"][0]}""")
    player.take_damage(room.adjustments[2]["damage_player"][1], True)

def sea_creature_defeated(room, player):
    for each_interactable in room.interactables:
        if each_interactable.type == "SEA CREATURE":
            print(" You can now move freely again.")
            room.interactables[0].action_words.append("SWIM")
            room.interactables[0].action_words.append("THROW ROCKS")
            room.exits = room.interactables[0].exit_hold
            room.description = "A room with a small pond, the corpse of a sea creature is floating in the water."
            room.adjustments[1].clear()
            player.hiding = False
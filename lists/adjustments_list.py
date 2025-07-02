import random

# since these are called generically but have different perameters, 
# each room will have a dictionary for the arguements of its 
# specific adjustment functions

def add_to_interactable(nav):
    if nav.current_room.visits == nav.current_room.adjustments[2]["add_to_interactable"][0]:
        nav.current_room.interactables[0].action_words.append(nav.current_room.adjustments[2]["add_to_interactable"][1])

def add_to_description(nav):
    if nav.current_room.visits == nav.current_room.adjustments[2]["add_to_description"][0]:
        nav.current_room.description += nav.current_room.adjustments[2]["add_to_description"][1]

def add_monsters(nav):
    if nav.current_room.visits == nav.current_room.adjustments[2]["add_monsters"][0]:
        for x in range(0, nav.current_room.adjustments[2]["add_monsters"][1]):
            nav.current_room.spawn_monster(nav.current_room.adjustments[2]["add_monsters"][2])

def change_monster_spawning(nav): ##
    if nav.current_room.visits == nav.current_room.adjustments[2]["change_monster_spawning"][0]:
        nav.current_room.monster_spawning = nav.current_room.adjustments[2]["change_monster_spawning"][1]

def tree_inspect_renew(nav):
    for each_interactable in nav.current_room.interactables:
        if each_interactable.type and each_interactable.challenge >= 6 == "GLOWING TREE":
            if each_interactable.gift_given == False and "INSPECT" not in each_interactable.action_words and "APOLOGIZE" not in each_interactable.action_words:
                each_interactable.action_words.append("INSPECT")

def shop_refresh(nav):
    dungeon_length = len(nav.rooms_visited["1"]) + len(nav.rooms_visited["2"]) + len(nav.rooms_visited["3"])
    for each_interactable in nav.current_room.interactables:
        if "BUY" in each_interactable.action_words:
            if nav.current_room.visits == 1: each_interactable.refresh_requirement = dungeon_length
            elif dungeon_length >= each_interactable.refresh_requirement + nav.current_room.adjustments[2]["shop_refresh"][0]:
                each_interactable.inventory = nav.current_room.adjustments[2]["shop_refresh"][1]
                nav.current_room.adjustments[2]["shop_refresh"][0] += 1
                each_interactable.refresh_requirement = dungeon_length
                each_interactable.convo[0] = nav.current_room.adjustments[2]["shop_refresh"][2]
            else: each_interactable.convo[0] = nav.current_room.adjustments[2]["shop_refresh"][3]

def money_tree_refresh(nav):
    dungeon_length = len(nav.rooms_visited["1"]) + len(nav.rooms_visited["2"]) + len(nav.rooms_visited["3"])
    for each_interactable in nav.current_room.interactables:
        if each_interactable.type == "MONEY TREE":
            if nav.current_room.visits == 1: each_interactable.refresh_requirement = dungeon_length
            elif dungeon_length >= each_interactable.refresh_requirement + nav.current_room.adjustments[2]["money_tree_refresh"][0]:
                each_interactable.fruit += len(nav.rooms_visited[str(nav.floor)]) * nav.floor
                each_interactable.action_words.append("PICK FRUIT")
                nav.current_room.adjustments[2]["money_tree_refresh"][0] += 2
                each_interactable.refresh_requirement = dungeon_length

def block_exit(nav):
    if nav.current_room.visits == nav.current_room.adjustments[2]["block_exit"][0]:
        nav.current_room.interactables[0].exit_hold = nav.current_room.exits[nav.current_room.adjustments[2]["block_exit"][1]]
        nav.current_room.exits[nav.current_room.adjustments[2]["block_exit"][1]] = None

def change_room(nav, player):
    nav.enter_room(nav.current_room.adjustments[2]["change_room"][0])
    nav.current_room.interactables[0].exit_hold = nav.current_room.exits[0]
    nav.current_room.exits[0] = None
    nav.previous_room.adjustments[1].remove(change_room)

def check_for_heavy_armor(nav, player):
    if player.inventory.armor.rating == 3 or player.inventory.armor.rating==4:
        damage_player(nav.current_room, player)

def damage_player(nav, player):
    print(f""" {nav.current_room.adjustments[2]["damage_player"][0]}""")
    player.take_damage(nav.current_room.adjustments[2]["damage_player"][1], True)

def sea_creature_defeated(nav, player):
    for each_interactable in nav.current_room.interactables:
        if each_interactable.type == "SEA CREATURE":
            print(" You can now move freely again.")
            nav.current_room.interactables[0].action_words.append("SWIM")
            nav.current_room.interactables[0].action_words.append("THROW ROCKS")
            nav.current_room.exits = nav.current_room.interactables[0].exit_hold
            nav.current_room.description = "A room with a small pond, the corpse of a sea creature is floating in the water."
            nav.current_room.adjustments[1].clear()
            player.hiding = False
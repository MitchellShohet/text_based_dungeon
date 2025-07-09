import random
from line_spacer import line_spacer
from classes.dungeon.room_components import Exit

# since these are called generically but have different perameters, 
# each room will have a dictionary for the arguements of its 
# specific adjustment functions

def add_to_interactable(room, dungeon_length):
    if room.visits == room.adjustments[2]["add_to_interactable"][0]:
        room.interactables[0].action_words.append(room.adjustments[2]["add_to_interactable"][1])

def add_interactable(room, dungeon_length):
    if room.visits == room.adjustments[2]["add_interactable"][0]:
        room.interactables.append(room.adjustments[2]["add_interactable"][1])

def add_to_description(room, dungeon_length):
    if room.visits == room.adjustments[2]["add_to_description"][0]:
        room.description += room.adjustments[2]["add_to_description"][1]

def add_monsters(room, dungeon_length):
    if room.visits == room.adjustments[2]["add_monsters"][0]:
        for x in range(0, room.adjustments[2]["add_monsters"][1]):
            room.spawn_monster(room.adjustments[2]["add_monsters"][2])

def change_monster_spawning(room, dungeon_length): ##
    if room.visits == room.adjustments[2]["change_monster_spawning"][0]:
        room.monster_spawning = room.adjustments[2]["change_monster_spawning"][1]

def tree_inspect_renew(room, dungeon_length):
    for each_interactable in room.interactables:
        if each_interactable.type == "GLOWING TREE" and each_interactable.challenge >= 6:
            if each_interactable.gift_given == False and "INSPECT" not in each_interactable.action_words and "APOLOGIZE" not in each_interactable.action_words:
                each_interactable.action_words.append("INSPECT")

def shop_refresh(room, dungeon_length):
    for each_interactable in room.interactables:
        if "BUY" in each_interactable.action_words:
            if room.visits == 1: each_interactable.refresh_requirement = dungeon_length
            elif dungeon_length >= each_interactable.refresh_requirement + room.adjustments[2]["shop_refresh"][0]:
                each_interactable.inventory = room.adjustments[2]["shop_refresh"][1]
                room.adjustments[2]["shop_refresh"][0] += 1
                each_interactable.refresh_requirement = dungeon_length
                each_interactable.convo[0] = room.adjustments[2]["shop_refresh"][2]
            else: each_interactable.convo[0] = room.adjustments[2]["shop_refresh"][3]

def money_tree_refresh(room, dungeon_length):
    for each_interactable in room.interactables:
        if each_interactable.type == "MONEY TREE":
            if room.visits == 1: each_interactable.refresh_requirement = dungeon_length
            elif dungeon_length >= each_interactable.refresh_requirement + room.adjustments[2]["money_tree_refresh"][0]:
                each_interactable.fruit += dungeon_length
                each_interactable.action_words.append("PICK FRUIT")
                room.adjustments[2]["money_tree_refresh"][0] += 2
                each_interactable.refresh_requirement = dungeon_length

def block_exit(room, dungeon_length):
    if room.visits == room.adjustments[2]["block_exit"][0]:
        room.interactables[0].exit_hold = room.exits[room.adjustments[2]["block_exit"][1]]
        room.exits[room.adjustments[2]["block_exit"][1]] = None

def change_room(nav, player):
    nav.enter_room(nav.current_room.adjustments[2]["change_room"][0])
    if change_room in nav.previous_room.adjustments[1]: nav.previous_room.adjustments[1].remove(change_room)
    if nav.current_room.exits[0] is not None: nav.previous_room = nav.current_room.exits[0]

def block_exit(room, dungeon_length):
    room.interactables[0].exit_hold = room.exits[room.adjustments[2]["block_exit"][0]]
    room.exits[room.adjustments[2]["block_exit"][0]] = None
    if room.adjustments[2]["block_exit"][1]: print(room.adjustments[2]["block_exit"][[1]])
    room.adjustments[0].remove(block_exit)

def teleport_sequence(nav, player): #**Room options will need to be updated as we develop more
    nav.current_room.adjustments[1].remove(teleport_sequence)
    tele_options = [nav.room_options[1][0]]
    for each_room in nav.rooms_visited["1"]:
        if each_room.name == "STELLA'S TRADE CAMP" or each_room.name == "CHASM ROOM" or each_room.name == "GIANT SEQUOIA CHAMBER" or each_room.name == "SECOND FLOOR TUNNEL": tele_options.append(each_room)
    if len(nav.rooms_visited["2"]) > 0: 
        for each_room in nav.rooms_visited["2"]:
            if each_room.name == "SECOND FLOOR LANDING" or each_room.name == "FINAL FLOOR TUNNEL": tele_options.append(each_room)
    if len(nav.rooms_visited["3"]) > 0: 
        for each_room in nav.rooms_visited["3"]:
            if each_room.name == "FINAL FLOOR LANDING" or each_room.name == "IDOL ROOM": tele_options.append(each_room)
    room_choice = False
    select_loop = True
    while select_loop == True:
        for each_room in tele_options:
            print(f""" {each_room.name}""")
        print(" NEVERMIND")
        selection = input("\n - ").upper()
        if selection == "NEVERMIND": select_loop = False
        for each_room in tele_options:
            if selection == each_room.name:
                select_loop = False
                room_choice = each_room
        if select_loop == True: print(f""" {selection} is not an option here.""")
    if room_choice:
        nav.current_room.adjustments[2]["change_room"] = [Exit(0, room_choice)]
        print(f""" {nav.current_room.interactables[0].name}: {nav.current_room.interactables[0].convo[8]}""",
            "\n",
            line_spacer,
            "\n"
            "\n You feel yourself landing back on solid ground, the magic fading.")
        change_room(nav, player)
    else: print(" You changed your mind and the fairy looks disappointed")
    nav.previous_room = nav.current_room.exits[0].link

def check_for_heavy_armor(room, player):
    if player.inventory.armor.rating == 3 or player.inventory.armor.rating==4:
        damage_player(room, player)

def damage_player(room, player):
    print(f""" {room.adjustments[2]["damage_player"][0]}""")
    player.take_damage(room.adjustments[2]["damage_player"][1], True)

def sea_creature_defeated(room, player):
    for each_interactable in room.interactables:
        if each_interactable.type == "SEA CREATURE":
            print("\n You can now move freely again.")
            room.interactables[0].action_words.append("SWIM")
            room.interactables[0].action_words.append("THROW ROCKS")
            room.exits = room.interactables[0].exit_hold
            room.description = "A room with a small pond, the corpse of a sea creature is floating in the water."
            room.adjustments[1].clear()
            player.hiding = False

def add_owl(room, player):
    if len(room.interactables) == 0:
        print(" You notice an owl in the corner glaring at you.")
        room.interactables.append(room.adjustments[2]["add_owl"][0])
        room.description += " There's an owl glaring at you from the corner."

def break_the_table(room, player):
    table_destroyed = False
    for each_interactable in room.interactables:
        if each_interactable.type == "TABLE REMAINS":
            if add_to_description in room.adjustments[0]: room.adjustments[0].remove(add_to_description)
            table_destroyed = True
            room.description = "A small room with a bedroll, an extinguished firepit, and some small trinkets on the floor next to the remains of a table."
        if each_interactable.type == "BILL" and table_destroyed == True:
            each_interactable.convo[0] = "...You destroyed my table."
            room.description = "A small room with a bedroll, an extinguished firepit, and some small trinkets on the floor. A younger looking kid is looking at the remains of a destroyed table."

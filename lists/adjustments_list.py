import random
from line_spacer import line_spacer
from classes.dungeon.room_components import Exit
from classes.combatants.combatant import Combatant
from classes.inventory.inventory import Inventory
from lists.items_lists import StatMedallion, DurabilityGem, misc_options
from lists.monsters_list import Skeleton, SeaCreature
from lists.alt_rooms_list import hallway_list, dead_end_list

# since these are called generically but have different perameters, 
# each room will have a dictionary for the arguements of its 
# specific adjustment functions. The last group are the exceptions.

#-------------------------------------------------------
#---------- TRIGGERED UPON ENTERING A ROOM -------------
#-------------------------------------------------------

def pick_alt_room_description(room, dungeon_length):
    if room.visits == 1:
        if room.name == "HALLWAY": alt_room_list = hallway_list
        else: alt_room_list = dead_end_list
        alt_room = alt_room_list[random.randint(0, len(alt_room_list)-1)]
        room.description = alt_room
        alt_room_list.remove(alt_room)

def add_interactable(room, dungeon_length):
    if room.visits == room.adjustments[2]["add_interactable"][0]:
        room.interactables.append(room.adjustments[2]["add_interactable"][1])

def add_to_interactable(room, dungeon_length):
    if room.visits == room.adjustments[2]["add_to_interactable"][0]:
        room.interactables[0].action_words.append(room.adjustments[2]["add_to_interactable"][1])

def change_room_description(room, dungeon_length):
    if room.visits == room.adjustments[2]["change_room_description"][0]:
        room.description = room.adjustments[2]["change_room_description"][1]

def change_room_name(room, dungeon_length):
    if room.visits == room.adjustments[2]["change_room_name"][0]: room.name = room.adjustments[2]["change_room_name"][1]

def add_monsters(room, dungeon_length):
    if room.visits == room.adjustments[2]["add_monsters"][0]:
        for x in range(0, room.adjustments[2]["add_monsters"][1]):
            room.spawn_monster(room.adjustments[2]["add_monsters"][2])

def adjustment_print(room, dungeon_length):
    if room.visits == room.adjustments[2]["adjustment_print"][0]:
        print(room.adjustments[2]["adjustment_print"][1])

def change_monster_spawning(room, dungeon_length): ##
    if room.visits == room.adjustments[2]["change_monster_spawning"][0]:
        room.monster_spawning = room.adjustments[2]["change_monster_spawning"][1]

def change_adjustable_argument(room, dungeon_length):
    room.adjustments[2][room.adjustments[2]["change_adjustable_argument"][0]][room.adjustments[2]["change_adjustable_argument"][1]] = room.adjustments[2]["change_adjustable_argument"][2]

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

def tree_inspect_renew(room, dungeon_length):
    for each_interactable in room.interactables:
        if each_interactable.type == "GLOWING TREE" and each_interactable.challenge >= 6:
            if room.visits == 1: each_interactable.refresh_requirement = dungeon_length
            elif each_interactable.gift_given == False and "INSPECT" not in each_interactable.action_words and "APOLOGIZE" not in each_interactable.action_words and dungeon_length >= each_interactable.refresh_requirement:
                each_interactable.action_words.append("INSPECT")
                each_interactable.refresh_requirement = dungeon_length

def inspectable_renew(room, dungeon_length):
    for each_interactable in room.interactables:
        try: each_interactable.refresh_requirement + 1
        except: pass
        else:
            if room.visits == 1: each_interactable.refresh_requirement = dungeon_length + 1
            elif dungeon_length >= each_interactable.refresh_requirement:
                each_interactable.action_words.append("INSPECT")
                each_interactable.refresh_requirement = dungeon_length + 1

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
        if room.adjustments[2]["block_exit"][2]: 
            if isinstance(room.adjustments[2]["block_exit"][2], list):
                for each_descriptor in room.adjustments[2]["block_exit"][2]: print(each_descriptor)
            else: print(room.adjustments[2]["block_exit"][2])

def cave_in(room, dungeon_length): #This removes access to this room from the previous one, in case the player teleports backwards
    for each_exit in room.interactables[0].exit_hold.link.exits:
        if each_exit.link == room:
            room.interactables[1].exit_hold = each_exit
            room.interactables[0].exit_hold.link.exits.remove(each_exit)

def randomize_container_contents(room, dungeon_length):
    if room.visits == 1:
        container_options = ["CRATE", "BARREL", "TRUNK", "TENT"]
        room_containers = []
        for each_interactable in room.interactables:
            if each_interactable.type in container_options: room_containers.append(each_interactable)
        for each_container in room_containers: 
            room.interactables.remove(each_container)
        x = 0
        while x < len(room_containers):
            container = room_containers[random.randint(0,len(room_containers)-1)]
            if container.contents == 0:
                container.contents = room.adjustments[2]["randomize_container_contents"][x]
                x += 1
        random.shuffle(room_containers)
        x = 1
        for each_container in room_containers:
            each_container.number = x
            x += 1
            room.interactables.append(each_container)

def chasm_sea_creature_start1(room, dungeon_length):
    room.interactables[0].action_words  = []
    room.interactables[1].action_words = []
    room.adjustments[1].append(chasm_sea_creature_start2)

def set_exit_min(nav):
    if nav.exit_min == 1:
        nav.exit_min = nav.dungeon_length + 4

def turn_off_idol_state(nav):
    nav.idol_state = False

#-------------------------------------------------------
#------------- TRIGGERED AT END OF TURN ----------------
#-------------------------------------------------------

def block_dungeon_entrance(room, player):
    if misc_options["IDOL OF DYNAE"] in player.inventory.misc and room.exits[0] != None:
        room.adjustments[2]["block_exit"][0] = room.visits
        block_exit(room, 0)
    else:
        if room.exits[0] == None: room.exits[0] = room.interactables[0].exit_hold

def dungeon_exit_idol_test(room, player):
    if misc_options["IDOL OF DYNAE"] in player.inventory.misc and "BREAK" in room.interactables[1].action_words:
        room.interactables[1] = room.adjustments[2]["dungeon_exit_idol_test"][0]
    elif misc_options["IDOL OF DYNAE"] not in player.inventory.misc and "BREAK" not in room.interactables[1].action_words:
        room.interactables[1] = room.adjustments[2]["dungeon_exit_idol_test"][1]

def damage_player(room, player):
    print(f""" {room.adjustments[2]["damage_player"][0]}""")
    player.take_damage(room.adjustments[2]["damage_player"][1], True)

def obtain_item(room, player, interactable=None):
    if obtain_item in room.adjustments[1]: room.adjustments[1].remove(obtain_item)
    player.inventory.add_item(room.adjustments[2]["obtain_item"][0])
    if isinstance(room.adjustments[2]["obtain_item"][1], list):
        for each_text in room.adjustments[2]["obtain_item"][1]: print(f""" {each_text}""")
    else: print(f""" {room.adjustments[2]["obtain_item"][1]}""")

def remove_item(room, player):
    room.adjustments[1].remove(remove_item)
    player.inventory.remove_item(room.adjustments[2]["remove_item"][0])

def add_castle_wave(room, player):
    if len(room.monsters) == 0: 
        room.adjustments[2]["add_castle_wave"][0] += 1
        if room.adjustments[2]["add_castle_wave"][0] == 4: end_castle_sequence(room)
        elif room.adjustments[2]["add_castle_wave"][0] == 1: pass
        else:
            add_monsters(room,0)
            if room.interactables[1].type == "WIZARD TOWER UPPER FLOORS": print(f""" Suddenly {room.adjustments[2]["add_monsters"][1]} more {room.adjustments[2]["add_monsters"][2]().type}S run down the stairs!""")
            else: print(f""" Momentarily the CASTLE DOOR opens and {room.adjustments[2]["add_monsters"][1]} more {room.adjustments[2]["add_monsters"][2]().type}S pour into the courtyard!""")
            room.adjustments[2]["add_monsters"][1] += 1

def add_owl(room, player):
    if len(room.interactables) == 0:
        print(" You notice an owl in the corner glaring at you.")
        room.interactables.append(room.adjustments[2]["add_owl"][0])
        room.description.append("There's an owl glaring at you from the corner.")

def break_the_table(room, player):
    table_destroyed = False
    for each_interactable in room.interactables:
        if "REMAINS" in each_interactable.type:
            if change_room_description in room.adjustments[0]: room.adjustments[0].remove(change_room_description)
            if room.name == "BILL'S HOVEL": room.description = ["You enter a tight cavern and find a bedroll, an extinguished firepit,", "and some small trinkets on the floor next to the remains of a table."]
            table_destroyed = True
        if each_interactable.type == "BILL" and table_destroyed == True:
            each_interactable.convo[0] = "...You destroyed my table."
            room.description = ["You enter a tight cavern and find a bedroll, an extinguished firepit, and some small trinkets on the floor.", "A younger looking kid is looking at the remains of a destroyed table."]
        elif each_interactable.type == "HARBOR" and table_destroyed == True:
            each_interactable.convo = ["...You destroyed my table.", "Hey! You want to start something??", "Beat it, I don't need to deal with you.", "I better see a discount to pay for my table.", "Sure", "You don't have anything worthwhile.", "I can clear the path if you want but it's gonna cost. For you- 40 dollar bills"]
            each_interactable.price = 40
            room.description = ["The path leads to a rocky chamber with heavy timbers reenforcing the walls.", "A burly woman is looking at the remains of a destroyed table."]
        elif each_interactable.type == "SHIELD" and table_destroyed == True:
            each_interactable.convo = ["...You destroyed my sign. I worked really hard on that.", "Oh come on!! Look I didn't do anything to you, just leave!", "Please just leave.", "Okay yeah I'll look at your stock, but what about my sign?", "Ok, thanks..", "Sorry I'm not really interested in anything you have.", "A BATTLE AXE will help you get further, do you wanna buy one? It's 150 dollar bills."]
            each_interactable.price = 150
            room.adjustments[2]["obtain_item"][1] = "You traded with SHIELD and recieved a BATTLE AXE for 150 dollar bills!"
            room.description = ["You wander across a bare-bones forge with multiple BATTLE AXES on display.", "There's no sign to display the name of the place, but that would probably help business."]

def sea_creature_defeated(room, player):
    for each_interactable in room.interactables:
        if each_interactable.type == "POOL": pool = each_interactable
        if each_interactable.type == "SEA CREATURE":
            each_interactable.type = "DEFEATED SEA CREATURE"
            room.adjustments[1].remove(check_for_heavy_armor)
            pool.action_words = pool.words_hold
            room.exits = pool.exit_hold
            room.description = room.adjustments[2]["sea_creature_defeated"][0]
            player.hiding_score = random.randint(1,5)
            player.hiding = False
            print("\n You can now move freely again.")
            if room.name == "CHASM SEA CREATURE": chasm_sea_creature_defeated(room)

def check_for_heavy_armor(room, player):
    if player.inventory.armor.rating == 3 or player.inventory.armor.rating==4:
        damage_player(room, player)

def reveal_mimics(room, player): 
    if player.investigation >= 6:
        for each_interactable in room.interactables:
            try: each_interactable.reveal()
            except: pass
            else: each_interactable.reveal()
        room.adjustments[1].remove(reveal_mimics)

def sleeping_minotaur_defeated(room, player):
    for each_interactable in room.interactables:
        if each_interactable.type == "MINOTAUR":
            room.description = ["You enter an open chamber with a dead minotaur lying on a fur rug."]
            room.adjustments[1].clear()

def clear_cave_in(room, player):
    room.adjustments[1].remove(clear_cave_in)
    room.adjustments[0].append(add_interactable)
    room.interactables[2].action_words.remove("HIRE")
    room.adjustments[2]["add_interactable"][0] = room.visits + 1
    room.adjustments[2]["add_interactable"][1] = room.interactables[2]
    room.interactables.remove(room.interactables[2])
    room.interactables[1].punchline = "Somehow you feel Harbor's disappointment."
    print(" Harbor gets up, grabs some tools and heads out to clear the rubble.")
    room.exits[0].link.interactables[0].exit_hold.link.exits.append(room.exits[0].link.interactables[1].exit_hold)
    room.exits[0].link.exits[0] = room.exits[0].link.interactables[0].exit_hold
    room.exits[0].link.interactables[0].exit_hold = None
    room.exits[0].link.interactables[1].exit_hold = None
    room.exits[0].link.description = ["You enter a rocky tunnel with heavy timbers reenforcing the walls.", "The cave in has been cleared away and the passage is usable again."]

def ceribane_alchemy(room, player):
    room.adjustments[1].remove(ceribane_alchemy)
    player.inventory.add_item(StatMedallion())
    print(" You hired CERIBANE to make you a STAT MEDALLION for 2 GOLEM EYES!")
    room.adjustments[2]["ceribane_alchemy"][0] += 1
    if room.adjustments[2]['ceribane_alchemy'][0] >= 3: 
        print(" CERIBANE: Well great-grandmother needs to go gather some more ingredients. I hope we see each other again in another life.")
        room.interactables.pop(0)
        room.description = ["You see a door with an 'OPEN 7 DAYS A WEEK' sign on the front.", "Inside is a homely shop, its counters covered with books, tools, vials, and strange ingredients.", "You see a lonely, emerald cauldron longing for an old lady to hunch over it."]

def golem_machinery(room, player):
    active_gems = sum(1 for each_interactable in room.interactables if each_interactable.type == "GREEN GEM")
    working_drill = sum(1 for each_interactable in room.interactables if each_interactable.type == "DRILL")
    if active_gems == 0: 
        print(" Both gems on the machine have been destroyed!")
        shutdown_golem_machine(room)
    elif working_drill == 0:
        shutdown_golem_machine(room)
    elif room.adjustments[2]["add_monsters"][0] < room.visits: room.adjustments[2]["add_monsters"][0] = room.visits
    else: 
        add_monsters(room, 0)
        print(" A new MUD GOLEM has appeared!")

def chasm_sea_creature_start2(room, player):
    room.adjustments[1].remove(chasm_sea_creature_start2)
    room.interactables[1].description = "A rocky wall that might be climbable, if you weren't being held underwater by a SEA CREATURE."
    run_sea_creature(room, player)

def change_room(nav, player):
    nav.enter_room(nav.current_room.adjustments[2]["change_room"][0])
    if change_room in nav.previous_room.adjustments[1]: nav.previous_room.adjustments[1].remove(change_room)
    try: nav.current_room.exits[0].link
    except: pass
    else: 
        rooms_connected = False
        for each_exit in nav.current_room.exits:
            if each_exit.link == nav.previous_room:
                rooms_connected = True
        if rooms_connected == False and nav.current_room.exits[0].link != None: nav.previous_room = nav.current_room.exits[0].link


#rename to fairy_teleport after david+hailey play
def teleport_sequence(nav, player): #**Room options will need to be updated as we develop more
    nav.current_room.adjustments[1].remove(teleport_sequence)
    tele_options = [nav.room_options[1][0]]
    for each_room in nav.rooms_visited["1"]:
        if each_room.name == "MAGIC TREE GROVE" or each_room.name == "STELLA'S TRADE CAMP" or each_room.name == "VAL'S TRADE CAMP" or each_room.name == "CRYSTAL CAT" or each_room.name == "SECOND FLOOR TUNNEL": tele_options.append(each_room)
    if len(nav.rooms_visited["2"]) > 0: 
        for each_room in nav.rooms_visited["1"]:
            if each_room.name == "SECOND FLOOR TUNNEL": tele_options.append(each_room.exits[1].link)
        for each_room in nav.rooms_visited["2"]:
            if each_room.name == "MONEY TREE CHAMBER" or each_room.name == "ELM TREE CHAMBER" or each_room.name == "GARLAND'S TRADE CAMP" or each_room.name == "SHIELD'S SMITHY" or each_room.name == "JUNIOR ALCHEMIST" or each_room.name == "CAVE IN" or each_room.name == "FINAL FLOOR TUNNEL": tele_options.append(each_room)
    if len(nav.rooms_visited["3"]) > 0: 
        for each_room in nav.rooms_visited["2"]:
            if each_room.name == "FINAL FLOOR TUNNEL": tele_options.append(each_room.exits[1].link)
        for each_room in nav.rooms_visited["3"]:
            if each_room.name == "GIANT SEQUOIA CHAMBER" or each_room.name == "FINAL FLOOR MARKET" or each_room.name == "ALCHEMIST CONDO" or each_room.name == "ENCHANTMENT HOLLOW" or each_room.name == "IDOL ROOM": tele_options.append(each_room)
    room_choice = False
    select_loop = True
    while select_loop == True:
        for each_room in tele_options:
            print(f""" {each_room.name}""")
        selection = input("\n - ").upper()
        for each_room in tele_options:
            if selection == each_room.name:
                select_loop = False
                room_choice = each_room
        if select_loop == True: print(f""" {selection} is not an option here.""")
    nav.current_room.adjustments[2]["change_room"] = [Exit(0, room_choice)]
    print(f""" {nav.current_room.interactables[0].name}: {nav.current_room.interactables[0].convo[8]}""",
        "\n",
        line_spacer,
        "\n",
        "\n You feel your feet landing back on solid ground, the magic fading.")
    change_room(nav, player)
    nav.previous_room = nav.current_room.exits[0].link

def mermaid_teleport(nav, player): #**Room options will need to be updated as we develop more
    nav.current_room.adjustments[1].remove(teleport_sequence)
    tele_options = [nav.room_options[1][0]]
    for each_room in nav.rooms_visited["1"]:
        if each_room.name == "MAGIC TREE GROVE" or each_room.name == "STELLA'S TRADE CAMP" or each_room.name == "VAL'S TRADE CAMP" or each_room.name == "CRYSTAL CAT" or each_room.name == "SECOND FLOOR TUNNEL": tele_options.append(each_room)
    if len(nav.rooms_visited["2"]) > 0: 
        for each_room in nav.rooms_visited["1"]:
            if each_room.name == "SECOND FLOOR TUNNEL": tele_options.append(each_room.exits[1].link)
        for each_room in nav.rooms_visited["2"]:
            if each_room.name == "MONEY TREE CHAMBER" or each_room.name == "ELM TREE CHAMBER" or each_room.name == "GARLAND'S TRADE CAMP" or each_room.name == "SHIELD'S SMITHY" or each_room.name == "JUNIOR ALCHEMIST" or each_room.name == "CAVE IN" or each_room.name == "FINAL FLOOR TUNNEL": tele_options.append(each_room)
    if len(nav.rooms_visited["3"]) > 0: 
        for each_room in nav.rooms_visited["2"]:
            if each_room.name == "FINAL FLOOR TUNNEL": tele_options.append(each_room.exits[1].link)
        for each_room in nav.rooms_visited["3"]:
            if each_room.name == "GIANT SEQUOIA CHAMBER" or each_room.name == "FINAL FLOOR MARKET" or each_room.name == "ALCHEMIST CONDO" or each_room.name == "ENCHANTMENT HOLLOW" or each_room.name == "IDOL ROOM": tele_options.append(each_room)
    teleport_sequence(tele_options, "You feel the magic of the scale take effect, and pulls you from this place!")

#-------------------------------------------------------
#---------------- TRIGGERED ELSEWHERE ------------------
#-------------------------------------------------------

def monsters_notice_then_attack(room, player):
    for each_monster in room.monsters:
        if each_monster.is_aware == False:
            if each_monster.type == "AVATAR OF DYNAE":
                print(f"""\n The {each_monster.type} noticed you!""")
            else: print(f"""\n {each_monster.type} {each_monster.number} noticed you!""")
            each_monster.is_aware = True
        elif each_monster.type == "AVATAR OF DYNAE": print(f"""\n The {each_monster.type} is aware of you!""")
        else: print(f"""\n {each_monster.type} {each_monster.number} is aware of you!""")
        each_monster.make_attack(player)

def monsters_attempt_notice_and_attack(room, player, player_request=False):
    for each_monster in room.monsters:
        each_monster.notice_player(player.hiding_score, player_request)
        if each_monster.is_aware == True: each_monster.make_attack(player)

def monsters_attack(room, player):
    for each_monster in room.monsters: 
        if each_monster.is_aware == True: 
            if each_monster.type == "AVATAR OF DYNAE":
                print(f"""\n The {each_monster.type} is aware of you!""") 
            else: print(f"""\n {each_monster.type} {each_monster.number} is aware of you!""")
            each_monster.make_attack(player)

def player_leaves_hiding(room, player):
    player.hiding_score = random.randint(1,5) #this is the luck component of hiding for each room as the player enters it
    player.hiding = False

def run_inspect(interactable, player, room):  #Change the failure message to be dependant on a room adjustment variable
        if player.investigation + random.randint(1,5) >= interactable.invest_requirement:
            interactable.invest_requirement = 0
            interactable.effect(room=room, interactable=interactable, player=player)
        else:
            if interactable.number == 0: print(f""" The secrets of the {interactable.type} elude you.""")
            else: print(f""" The secrets of {interactable.type} {interactable.number} elude you.""")
        if "INSPECT" in interactable.action_words: interactable.action_words.remove("INSPECT")

def run_shatter(interactable, player, room):
    defender_object = Combatant(interactable.type, 1, 1, 0, int(interactable.challenge), Inventory(), interactable.number)
    player.make_attack(defender_object)
    if defender_object.current_health <= 0:
        interactable.action_words.clear()
        interactable.description = "The destroyed remains of what used to be a "+interactable.type
        interactable.type = interactable.type+" REMAINS"
        interactable.stealth_mod-=1
        try: interactable.contents.name
        except: pass
        else:
            print(f""" You found 1 {interactable.contents.name}!""")
            player.inventory.add_item(interactable.contents)
        try: interactable.contents.is_aware
        except: pass
        else:
            print(f""" A {interactable.contents.type} came out of the {interactable.type}!""")
            add_monsters(room, 0)
            room.monsters[len(room.monsters)-1].is_aware = True
            room.monsters[len(room.monsters)-1].make_attack(player)
        if interactable.contents == None: print(" There was nothing inside.")
    else: print(f""" You couldn't break {interactable.type} {interactable.number}.""")
    if "SHATTER" in interactable.action_words: interactable.action_words.remove("SHATTER")
    elif "CHOP" in interactable.action_words: interactable.action_words.remove("CHOP")
    elif "BREAK" in interactable.action_words: interactable.action_words.remove("BREAK")

def get_money(room, interactable, player):
    player.inventory.dollar_bills += room.adjustments[2]["get_money"][0]
    if isinstance(room.adjustments[2]["get_money"][1], list):
        for each_descriptor in room.adjustments[2]["get_money"][1]:
            print(f""" {each_descriptor}""")
    else: print(room.adjustments[2]["get_money"][1])

def punchline_test(interactable, action_word):
    action = False
    if action_word == "PLACE HAND" and "PLACE HAND" in interactable.action_words:
        action = " You PLACE YOUR HAND on the " + interactable.type
    elif action_word == "READ" and "READ" in interactable.action_words:
        action = f""" You READ the {interactable.type}. It says:"""
    elif action_word == "LICK" and "LICK" in interactable.action_words:
        action = " You LICK the " + interactable.type
    elif action_word == "OBSERVE" and "OBSERVE" in interactable.action_words:
        action = f""" You OBSERVE the {interactable.type} for a while."""
    elif action_word == "LOOK AT" and "LOOK AT" in interactable.action_words:
        action = f""" YOU LOOK AT the {interactable.type}!"""
    elif action_word == "INSPECT" and "INSPECT" in interactable.action_words:
        action = f""" You INSPECT the {interactable.type} for a while, determined to uncover it's secrets.."""
    elif action_word == "ADMIRE" and "ADMIRE" in interactable.action_words:
        action = f""" Now that you have a moment to ADMIRE the {interactable.type}..."""
    elif action_word == "BREAK" and "BREAK" in interactable.action_words:
        action = f""" You attempt to break the {interactable.type}!"""
    elif action_word == "SIT" and "SIT" in interactable.action_words:
        if interactable.type == "TREE" or interactable.type == "GLOWING TREE" or interactable.type == " MONEY TREE" or interactable.type == "STATUE": action = f""" You SIT under the {interactable.type} for a while. It's a good chance to organize your thoughts."""
        elif interactable.type == "TABLE": action = f""" You SIT at the {interactable.type} for a while. It's a good chance to organize your thoughts."""
        else: action = f""" You SIT on the {interactable.type} for a while. It's a good chance to organize your thoughts."""
    elif action_word == "OPEN" and "OPEN" in interactable.action_words:
        action = f""" You pull at the {interactable.type} to try and open it!"""
    if action: 
        print(action)
        if interactable.punchline: print(f""" {interactable.punchline}""")

def reveal_passage(room, interactable, player):
    print(room.adjustments[2]["reveal_passage"][0])
    interactable.action_words.append(room.adjustments[2]["reveal_passage"][1])

def end_castle_sequence(room):
    room.adjustments[1].remove(add_castle_wave)
    change_room_description(room,0)
    print(f""" You defeated all the {room.adjustments[2]["add_monsters"][2]().type}S!""")
    room.exits[0] = room.interactables[0].exit_hold
    room.interactables[0].action_words.clear()
    print(f""" The pathway behind you opened back up.""")
    if "WIZARD " in room.interactables[1].type: room.interactables[1].type = "TOWER UPPER FLOORS"
    else: room.interactables[1].type = "KEEP"
    print(f""" A strange chime sounds from the {room.interactables[1].action_words[0]} that leads into the {room.interactables[1].type}""")
    room.interactables[2].action_words.append("ADMIRE")
    room.exits[0].link.adjustments[2]["change_room_description"][0] = room.exits[0].link.visits + 1
    room.exits[0].link.adjustments[2]["add_interactable"][0] = room.exits[0].link.visits + 1

def inspect_tree(room, interactable, player):
    print(" After some time you start to understand the secrets of the GLOWING TREE. The tree feels seen and offers you a gift from its branches.")
    if interactable.number == 0 and interactable.monster.type == "WIZARD" or interactable.number == 0 and interactable.monster.type == "MUD GOLEM":
        interactable.monster.number = 1
    else:
        if sum(1 for each_monster in room.monsters if each_monster.type == "MINOTAUR") == 0: interactable.monster.number = 1
        else: interactable.monster.number = sum(1 for each_monster in room.monsters if each_monster.type == "MINOTAUR") + 1
    print(f""" The GLOWING TREE gifted you a {interactable.reward.name}!""")
    player.inventory.add_item(interactable.reward)
    interactable.gift_given = True
    print(f""" A {interactable.monster.type} has come to test you.""")
    room.monsters.append(interactable.monster)

def run_sea_creature(room, player):
    room.spawn_monster(SeaCreature, room.adjustments[2]["run_sea_creature"][0])
    pool = False
    for each_monster in room.monsters: 
        if each_monster.type == "SEA CREATURE": each_monster.is_aware = True
    for each_interactable in room.interactables:
        if each_interactable.type == "POOL": pool = each_interactable
    pool.words_hold = pool.action_words
    pool.action_words = []
    pool.exit_hold = room.exits
    room.exits = None
    player.hiding = True
    room.adjustments[1].append(check_for_heavy_armor)
    print(" Immediately you feel something WRAP AROUND YOUR LEG AND PULL YOU UNDER THE WATER!!!")

def inspect_crystal(room, interactable, player):
    print(" After some time you start to understand the secrets of the GLOWING CRYSTAL.  You're able to extract the magic and recover some health.")
    if player.current_health == player.max_health: 
        print(" Your health is currently full. Come back later to regain some from the GLOWING CRYSTAL.")
        interactable.action_words.append("INSPECT")
    else:
        player.recover_health(interactable.number*3)

def inspect_machine(room, interactable, player):
    if golem_machinery in room.adjustments[1]:
        print(" After some time you figure out how to operate the MACHINE and turn it off.")
        shutdown_golem_machine(room)
    else: print(" You play with the buttons on the machine for a bit. It's a fun time and the machine is definitely shut down.")

def shutdown_golem_machine(room):
    print(" No more MUD GOLEMS will spawn in this room.")
    room.adjustments[1].remove(golem_machinery)
    room.adjustments[2]["change_monster_spawning"][0] = room.visits
    change_monster_spawning(room, 0)

def inspect_control_panel(room, interactable, player):
    if "INSPECT FIRST DIAL" in interactable.action_words:
        print(" You're able to quickly decypher the runes of the first dial! Now to analyze the second!")
        interactable.action_words.clear()
        interactable.action_words.append("INSPECT SECOND DIAL")
    else:
        print(" You're able to quickly analyze the second dial and use both dials to shut down the barrier!")
        room.interactables.clear()
        for each_chest in room.adjustments[2]["shutdown_control_panel"]:
            room.interactables.append(each_chest)
        room.description = ["Upon crossing a door you find yourself in a room filled with a green acidic gas.", f"""At the far end you see {room.adjustments[2]["inspect_control_panel"][0]} chests behind a disabled magical interactable."""]

def get_number(container):
    return container.number

def chasm_sea_creature_defeated(room):
    room.adjustments[2]["run_sea_creature"][0] += 1
    room.interactables[0].action_words.append("SIT")
    room.interactables[1].action_words.append("INSPECT")
    room.interactables[1].description = "A rocky wall that might be climbable"

def disable_magic_barrier(room, interactable, player):
    interactable.type = "DISABLED MAGIC BARRIER"
    if interactable.challenge == 12: print(" After some time you were able to unravel the magic of the BARRIER!")
    print(" You disabled the MAGIC BARRIER!")
    interactable.effect2(room, interactable, player)

def obtain_idol(room, interactable, player):
    print("\n The IDOL OF DYNAE is before you. ")
    select_loop = True
    while select_loop == True:
        print(" Take the IDOL?")
        selection = input("\n - ").upper()
        if selection == "YES" or selection == "YE" or selection == "Y" or selection == "YEA" or selection == "YEP" or selection == "YEAH" or selection == "YUP" or selection == "YA" or selection == "YAR" or selection == "SI" or selection == "TRUE" or selection == "YAS" or selection == "YESSIR":
            select_loop = False
        else: print(f""" The IDOL draws you to it.. {selection} isn't an option.""")
    player.inventory.add_item(misc_options["IDOL OF DYNAE"])
    print("\n You got the IDOL OF DYNAE!")
    print(" Now hurry to the DUNGEON EXIT!")
    room.exits[0].link.adjustments[0].append(enter_idol_state)
    room.interactables = []
    room.monster_spawning = None
    room.description = ["The mostly collapsed chamber where the IDOL OF DYNAE was housed."]
    print("\n Suddenly you feel the ground around you begin violently shaking! The room begins collapsing in on itself and you rush back out the way you came!!")
    for x in range(len(room.monsters)):
        room.monsters[0].take_damage(random.randint(36,71), True)
        room.interactables.append(room.monsters[0])
        room.monsters.remove(room.monsters[0])
    room.adjustments[2]["change_room"] = [room.exits[0]]
    room.adjustments[1].append(change_room)

def reach_dungeon_exit(room, interactable, player):
    print("\n The DUNGEON EXIT is before you.")
    select_loop = True
    while select_loop == True:
        print(" Leave the Dungeon?")
        selection = input("\n - ").upper()
        if selection == "YES" or selection == "YE" or selection == "Y" or selection == "YEA" or selection == "YEP" or selection == "YEAH" or selection == "YUP" or selection == "YA" or selection == "YAR" or selection == "SI" or selection == "TRUE" or selection == "YAS" or selection == "YESSIR":
            select_loop = False
        elif selection == "NO" or selection == "N" or selection == "NOT YET" or selection == "NAH" or selection == "NOPE" or selection == "NOO" or selection == "NEVER" or selection == "NA":
            room.interactables[1] = room.adjustments[2]["reach_dungeon_exit"][0]
            print(" You decided to stay in the Dungeon for a little longer.")
            return
        else: print(f""" {selection} isn't an option.""")
    for x in range(len(room.monsters)):
        room.monsters.remove(room.monsters[0])
    print(line_spacer)
    print("\n As you cross the boundary leaving the Dungeon, you hear the AVATARS OF DYNAE screeching as the turn to ash behind you.")
    print(" Walking out into the bright daylight you feel the warmth of the sun against you again.")
    print(" It's hard to say how much time passed while you were in the dungeon, but that's behind you now.")
    print(" You have the IDOL OF DYNAE, a massive accomplishment that will garner fame and riches till your dying day.")
    print(" But for now, it's time to go home...")
    room.adjustments[1].append(change_room)

def enter_idol_state(nav):
    nav.idol_state = True
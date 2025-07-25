import random
from line_spacer import line_spacer
from classes.combatants.player_character import PlayerCharacter
from classes.dungeon.navigation import Navigation
from lists.items_lists import weapon_options, armor_options, HealthPotion, StatMedallion, SmokeBomb, DurabilityGem, PowerBerry
from lists.adjustments_list import change_room, teleport_sequence, check_for_heavy_armor

class PlayThrough:
    def __init__(self):
        self.player_alive = True
        self.navigation = Navigation()
        self.player_character = PlayerCharacter()
        self.player_attacking = False

    def game_start(self):
        print(f"""
            {line_spacer}
            \n Welcome to The Dungeon of Dynae! You are an explorer and must navigate through the dungeon to find the Idol of Dynae and escape!
            \n To play, simply input the choice you'd like to make. You can always input MENU to see your current options.
            \n Before you can begin your journey, you must build your adventurer's stats!
            {line_spacer}""")
        self.player_character.set_player_stats()
        print(f"""\n {self.navigation.current_room.description} """)

    def death_sequence(self):
        print(f"""\n {line_spacer}
            \n {line_spacer}
            \n You have died.
            \n {line_spacer}
            \n {line_spacer} """)
        death_loop = True
        while death_loop == True: 
            print("\n RETRY?")
            command = input("\n - ")
            if command.upper() == "NO":
                death_loop = False
                return False
            if command.upper() == "YES": #bug here where it starts you in the same dungeon as last game
                death_loop = False
                return True
            
    def nav_sequence(self, direction):
        if direction == "FORWARD":
            def move_function(): return self.navigation.test_forward()
        elif direction == "LEFT":
            def move_function(): return self.navigation.test_left()
        elif direction == "RIGHT":
            def move_function(): return self.navigation.test_right()
        elif direction == "BACKWARD":
            def move_function(): return self.navigation.test_backward()
        else: move_function = None
        try: self.navigation.current_room.exits[move_function()].link
        except: print("There is no exit that direction.")
        else: 
            if len(self.navigation.current_room.monsters) > 0: 
                for each_monster in self.navigation.current_room.monsters: #this loop determines if monsters notice and/or attack the player on their way out
                    if each_monster.is_aware == False:
                        each_monster.notice_player(self.player_character.hiding_score)
                    else:
                        print(f"""\n {each_monster.type} {each_monster.number} is aware of you!""")
                    if each_monster.is_aware == True:
                        each_monster.make_attack(self.player_character)
            if self.player_character.current_health > 0:
                print(line_spacer) #this visually segments the game for each room entered. It helps with readability.
                print(f"""\n You moved {direction}""")
                self.navigation.enter_room(self.navigation.current_room.exits[move_function()]) #uses the move function determined by the direction earlier, as an argument to move rooms
                self.player_character.hiding_score = random.randint(1,5) #this is the luck component of hiding for each room as the player enters it
                self.player_character.hiding = False

    def select_sequence(self, action_word, list):
        selection_loop = True
        while selection_loop == True:
            item_names = []
            if action_word == "HIDE": print(" Where would you like to HIDE?")
            elif action_word == "LOOK": print(" What would you like to LOOK into?")
            else: print(f""" What would you like to {action_word}?""")
            for each_thing in list: #Prints out each option for the player to choose from depending on the list provided
                if action_word == "LOOK":
                    if each_thing.number == 0 and each_thing.can_investigate == True: print(f""" {each_thing.type}""")
                    elif each_thing.can_investigate == True: print(f""" {each_thing.type} {each_thing.number}""")
                if action_word == "EQUIP":
                    if each_thing.type == "WEAPON" or each_thing.type == "ARMOR" or each_thing.name == "SHIELD":
                        if each_thing.name not in item_names:
                            item_names.append(each_thing.name)
                            print(f""" {each_thing.name}""") 
                if action_word == "USE": 
                    print(f""" {each_thing.name}""")
                if action_word == "HIDE":
                    if each_thing.number == 0: print(f""" {each_thing.type}""")
                    else: print(f""" {each_thing.type} {each_thing.number}""")
                if action_word == "ATTACK": 
                    print(f""" {each_thing.type} {each_thing.number}""")
            print(" NEVERMIND")
            selection = input("\n - ").upper()
            if selection == "NEVERMIND":
                selection_loop = False
                self.player_attacking = False
            for each_thing in list: 
                if action_word == "LOOK": #each_thing is each interactable and each monster in the room
                    if each_thing.can_investigate == True:
                        if selection == each_thing.type + " " + str(each_thing.number) or selection == each_thing.type + str(each_thing.number) or str(selection) + "0" == each_thing.type + str(each_thing.number):
                            each_thing.investigate(self.player_character, self.navigation.current_room)
                            selection_loop = False
                if action_word == "EQUIP": #each_thing is each equipable item in the player's inventory
                    if each_thing.name == selection:
                        self.player_character.equip(each_thing)
                        selection_loop = False
                        break
                if action_word == "USE": #each_thing is each consumable item in the player's inventory
                    if each_thing.name == selection:
                        if each_thing.is_healing == True and self.player_character.current_health == self.player_character.max_health:
                            print("\n Your health is already full.")
                            selection_loop = False
                        else:
                            each_thing.effect(self.player_character)
                            self.player_character.inventory.remove_item(each_thing)
                            selection_loop = False
                        break
                if action_word == "HIDE": #each_thing is each interactable in the room
                    if selection == each_thing.type + " " + str(each_thing.number) or selection == each_thing.type + str(each_thing.number) or selection + "0" == each_thing.type + str(each_thing.number):
                        print(f""" Hiding place modifier: {each_thing.stealth_mod}""") #to be removed?
                        print(f""" Luck: {self.player_character.hiding_score}""")
                        self.player_character.hiding_score += each_thing.stealth_mod + self.player_character.stealth
                        self.player_character.hiding = True
                        selection_loop = False
                if action_word == "ATTACK": #each_thing is each monster in the room
                    if selection == each_thing.type + " " + str(each_thing.number) or selection == each_thing.type + str(each_thing.number):
                        self.player_character.make_attack(each_thing)
                        if each_thing.current_health <= 0:
                            self.navigation.current_room.interactables.append(each_thing)
                            self.navigation.current_room.monsters.remove(each_thing)
                        elif each_thing.is_aware == False:
                            print(f"""\n {each_thing.type} noticed you!""")
                            each_thing.is_aware = True
                        selection_loop = False
            if selection_loop == True: print(f""" {selection} is not an option (include the number if it has one).""")

    def game_loop(self):
        while self.player_alive == True:
            print(" What would you like to do?")
            command = input("\n - ").upper()
            #-------------------------------
            if command == "FORWARD" or command == "FF" or command == "FORAWRD" or command == "FORWAR" or command == "STRAIGHT": self.nav_sequence("FORWARD")
            elif command == "LEFT" or command == "LFET" or command == "LEF": self.nav_sequence("LEFT")
            elif command == "RIGHT" or command == "RIHGT" or command == "RGIHT" or command == "RIGH": self.nav_sequence("RIGHT")
            elif command == "BACKWARD" or command == "BACK" or command == "BACKARD" or command == "BACKAWRD" or command == "BACKWAR" or command == "BAC" or command == "BAKCWARD": self.nav_sequence("BACKWARD")
            #-----------------------------
            elif command == "USE" or command == "USE ITEM" or command == "ITEM" or command == "USEITEM" or command == "USE ITE" or command == "USE ITM":
                if len(self.player_character.inventory.consumables) > 0: 
                    self.select_sequence("USE", self.player_character.inventory.consumables)
                else: print(" You have no consumables to use. Input MENU for a list of current options.")
            #-------------------------------
            elif command == "EQUIP" or command == "EQIP" or command == "EQUI" or command == "EQUP" or command == "ARMOR" or command == "SWITCH WEAPON" or command == "EQUAIP" or command == "EQUIPE":
                if self.player_character.inventory.has_equipables == True: 
                    self.select_sequence("EQUIP", self.player_character.inventory.misc)
                else: print(" You have nothing new to equip. Input MENU for a list of current options.")
            #--------------------------------
            elif command == "LOOK" or command == "PERCEPTION" or command == "INVESTIGATE" or command == "SEARCH"  or command == "LOO" or command == "LOK" or command == "LOOKE": 
                if len(self.navigation.current_room.interactables) > 0 or len(self.navigation.current_room.monsters) > 0: 
                    self.select_sequence("LOOK", self.navigation.current_room.interactables + self.navigation.current_room.monsters)
                else: print(" There's nothing to LOOK at here. Input MENU for a list of current options.")
            #---------------------------------
            elif command == "HIDE" or command == "HID":
                if self.player_character.hiding == False:
                    if len(self.navigation.current_room.interactables) > 0:
                        self.player_attacking = True
                        self.select_sequence("HIDE", self.navigation.current_room.interactables)
                        if self.player_attacking == True:
                            print(f""" player stealth: {self.player_character.stealth}. """)
                            for each_monster in self.navigation.current_room.monsters:
                                each_monster.notice_player(self.player_character.hiding_score, player_request=True)
                                if each_monster.is_aware == True: each_monster.make_attack(self.player_character)
                    else: print(" There's nowhere to hide here. Input MENU for a list of current options.")
                elif check_for_heavy_armor in self.navigation.current_room.adjustments[1]: print(" You can't hide while fighting the SEA CREATURE")
                else: print(" You are already hiding.")
            #------------------------------------
            elif command == "ATTACK" or command == "SWING SWORD" or command == "ATACK" or command == "ATTAC" or command == "ATTACVK" or command == "KILL" or command == "STAB":
                if len(self.navigation.current_room.monsters) > 0:
                    self.player_attacking = True
                    self.select_sequence("ATTACK", self.navigation.current_room.monsters)
                    if self.player_attacking == True:
                        self.player_character.hiding = False
                        for each_monster in self.navigation.current_room.monsters:
                            if each_monster.is_aware == False:
                                print(f"""\n {each_monster.type} {each_monster.number} noticed you!""")
                                each_monster.is_aware = True
                            else: print(f"""\n {each_monster.type} {each_monster.number} is aware of you!""")
                            each_monster.make_attack(self.player_character)
                else: print(" There are no monsters here to attack. Input MENU for a list of current options.")
            #---------------------------------
            elif command == "STATS" or command == "SATS" or command == "STAT" or command == "SATS" or command == "POINTS":
                self.player_character.get_player_stats()
                print(f"""\n Your current weapon is: {self.player_character.inventory.weapon.name}.""") 
                print(f""" Your current armor is: {self.player_character.inventory.armor.name}.""")
                if "SHIELD" in self.player_character.inventory.misc: print(" You are using a shield.")
            #---------------------------------
            elif command == "INVENTORY" or command == "INVNTORY" or command == "INVENTRY" or command == "INVENTOR" or command == "INVENTOY" or command == "INVETROIY" or command == "INVENTROY":
                print(f""" Your current weapon is: {self.player_character.inventory.weapon.name}.""") 
                print(f""" Your current armor is: {self.player_character.inventory.armor.name}.""")
                if "SHIELD" in self.player_character.inventory.misc: print(" You are using a shield.")
                print("\n CONSUMABLES:")
                consumables_names = []
                for each_consumable in self.player_character.inventory.consumables:
                    if each_consumable.name not in consumables_names: consumables_names.append(each_consumable.name)
                for each_consumable_name in consumables_names:
                    print(f""" {sum(1 for each_consumable in self.player_character.inventory.consumables if each_consumable.name == each_consumable_name)} {each_consumable_name}S""")
                print("\n MISC:")
                misc_names = []
                for each_misc in self.player_character.inventory.misc:
                    if each_misc.name not in misc_names: misc_names.append(each_misc.name)
                for each_misc_name in misc_names:
                    print(f""" {sum(1 for each_misc in self.player_character.inventory.misc if each_misc.name == each_misc_name)} {each_misc_name}""")
                print(f""" DOLLAR BILLS: {self.player_character.inventory.dollar_bills}""")
            #-------------------------------------
            elif command == "MENU" or command == "START" or command == "PAUSE":
                options = ["NAVIGATE OPTIONS:"]
                try:self.navigation.current_room.exits[self.navigation.test_forward()].link
                except: pass
                else: options.append("FORWARD")
                try:self.navigation.current_room.exits[self.navigation.test_left()].link
                except: pass
                else: options.append("LEFT")
                try:self.navigation.current_room.exits[self.navigation.test_right()].link
                except: pass
                else: options.append("RIGHT")
                try: self.navigation.current_room.exits[self.navigation.test_backward()].link
                except: pass
                else:
                    if self.navigation.current_room.exits[self.navigation.test_backward()].link == self.navigation.previous_room: options.append("BACKWARD")
                options.append("  ")
                options.append("GENERAL OPTIONS:")
                if len(self.navigation.current_room.monsters) > 0: options.append("ATTACK")
                if len(self.navigation.current_room.interactables) > 0 or len(self.navigation.current_room.monsters) > 0: options.append("LOOK")
                if self.player_character.hiding == False and len(self.navigation.current_room.interactables) > 0: options.append("HIDE")
                if len(self.player_character.inventory.consumables) > 0: options.append("USE ITEM")
                if self.player_character.inventory.has_equipables == True: options.append("EQUIP")
                options.append("STATS")
                options.append("INVENTORY")
                if len(self.navigation.current_room.interactables) > 0:
                    options.append(" ")
                    options.append("ROOM OPTIONS:")
                    for each_interactable in self.navigation.current_room.interactables:
                        if len(each_interactable.action_words) > 0:
                            for each_action_word in each_interactable.action_words:
                                options.append(each_action_word)
                i=0
                while i < len(options):
                    j=i+1
                    while j < len(options):
                        if options[i] == options[j]:
                            options.remove(options[j])
                            j-=1
                        j+=1
                    print(f""" {options[i]}""")
                    i+=1
            #-------------------------------------------------
            elif command == "MCS ADD ITEMS": #cheat codes
                self.player_character.inventory.add_item(weapon_options["MAGIC SWORD"])
                self.player_character.inventory.add_item(armor_options["MAGIC PLATE"])
            elif command == "MCS LEVEL UP":
                self.player_character.stat_points += 30
                self.player_character.set_player_stats()
            elif command == "DIE": self.player_character.take_damage(int(10000000000))
            #-------------------------------------------------
            else: self.navigation.current_room.room_interaction(command, self.player_character, self.navigation.current_room) #
            for each_adjustment in self.navigation.current_room.adjustments[1]:
                if each_adjustment == change_room or each_adjustment == teleport_sequence:
                    each_adjustment(self.navigation, self.player_character)
                else: each_adjustment(self.navigation.current_room, self.player_character)
            if self.player_character.current_health <= 0: self.player_alive = False
            if self.navigation.current_room.name == "Go Home":
                print(f"""
                        \n {line_spacer}
                        \n You live out the rest of your life not dying in the dungeon.
                        \n Then one day you die.
                    """)
                self.player_alive = False

is_active = True
while is_active == True:
    current_game = PlayThrough()
    current_game.game_start()
    current_game.game_loop()
    is_active = current_game.death_sequence()
    if is_active == False: print("\n Thanks for playing!")
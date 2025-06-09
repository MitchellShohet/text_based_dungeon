import random
from line_spacer import line_spacer
from classes.combatants.player_character import PlayerCharacter
from classes.dungeon.navigation import Navigation
from lists.items_lists import weapon_options, HealthPotion, StatMedallion, SmokeBomb, DurabilityGem, PowerBerry

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
            def move_function():
                return self.navigation.test_forward()
        elif direction == "BACKWARD":
            def move_function():
                return self.navigation.test_backward()
        elif direction == "LEFT":
            def move_function():
                return self.navigation.test_left()
        elif direction == "RIGHT":
            def move_function():
                return self.navigation.test_right()
        else: 
            move_function = None
        try:
            self.navigation.current_room.exits[move_function()]
        except:
            print("There is no exit that direction.")
        else: 
            if len(self.navigation.current_room.monsters) > 0:
                for each_monster in self.navigation.current_room.monsters:
                    if each_monster.is_aware == False:
                        each_monster.notice_player(self.player_character.hiding_score)
                    else:
                        print(f"""\n {each_monster.type} {each_monster.number} is aware of you!""")
                    if each_monster.is_aware == True:
                        each_monster.make_attack(self.player_character)
            print(line_spacer)
            print(f"""\n You moved {direction}""")
            self.navigation.enter_room(move_function())
            self.player_character.hiding_score = random.randint(1,5)
            self.player_character.hiding = False
            print(f""" current hiding luck: {self.player_character.hiding_score}.""")

    def select_sequence(self, action_word, list, ):
        selection_loop = True
        while selection_loop == True:
            if action_word == "HIDE":
                print("\n Where would you like to HIDE?")
            else:
                print(f""" What would you like to {action_word}?""")
            for each_thing in list:
                if action_word == "INVESTIGATE":
                    if each_thing.can_investigate == True and each_thing.number == 0:
                        print(f""" {each_thing.type}""")
                    elif each_thing.can_investigate == True:
                        print(f""" {each_thing.type} {each_thing.number}""")
                if action_word == "EQUIP":
                    if each_thing.type == "WEAPON" or each_thing.type == "ARMOR" or each_thing.name == "SHIELD":
                        print(f""" {each_thing.name}""")
                if action_word == "USE":
                    print(f""" {each_thing.name}""")
                if action_word == "HIDE":
                    if each_thing.number == 0:
                        print(f""" {each_thing.type}""")
                    else:
                        print(f""" {each_thing.type} {each_thing.number}""")
                if action_word == "ATTACK":
                        print(f""" {each_thing.type} {each_thing.number}""")
            print(" NEVERMIND")
            selection = input("\n - ").upper()
            if selection == "NEVERMIND":
                selection_loop = False
                player_attacking = False
            for each_thing in list:
                if action_word == "INVESTIGATE":
                    if selection == each_thing.type + " " + str(each_thing.number) or selection == each_thing.type + str(each_thing.number) or str(selection) + "0" == each_thing.type + str(each_thing.number):
                        each_thing.investigate(self.player_character, self.navigation.current_room)
                        selection_loop = False
                if action_word == "EQUIP":
                    if each_thing.name == selection:
                        self.player_character.equip(each_thing)
                        selection_loop = False
                        break
                if action_word == "USE":
                    if each_thing.name == selection:
                        if each_thing.name == "HEALTH POTION" and self.player_character.current_health == self.player_character.max_health or each_thing.name == "GREATER HEALTH POTION" and self.player_character.current_health == self.player_character.max_health:
                            print("\n Your health is already full.")
                            selection_loop = False
                        else:
                            each_thing.effect(self.player_character)
                            self.player_character.inventory.remove_item(each_thing)
                            selection_loop = False
                        break
                if action_word == "HIDE":
                    if selection == each_thing.type + " " + str(each_thing.number) or selection == each_thing.type + str(each_thing.number) or selection + "0" == each_thing.type + str(each_thing.number):
                        self.player_character.hiding_score += each_thing.stealth_mod + self.player_character.stealth
                        print(f"""\n Hiding place modifier: {each_thing.stealth_mod}""") #to be removed?
                        self.player_character.hiding = True
                        selection_loop = False
                if action_word == "ATTACK":
                    if selection == each_thing.type + " " + str(each_thing.number) or selection == each_thing.type + str(each_thing.number):
                        self.player_character.make_attack(each_thing)
                        if each_thing.current_health <= 0:
                            self.navigation.current_room.interactables.append(each_thing)
                            self.navigation.current_room.monsters.remove(each_thing)
                            if self.navigation.current_room.monster_spawning.monster1().type == each_thing.type:
                                self.navigation.current_room.monster1_count -= 1
                            else:
                                self.navigation.current_room.monster2_count -= 1
                        selection_loop = False
            if selection_loop == True:
                print(f"""\n {selection} is not an option (include the number if it has one).""")

    def game_loop(self):
        while self.player_alive == True:
            print(" What would you like to do?")
            command = input("\n - ").upper()
            if command == "FORWARD" or command == "FF":
                self.nav_sequence("FORWARD")
            elif command == "BACKWARD":
                self.nav_sequence("BACKWARD")
            elif command == "LEFT":
                self.nav_sequence("LEFT")
            elif command == "RIGHT":
                self.nav_sequence("RIGHT")
            elif command == "USE" or command == "USE ITEM" or command == "ITEM":
                if len(self.player_character.inventory.consumables) > 0:
                    self.select_sequence("USE", self.player_character.inventory.consumables)
                else:
                    print("You have no consumables to use.")
            elif command == "EQUIP": #add a while loop for sequence
                if self.player_character.inventory.has_equipables == True:
                    self.select_sequence("EQUIP", self.player_character.inventory.misc)
                else:
                    print("You have nothing new to equip.")
            elif command == "INVESTIGATE": 
                if len(self.navigation.current_room.interactables) > 0:
                    self.select_sequence("INVESTIGATE", self.navigation.current_room.interactables, )
                else:
                    print("\n There's nothing to INVESTIGATE here. Input MENU for a list of current options.")
                    return
            elif command == "HIDE":
                if self.player_character.hiding == False:
                    if len(self.navigation.current_room.interactables) > 0:
                        self.select_sequence("HIDE", self.navigation.current_room.interactables)
                        print(f""" player stealth: {self.player_character.stealth}. """)
                        for each_monster in self.navigation.current_room.monsters:
                            each_monster.notice_player(self.player_character.hiding_score, player_request=True)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                    else:
                        print("\n There's nowhere to hide here.")
                else:
                    print("\n You are already hiding.")
            elif command == "ATTACK":
                if len(self.navigation.current_room.monsters) > 0:
                    player_attacking = True
                    self.select_sequence("ATTACK", self.navigation.current_room.monsters)
                    if player_attacking == True:
                        self.player_character.hiding = False
                        for each_monster in self.navigation.current_room.monsters:
                            each_monster.is_aware == True
                            print(f"""\n {each_monster.type} {each_monster.number} noticed you!""")
                            each_monster.make_attack(self.player_character)
                else:
                    print("\n There are no monsters here to attack.")
            elif command == "VIEW STATS":
                self.player_character.get_player_stats()
                print(f"""\n Your current weapon is: {self.player_character.inventory.weapon.name}.""") 
                print(f""" Your current armor is: {self.player_character.inventory.armor.name}.""")
                if "SHIELD" in self.player_character.inventory.misc:
                    print(" You are using a shield.")
                print("\n CONSUMABLES:")
                for each_consumable in self.player_character.inventory.consumables:
                    print(f""" {each_consumable.name}""")
                print("\n MISC:")
                for each_misc in self.player_character.inventory.misc:
                    print(f""" {each_misc.name}""")
                print(f"""\n DOLLAR BILLS: {self.player_character.inventory.dollar_bills}""")
            elif command == "MENU":
                print("BACKWARD")
                try:self.navigation.current_room.exits(self.navigation.test_forward())
                except: pass
                else: print("FORWARD")
                try:self.navigation.current_room.exits(self.navigation.test_left())
                except: pass
                else: print("LEFT")
                try:self.navigation.current_room.exits(self.navigation.test_right())
                except: pass
                else: print("RIGHT")
                print("VIEW STATS")
                if len(self.player_character.inventory.consumables) > 0:
                    print("USE ITEM")
                if self.player_character.inventory.has_equipables == True:
                    print("EQUIP")
                if len(self.navigation.current_room.interactables) > 0:
                    print("INVESTIGATE")
                if self.player_character.hiding == False and self.player_character.hiding == False:
                    print("HIDE")
                if len(self.navigation.current_room.monsters) > 0:
                    print("ATTACK")
                if len(self.navigation.current_room.interactables) > 0:
                    for each_interactable in self.navigation.current_room.interactables:
                        if len(each_interactable.action_words) > 0:
                            for each_action_word in each_interactable.action_words:
                                print(each_action_word)







            elif command == "TEST ADD WEAPON":
                self.player_character.inventory.add_item(weapon_options["MAGIC SWORD"])
            elif command == "DIE":
                self.player_character.take_damage(int(100))
            else:
                self.navigation.current_room.room_interaction(command, self.player_character, self.navigation.current_room) #
            if self.player_character.current_health <= 0:
                self.player_alive = False
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
    if is_active == False:
        print("\n Thanks for playing!")
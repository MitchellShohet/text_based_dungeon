import random
from line_spacer import line_spacer
from classes.combatants.player_character import PlayerCharacter
from classes.dungeon.navigation import Navigation
from classes.inventory.items import Item
from lists.items_lists import weapon_options, HealthPotion, StatMedallion, SmokeBomb, DurabilityGem, PowerBerry

class PlayThrough:
    def __init__(self):
        self.player_alive = True
        self.navigation = Navigation()
        self.player_character = PlayerCharacter()

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
            command = input("\n RETRY? - ")
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
            print(f"""\n You moved {direction}""")
            self.navigation.enter_room(move_function())
            self.player_character.hiding_score = random.randint(1,5)
            self.player_character.hiding = False
            print(f"""\n current hiding luck: {self.player_character.hiding_score}.""")

#-- work on moving the functions outside of the loop for cleanliness?
    def game_loop(self):
        while self.player_alive == True:
            command = input("\n What would you like to do? - ").upper()
            if command == "FORWARD":
                self.nav_sequence(command)
            elif command == "BACKWARD":
                self.nav_sequence(command)
            elif command == "LEFT":
                self.nav_sequence(command)
            elif command == "RIGHT":
                self.nav_sequence(command)
            elif command == "VIEW STATS":
                self.player_character.get_player_stats()
                print(f"""\n Current weapon: {self.player_character.inventory.weapon}. 
                    \n Current armor: {self.player_character.inventory.armor}.""")
                if "SHIELD" in self.player_character.inventory.misc:
                    print("You are using a shield.")
            elif command == "USE":
                if len(self.player_character.inventory.consumables) > 0:
                    print("\n Which item do you want to use?")
                    for each_item in self.player_character.inventory.consumables:
                        print(f"""\n {each_item.name}""")
                    item_using = input("\n - ")
                    for each_item in self.player_character.inventory.consumables:
                        if each_item.name == item_using.upper():
                            each_item.effect(self.player_character)
                            self.player_character.inventory.remove_item(each_item)
                            break
            elif command == "EQUIP":
                if self.player_character.inventory.has_equipables == True:
                    for each_item in self.player_character.inventory.misc:
                        if each_item.type == "WEAPON" or each_item.type == "ARMOR":
                            print(f"""\n {each_item.name}""")
                    new_equip = input("\n Which item would you like to equip?").upper
                    for each_item in self.player_character.inventory.misc:
                        if each_item.name == new_equip:
                            self.player_character.equip(each_item)
                            break
                        else:
                            print(f"""\n {each_item.name} did not equal {new_equip.upper()}""")
                else:
                    print("You have nothing new to equip.")
            elif command == "INVESTIGATE": 
                if len(self.navigation.current_room.interactables) > 0:
                    selection_loop = True
                    while selection_loop == True:
                        print("\n What would you like to investigate?")
                        for each_interactable in self.navigation.current_room.interactables:
                            if each_interactable.can_investigate == True:
                                print(f"""\n {each_interactable.type} {each_interactable.number}""")
                        print("\n NEVERMIND")
                        selection = input(" - ").upper()
                        if selection == "NEVERMIND":
                            selection_loop = False
                        for each_interactable in self.navigation.current_room.interactables:
                            if selection == each_interactable.type + " " + str(each_interactable.number) or each_interactable.type + str(each_interactable.number):
                                each_interactable.investigate(self.player_character)
                                selection_loop = False
                        if selection_loop == True:
                                cancel = input(f"""\n {selection} is not an option. Investigate something else? (Please include the number)""")
                                if cancel == "NO":
                                    selection_loop = False
                else:
                    print("\n There's nothing to INVESTIGATE here. Input MENU for a list of current options.")
                    return
            elif command == "HIDE":
                if self.player_character.hiding == False:
                    if len(self.navigation.current_room.interactables) > 0:
                        selection_loop = True
                        while selection_loop == True:
                            print("\n Where are you going to hide?")
                            for each_interactable in self.navigation.current_room.interactables:
                                print(f"""\n {each_interactable.type} {each_interactable.number}""")
                            print("\n NEVERMIND")
                            selection = input(" - ").upper()
                            if selection == "NEVERMIND":
                                selection_loop = False
                            for each_interactable in self.navigation.current_room.interactables:
                                if selection == each_interactable.type + " " + str(each_interactable.number) or selection == each_interactable.type + str(each_interactable.number):
                                    self.player_character.hiding_score += each_interactable.stealth_mod + self.player_character.stealth
                                    print(f"""\n Hiding place modifier: {each_interactable.stealth_mod}""") #to be removed
                                    self.player_character.hiding = True
                                    selection_loop = False
                                    break
                            if selection_loop == True:
                                cancel = input(f"""\n {selection} is not an option. Hide somewhere else?""").upper()
                                if cancel == "NO":
                                    selection_loop = False
                        print(f"""\n player stealth: {self.player_character.stealth}. """)
                        for each_monster in self.navigation.current_room.monsters:
                            each_monster.notice_player(self.player_character.hiding_score, player_request=True)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                    else:
                        print("\n There's nowhere to hide here.")
                else:
                    print("\n You are already hiding.")
            elif command == "ATTACK":
                if len(self.navigation.current_room.monsters) == 0:
                    print("\n There are no monsters here to attack.")
                else:
                    player_attacking = True
                    attack_ready = False
                    while attack_ready == False:
                        print("\n Which monster will you attack?")
                        for each_monster in self.navigation.current_room.monsters:
                            print(f"""\n {each_monster.type} {each_monster.number}""")
                        print("\n NEVERMIND")
                        attack_choice = input("\n - ").upper()
                        if attack_choice == "NEVERMIND":
                            attack_ready = True
                            player_attacking = False
                        else:
                            for each_monster in self.navigation.current_room.monsters:
                                if attack_choice == each_monster.type + " " + str(each_monster.number) or attack_choice == each_monster.type + str(each_monster.number):
                                    attack_ready = True
                                    self.player_character.make_attack(each_monster)
                                    if each_monster.current_health <= 0:
                                        self.navigation.current_room.interactables.append(each_monster)
                                        self.navigation.current_room.monsters.remove(each_monster)
                                        if self.navigation.current_room.monster_spawning.monster1().type == each_monster.type:
                                            self.navigation.current_room.monster1_count -= 1
                                        else:
                                            self.navigation.current_room.monster2_count -= 1
                            if attack_ready == False:
                                print(f"""\n {attack_choice} isn't an option here (include the monster and its number).""")
                    if player_attacking == True:
                        for each_monster in self.navigation.current_room.monsters:
                            each_monster.is_aware == True
                            print(f"""\n {each_monster.type} {each_monster.number} noticed you!""")
                            each_monster.make_attack(self.player_character)







            elif command == "TEST ADD WEAPON":
                self.player_character.inventory.add_item(weapon_options["MAGIC SWORD"])
            elif command == "TEST ADD CONSUMABLE":
                self.player_character.inventory.add_item(HealthPotion())
                self.player_character.inventory.add_item(StatMedallion())
                self.player_character.inventory.add_item(SmokeBomb())
                self.player_character.inventory.add_item(DurabilityGem())
                self.player_character.inventory.add_item(PowerBerry())
            elif command == "TEST LEVEL UP":
                self.player_character.stat_points += 1
                self.player_character.set_player_stats()
            elif command == "DIE":
                self.player_character.take_damage(int(100))
            elif command == "MENU":
                print("The MENU logic isn't written yet, this is a placeholder.")
            else:
                self.navigation.current_room.room_interaction(self.player_character, command)
            if self.player_character.current_health <= 0:
                self.player_alive = False
            if self.navigation.current_room.name == "Go Home":
                print(f"""
                        \n {line_spacer}
                        \n You live out the rest of your life not dying in the dungeon.
                        \n Then one day you die.
                    """)
                self.player_alive = False
            print(f"""\n {line_spacer}""")

is_active = True
while is_active == True:
    current_game = PlayThrough()
    current_game.game_start()
    current_game.game_loop()
    is_active = current_game.death_sequence()
    if is_active == False:
        print( "Thanks for playing!")
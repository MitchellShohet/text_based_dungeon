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

#--This needs to be cleaned up
    def game_loop(self):
        while self.player_alive == True:
            command = input("\n What would you like to do? - ")
            if command.upper() == "VIEW STATS":
                self.player_character.get_player_stats()
            elif command.upper() == "MONSTERS":
                self.navigation.current_room.view_monster_count(True)
            elif command.upper() == "FORWARD":
                try:
                    self.navigation.current_room.exits[self.navigation.test_forward()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    if len(self.navigation.current_room.monsters) > 0:
                        for each_monster in self.navigation.current_room.monsters:
                            each_monster.notice_player(self.player_character.hiding_score)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                    self.navigation.enter_room(self.navigation.test_forward())
                    self.player_character.hiding_score = random.randint(1,5)
            elif command.upper() == "BACKWARD":
                if len(self.navigation.current_room.monsters) > 0:
                        for each_monster in self.navigation.current_room.monsters:
                            if each_monster.is_aware == False:
                                each_monster.notice_player(self.player_character.hiding_score)
                            else:
                                print(f"""\n {each_monster.type.number} is aware of you!""")
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                self.navigation.enter_room(self.navigation.test_backward())
                self.player_character.hiding_score = random.randint(1,5)
            elif command.upper() == "LEFT":
                try:
                    self.navigation.current_room.exits[self.navigation.test_left()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    if len(self.navigation.current_room.monsters) > 0:
                        for each_monster in self.navigation.current_room.monsters:
                            each_monster.notice_player(self.player_character.hiding_score)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                    self.navigation.enter_room(self.navigation.test_left())
                    self.player_character.hiding_score = random.randint(1,5)
            elif command.upper() == "RIGHT":
                try:
                    self.navigation.current_room.exits[self.navigation.test_right()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    if len(self.navigation.current_room.monsters) > 0:
                        for each_monster in self.navigation.current_room.monsters:
                            each_monster.notice_player(self.player_character.hiding_score)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                    self.navigation.enter_room(self.navigation.test_right())
                    self.player_character.hiding_score = random.randint(1,5)
            elif command.upper() == "ATTACK":
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
            elif command.upper() == "EQUIP":
                if self.player_character.inventory.has_equipables == True:
                    for each_item in self.player_character.inventory.misc:
                        if each_item.type == "WEAPON" or each_item.type == "ARMOR":
                            print(f"""\n {each_item.name}""")
                    new_equip = input("\n Which item would you like to equip?")
                    for each_item in self.player_character.inventory.misc:
                        if each_item.name.upper() == new_equip.upper():
                            self.player_character.equip(each_item)
                            break
                        else:
                            print(f"""\n {each_item.name} did not equal {new_equip.upper()}""")
                else:
                    print("You have nothing new to equip.")
            elif command.upper() == "USE":
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
            elif command.upper() == "INVESTIGATE": 
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
                            if selection == each_interactable.type + " " + str(each_interactable.number) or each_interactable.type + str(each_interactable.number) :
                                each_interactable.investigate(self.player_character)
                                selection_loop = False
                        if selection_loop == True:
                                cancel = input(f"""\n {selection} is not an option. Investigate something else? (Please include the number)""")
                                if cancel == "NO":
                                    selection_loop = False
                else:
                    print("\n There's nothing to INVESTIGATE here. Input MENU for a list of current options.")
                    return
            elif command.upper() == "HIDE":
                if len(self.navigation.current_room.monsters) > 0:
                    if len(self.navigation.current_room.interactables) > 0:
                        print(f"""\n current hiding score: {self.player_character.hiding_score}.""")
                        selection_loop = True
                        while selection_loop == True:
                            print("\n Where are you going to hide?")
                            for each_interactable in self.navigation.current_room.interactables:
                                print(f"""\n {each_interactable.type}""")
                            selection = input(" - ").upper()
                            for each_interactable in self.navigation.current_room.interactables:
                                if each_interactable.type == selection:
                                    self.player_character.hiding_score += each_interactable.stealth_mod + self.player_character.stealth
                                    print(f"""\n Hiding place mod: {each_interactable.stealth_mod}""")
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
                    print("\n There's no monsters to hide from here.")                    

            elif command.upper() == "TEST ADD WEAPON":
                self.player_character.inventory.add_item(weapon_options["MAGIC SWORD"])
            elif command.upper() == "TEST ADD CONSUMABLE":
                self.player_character.inventory.add_item(HealthPotion())
                self.player_character.inventory.add_item(StatMedallion())
                self.player_character.inventory.add_item(SmokeBomb())
                self.player_character.inventory.add_item(DurabilityGem())
                self.player_character.inventory.add_item(PowerBerry())
            elif command.upper() == "TEST LEVEL UP":
                self.player_character.stat_points += 1
                self.player_character.set_player_stats()
            elif command.upper() == "DIE":
                self.player_character.take_damage(int(100))
            elif command.upper() == "MENU":
                print("The MENU logic isn't written yet, this is a placeholder.")
            else:
                self.navigation.current_room.room_interaction(self.player_character, command.upper)
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
        print( "Thanks for playing!")
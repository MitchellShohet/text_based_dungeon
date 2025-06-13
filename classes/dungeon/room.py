import random
from classes.dungeon.room_components import Exit

class Room:
    def __init__(self, name, description, exits=[Exit(0)], monster_spawning=None, interactables=[], adjustments=None):
        self.name = name
        self.description = description
        self.exits = exits
        self.monster_spawning = monster_spawning
        self.monsters = []
        self.interactables = interactables
        self.monster1_count = 0
        self.monster2_count = 0
        self.monster1_number = 1
        self.monster2_number = 1
        self.visits = 0
        self.adjustments=adjustments

    def set_exit_link(self, number, room):
        self.exits[number].set_link(room)

    def spawn_monster(self, monster_given=False): #this can be cleaned up to be more DRY
        if monster_given == False:
            if self.monster_spawning is not None:            
                monster_chance = random.randint(1, 10)
                if self.monster_spawning.threshold2 is not None:
                    if monster_chance >= self.monster_spawning.threshold2:
                        if self.monster_spawning.monster2 == "twice":
                            print(f""" Two new {self.monster_spawning.monster1().type}S have appeared!""")
                            first_monster1 = self.monster_spawning.monster1()
                            second_monster1 = self.monster_spawning.monster1()
                            first_monster1.number = self.monster1_number
                            second_monster1.number = self.monster1_number + 1
                            self.monsters.append(first_monster1)
                            self.monsters.append(second_monster1)
                            self.monster1_count += 2
                            self.monster1_number += 2
                        else: 
                            print(f""" A new {self.monster_spawning.monster2().type} has appeared!""")
                            monster = self.monster_spawning.monster2()
                            monster.number = self.monster2_number
                            self.monsters.append(monster)
                            self.monster2_count += 1
                            self.monster2_number += 1
                        monster_chance = 0
                if monster_chance >= self.monster_spawning.threshold1:
                    print(f""" A new {self.monster_spawning.monster1().type} has appeared!""")
                    monster = self.monster_spawning.monster1()
                    monster.number = self.monster1_number
                    self.monsters.append(monster)
                    self.monster1_count += 1
                    self.monster1_number += 1
        else:
            print(f""" A new {monster_given().type} has appeared!""")
            if monster_given().type == self.monster_spawning.monster1().type:
                monster = self.monster_spawning.monster1()
                monster.number = self.monster1_number
                self.monsters.append(monster)
                self.monster1_count += 1
                self.monster1_number += 1
            elif monster_given().type == self.monster_spawning.monster2().type:
                monster = self.monster_spawning.monster2()
                monster.number = self.monster2_number
                self.monsters.append(monster)
                self.monster2_count += 1
                self.monster2_number += 1
            else:
                monster = monster_given()
                monster.number = 1
                self.monsters.append(monster)


    def view_monster_count(self, player_request=False):
        if self.monster_spawning is not None: 
            if self.monster1_count == 1 and self.monster2_count == 0:
                print(f""" A {self.monster_spawning.monster1().type} is here.""")
            elif self.monster1_count > 1 and self.monster2_count ==0:
                print(f""" {self.monster1_count} {self.monster_spawning.monster1().type}S are here.""")
            elif self.monster1_count == 0 and self.monster2_count == 1:
                print(f""" A {self.monster_spawning.monster2().type} is here.""")
            elif self.monster1_count == 0 and self.monster2_count > 1:
                print(f""" {self.monster2_count} {self.monster_spawning.monster2().type}S are here.""")
            elif self.monster1_count == 1 and self.monster2_count == 1:
                print(f""" A {self.monster_spawning.monster1().type} and a {self.monster_spawning.monster2().type} are here.""")
            elif self.monster1_count == 1 and self.monster2_count > 1:
                print(f""" A {self.monster_spawning.monster1().type} and {self.monster2_count} {self.monster_spawning.monster2().type}S are here.""")
            elif self.monster1_count > 1 and self.monster2_count == 1:
                print(f""" {self.monster1_count} {self.monster_spawning.monster1().type}S and a {self.monster_spawning.monster2().type} are here.""")
            elif self.monster1_count > 1 and self.monster2_count > 1:
                print(f""" {self.monster1_count} {self.monster_spawning.monster1().type}S and {self.monster2_count} {self.monster_spawning.monster2().type}S are here.""")
            elif self.monster1_count == 0 and self.monster2_count == 0 and player_request == True: 
                print(" No monsters are here.")
    
    def room_interaction(self, player_action, player, room): #consider moving this to server.py and merging with select_sequence() for DRY
        if len(self.interactables) <= 0:
            print(f"""\n {player_action} isn't an option here. Input MENU for a list of current options.""")
        else:
            options = []
            for each_interactable in self.interactables:
                if len(each_interactable.action_words) > 0 :
                    if player_action in each_interactable.action_words:
                        options.append(each_interactable)
            if len(options) == 0:
                print(f"""\n {player_action} isn't an option here. Input MENU for a list of current options.""")
            elif len(options) == 1:
                options[0].run_interaction(player_action, player, room)
            else:
                selection_loop = True
                while selection_loop == True:
                    print(f"""\n Which {options[0].type} would you like to {player_action}?""")
                    for each_option in options:
                        print(f""" {each_option.type} {each_option.number}""")
                    print(" NEVERMIND")
                    selection = input("\n - ").upper()
                    if selection == "NEVERMIND":
                        selection_loop = False
                    for each_option in options:
                        if selection == each_option.type + " " + str(each_option.number) or selection == each_option.type + str(each_option.number):
                            each_option.run_interaction(player_action, player, room)
                            selection_loop = False
                            break
                    if selection_loop == True:
                        print(f"""\n {selection} is not an option (include the number if it has one).""")
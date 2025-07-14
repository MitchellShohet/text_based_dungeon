import random
from classes.dungeon.room_components import Exit

class Room:
    def __init__(self, name, description, exits=[Exit(0)], monster_spawning=None, interactables=[], adjustments=[[],[],{}]):
        self.name = name
        self.description = description
        self.exits = exits
        self.monster_spawning = monster_spawning
        self.monsters = []
        self.interactables = interactables
        self.visits = 0
        self.adjustments=adjustments

    def spawn_monster(self, monster_given=False):
        new_monster = None
        if monster_given == False:
            if self.monster_spawning is not None:
                monster_chance = random.randint(1, 10)
                if self.monster_spawning.threshold2 is not None and monster_chance >= self.monster_spawning.threshold2:
                    if self.monster_spawning.monster2 == "TWICE":
                        print(f""" Two new {self.monster_spawning.monster1().type}S have appeared!""")
                        self.spawn_monster(self.monster_spawning.monster1)
                        self.spawn_monster(self.monster_spawning.monster1)
                        return
                    else: 
                        print(f""" A new {self.monster_spawning.monster2().type} has appeared!""")
                        new_monster = self.monster_spawning.monster2()
                elif monster_chance >= self.monster_spawning.threshold1:
                    print(f""" A new {self.monster_spawning.monster1().type} has appeared!""")
                    new_monster = self.monster_spawning.monster1()
        else: new_monster = monster_given()
        if new_monster is not None:
            new_monster.number = sum(1 for each_monster in self.monsters if each_monster.type == new_monster.type) + 1
            self.monsters.append(new_monster)

    def view_monster_count(self, player_request=False):
        if len(self.monsters) == 0 and player_request == True: print(" No monsters are here.")
        else: 
            monster_list = []
            for each_monster in self.monsters:
                if each_monster.type not in monster_list: monster_list.append(each_monster.type)
            for each_monster_type in monster_list:
                if sum(1 for each_monster in self.monsters if each_monster.type == each_monster_type) == 1: print(f""" A {each_monster_type} is here.""")
                else: print(f""" {sum(1 for each_monster in self.monsters if each_monster.type == each_monster_type)} {each_monster_type}s are here.""")
    
    def room_interaction(self, player_action, player, room): #consider moving this to server.py and merging with select_sequence() for DRY
        if len(self.interactables) <= 0: print(f"""\n {player_action} isn't an option here. Input MENU for a list of current options.""")
        else:
            options = []
            for each_interactable in self.interactables:
                if len(each_interactable.action_words) > 0 and player_action in each_interactable.action_words: options.append(each_interactable)
            if len(options) == 0: print(f"""\n {player_action} isn't an option here. Input MENU for a list of current options.""")
            elif len(options) == 1: options[0].run_interaction(player_action, player, room)
            else:
                selection_loop = True
                while selection_loop == True:
                    if player_action == "TALK" or player_action == "SELL": print(f""" Who would you like to {player_action} to?""")
                    else: print(f""" Which would you like to {player_action}?""")
                    for each_option in options:
                        if each_option.number == 0: print(f""" {each_option.type}""")
                        else: print(f""" {each_option.type} {each_option.number}""")
                    print(" NEVERMIND")
                    selection = input("\n - ").upper()
                    if selection == "NEVERMIND": selection_loop = False
                    for each_option in options:
                        if selection == each_option.type + " " + str(each_option.number) or selection == each_option.type + str(each_option.number) or selection + "0" == each_option.type + str(each_option.number):
                            each_option.run_interaction(player_action, player, room)
                            selection_loop = False
                            break
                    if selection_loop == True: print(f"""\n {selection} is not an option (include the number if it has one).""")
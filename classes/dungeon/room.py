import random
from classes.dungeon.room_components import Exit

class Room:
    def __init__(self, name, description, exits=[Exit(0)], monster_spawning=None, interactables=[], adjustments=[[],[]]):
        self.name = name
        self.description = description
        self.exits = exits
        self.monster_spawning = monster_spawning
        self.monsters = []
        self.interactables = interactables
        self.visits = 0
        self.adjustments=adjustments

    def set_exit_link(self, number, room):
        self.exits[number].set_link(room)

    def spawn_monster(self, monster_given=False):
        new_monsters = []
        if monster_given == False and self.monster_spawning is not None:
            monster_chance = random.randint(1, 10)
            if self.monster_spawning.threshold2 is not None and monster_chance >= self.monster_spawning.threshold2:
                if self.monster_spawning.monster2 == "TWICE":
                    print(f""" Two new {self.monster_spawning.monster1().type}S have appeared!""")
                    new_monsters[0] = self.monster_spawning.monster1()
                    new_monsters[1] = self.monster_spawning.monster1()
                else: 
                    print(f""" A new {self.monster_spawning.monster2().type} has appeared!""")
                    new_monsters[0] = self.monster_spawning.monster2()
            elif monster_chance >= self.monster_spawning.threshold1:
                print(f""" A new {self.monster_spawning.monster2().type} has appeared!""")
                new_monsters[0] = self.monster_spawning.monster1()
        elif monster_given == True:
            new_monsters[0] = monster_given
        for each_monster in new_monsters:
            each_monster.number = self.monsters.count(each_monster) + 1

    def view_monster_count(self, player_request=False):
        if len(self.monsters) == 0 and player_request == True:
            print(" No monsters are here.")
        else: 
            monster_list = []
            for each_monster in range(0, len(self.monsters)):
                if each_monster not in monster_list:
                    monster_list.append(each_monster)
            for each_monster in monster_list:
                if self.monsters.count(each_monster) == 1:
                    print(f""" A {each_monster.type} is here.""")
                else:
                    print(f""" {self.monsters.count(each_monster)} {each_monster.type}s are here.""")
    
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
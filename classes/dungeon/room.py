import random
from classes.dungeon.room_components import Exit

class Room:
    def __init__(self, name, description, exits=[Exit(0)], monster_spawning=None, interactables=[]):
        self.name = name
        self.description = description
        self.exits = exits
        self.monster_spawning = monster_spawning
        self.monsters = []
        self.monster1_count = 0
        self.monster2_count = 0
        self.monster1_number = 1
        self.monster2_number = 1
        self.interactables = interactables

    def set_exit_link(self, exit_number, room):
        self.exits[exit_number].set_link(room)

    def spawn_monster(self):
        if self.monster_spawning is not None:            
            monster_chance = random.randint(1, 10)
            if self.monster_spawning.threshold2 is not None:
                if monster_chance >= self.monster_spawning.threshold2:
                    if self.monster_spawning.monster2 == "twice":
                        print(f"""\n Two new {self.monster_spawning.monster1().type}S have appeared!""")
                        first_monster1 = self.monster_spawning.monster1()
                        second_monster1 = self.monster_spawning.monster1()
                        first_monster1.number = self.monster1_number
                        second_monster1.number = self.monster1_number + 1
                        self.monsters.append(first_monster1)
                        self.monsters.append(second_monster1)
                        self.monster1_count += 2
                        self.monster1_number += 2
                    else: 
                        print(f"""\n A new {self.monster_spawning.monster2().type} has appeared!""")
                        monster = self.monster_spawning.monster2()
                        monster.number = self.monster2_number
                        self.monsters.append(monster)
                        self.monster2_count += 1
                        self.monster2_number += 1
                    monster_chance = 0
            if monster_chance >= self.monster_spawning.threshold1:
                print(f"""\n A new {self.monster_spawning.monster1().type} has appeared!""")
                monster = self.monster_spawning.monster1()
                monster.number = self.monster1_number
                self.monsters.append(monster)
                self.monster1_count += 1
                self.monster1_number += 1

    def view_monster_count(self, player_request=False):
        if self.monster_spawning is not None: 
            if self.monster1_count == 1 and self.monster2_count == 0:
                print(f"""\n A {self.monster_spawning.monster1().type} is here.""")
            elif self.monster1_count > 1 and self.monster2_count ==0:
                print(f"""\n {self.monster1_count} {self.monster_spawning.monster1().type}S are here.""")
            elif self.monster1_count == 0 and self.monster2_count == 1:
                print(f"""\n A {self.monster_spawning.monster2().type} is here.""")
            elif self.monster1_count == 0 and self.monster2_count > 1:
                print(f"""\n {self.monster2_count} {self.monster_spawning.monster2().type}S are here.""")
            elif self.monster1_count == 1 and self.monster2_count == 1:
                print(f"""\n A {self.monster_spawning.monster1().type} and a {self.monster_spawning.monster2().type} are here.""")
            elif self.monster1_count == 1 and self.monster2_count > 1:
                print(f"""\n A {self.monster_spawning.monster1().type} and {self.monster2_count} {self.monster_spawning.monster2().type}S are here.""")
            elif self.monster1_count > 1 and self.monster2_count == 1:
                print(f"""\n {self.monster1_count} {self.monster_spawning.monster1().type}S and a {self.monster_spawning.monster2().type} are here.""")
            elif self.monster1_count > 1 and self.monster2_count > 1:
                print(f"""\n {self.monster1_count} {self.monster_spawning.monster1().type}S and {self.monster2_count} {self.monster_spawning.monster2().type}S are here.""")
            elif self.monster1_count == 0 and self.monster2_count == 0 and player_request == True: 
                print("\n No monsters are here.")
    
    def room_interaction(self, player_action, player, room):
        if len(self.interactables) <= 0:
            print(f"""\n {player_action} isn't an option here. iiiiiiiiiiiiiiiiiiiiiInput MENU for a list of current options.""") #edit after testing
        else:
            is_valid = False
            for each_interactable in self.interactables:
                print(each_interactable.type)
                if len(each_interactable.action_words) > 0 :
                    print("yup")
                    for each_action_word in each_interactable.action_words:
                        print(each_action_word)
                        if player_action == each_action_word:
                            print("running")
                            each_interactable.run_interaction(player_action, player, room)
                            is_valid = True
                            break
            if is_valid == False:
                print(f"""\n {player_action} isn't an option here.2222222222222Input MENU for a list of current options.""") #edit after testing

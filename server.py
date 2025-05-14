from line_spacer import line_spacer
from classes.inventory.weapons import weapons
from classes.combatants.player_character import PlayerCharacter
from classes.combatants.monster_all.goblin import Goblin
from classes.dungeonComponents.dungeon_navigation import DungeonNavigation

is_active = True
successive_runs = []

class DungeonRun:
    def __init__(self):
        self.player_alive = True
        self.dungeon_nav = DungeonNavigation()
        self.player_character = PlayerCharacter()

    def game_start(self):
        print(f"""
            {line_spacer}
            \n Welcome to The Dungeon of Dynae! You are an explorer and must navigate through the dungeon_nav to find the Idol of Dynae and escape!
            \n To play, simply input the choice you'd like to make. You can always input MENU to see your current options.
            \n Before you can begin your journey, you must build your adventurer's stats!
            {line_spacer}""")
        self.player_character.set_player_stats()
        print(f"""\n {self.dungeon_nav.current_room.description} """)

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
            if command.upper() == "YES":
                death_loop = False
                return True

    def game_loop(self):
        while self.player_alive == True:
            command = input("\n What would you like to do? - ")
            if command.upper() == "VIEW STATS":
                self.player_character.get_player_stats()
            elif command.upper() == "FORWARD":
                try:
                    self.dungeon_nav.current_room.exits[self.dungeon_nav.test_forward()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    self.dungeon_nav.enter_room(self.dungeon_nav.test_forward())
                    print(f"""\n {self.dungeon_nav.current_room.description} """)
            elif command.upper() == "BACKWARD":
                self.dungeon_nav.enter_room(self.dungeon_nav.test_backward())
                print(f"""\n {self.dungeon_nav.current_room.description} """)
            elif command.upper() == "LEFT":
                try:
                    self.dungeon_nav.current_room.exits[self.dungeon_nav.test_left()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    self.dungeon_nav.enter_room(self.dungeon_nav.test_left())
                    print(f"""\n {self.dungeon_nav.current_room.description} """)
            elif command.upper() == "RIGHT":
                try:
                    self.dungeon_nav.current_room.exits[self.dungeon_nav.test_right()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    self.dungeon_nav.enter_room(self.dungeon_nav.test_right())
                    print(f"""\n {self.dungeon_nav.current_room.description} """)
            elif command.upper() == "TEST LEVEL UP":
                self.player_character.stat_points += 1
                self.player_character.set_player_stats()
            elif command.upper() == "TEST DAMAGE":
                command = input("damage - ")
                self.player_character.take_damage(int(command))
            elif command.upper() == "TEST HEALING":
                command = input("healing - ")
                self.player_character.recover_health(int(command))
            elif command.upper() == "TEST GOBLIN":
                goblin = Goblin()
                print("A GOBLIN is here!")
                goblin.display_stats
            elif command.upper() == "ATTACK":
                damage = self.player_character.make_attack(goblin.type, goblin.defense)
                goblin.take_damage(damage)
            elif command.upper() == "GOBLIN ATTACK":
                damage = goblin.make_attack(self.player_character.type, self.player_character.defense)
                self.player_character.take_damage(damage)
            elif command.upper() == "MENU":
                print("The MENU logic isn't written yet, this is a placeholder.")
            else:
                print("That's not an option here. Input MENU for a list of current options.") # This doesn't work yet
            if self.player_character.current_health <= 0:
                self.player_alive = False
            if self.dungeon_nav.current_room.name == "Go Home":
                print(f"""
                        \n {line_spacer}
                        \n You live out the rest of your life not dying in the dungeon_nav.
                        \n Then one day you die.
                    """)
                self.player_alive = False


while is_active == True:
    current_run = DungeonRun()
    successive_runs.append(current_run) # To save runs, this is a goal for later
    current_run.game_start()
    current_run.game_loop()
    is_active = current_run.death_sequence()
    if is_active == False:
        print( "Thanks for playing!")
from line_spacer import line_spacer
from classes.inventory.weapons import weapons
from classes.combatants.player_character import PlayerCharacter
from classes.combatants.monster_all.goblin import Goblin
from classes.dungeonComponents.dungeon import Dungeon

is_active = True
successive_runs = []

class DungeonRun:
    def __init__(self):
        self.player_alive = True
        self.dungeon = Dungeon()
        self.player_character = PlayerCharacter()

    def game_start(self):
        print(f"""
            {line_spacer}
            \n Welcome to The Dungeon of Dynae! You are an explorer and must navigate through the dungeon to find the Idol of Dynae and escape!
            \n To play, simply input the choice you'd like to make. You can always input MENU to see your current options.
            \n Before you can begin your journey, you must build your adventurer's stats!
            {line_spacer}""")
        self.player_character.set_player_stats()
        print(f"""\n {self.dungeon.current_room.description} """)

    def death_sequence(self):
        print(f"""\n {line_spacer}
            \n {line_spacer}
            \n You have died.
            \n {line_spacer}
            \n {line_spacer} """)
        death_loop = True
        while death_loop == True:
            command = input("\n RETRY? - ")
            if command == "NO":
                death_loop = False
                return False
            if command == "YES":
                death_loop = False
                return True

    def game_loop(self):
        while self.player_alive == True:
            command = input("\n What would you like to do? - ")
            if command == "VIEW STATS":
                self.player_character.get_player_stats()
            elif command == "TEST LEVEL UP":
                self.player_character.stat_points += 1
                self.player_character.set_player_stats()
            elif command == "TEST DAMAGE":
                command = input("damage - ")
                self.player_character.take_damage(int(command))
            elif command == "TEST HEALING":
                command = input("healing - ")
                self.player_character.recover_health(int(command))
            elif command == "TEST GOBLIN":
                goblin = Goblin()
                print("A GOBLIN is here!")
                goblin.display_stats
            elif command == "ATTACK":
                damage = self.player_character.make_attack(goblin.type, goblin.defense)
                goblin.take_damage(damage)
            elif command == "GOBLIN ATTACK":
                damage = goblin.make_attack(self.player_character.type, self.player_character.defense)
                self.player_character.take_damage(damage)
            else:
                print("That's not an option here. Input MENU for a list of current options.") # This doesn't work yet
            if self.player_character.current_health <= 0:
                self.player_alive = False

while is_active == True:
    current_run = DungeonRun()
    successive_runs.append(current_run) # To save runs, this is a goal for later
    current_run.game_start()
    current_run.game_loop()
    is_active = current_run.death_sequence()
    if is_active == False:
        print("Thanks for playing!")
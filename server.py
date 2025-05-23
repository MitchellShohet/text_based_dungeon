from line_spacer import line_spacer
from classes.combatants.player_character import PlayerCharacter
from classes.dungeonComponents.dungeon_navigation import DungeonNavigation

from classes.inventory.weapon import weapon_options
from classes.inventory.item import Item

class PlayThrough:
    def __init__(self):
        self.player_alive = True
        self.dungeon_nav = DungeonNavigation()
        self.player_character = PlayerCharacter()

    def game_start(self):
        print(f"""
            {line_spacer}
            \n Welcome to The Dungeon of Dynae! You are an explorer and must navigate through the dungeon to find the Idol of Dynae and escape!
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

#--This needs to be cleaned up
    def game_loop(self):
        while self.player_alive == True:
            command = input("\n What would you like to do? - ")
            if command.upper() == "VIEW STATS":
                self.player_character.get_player_stats()
            elif command.upper() == "MONSTERS":
                self.dungeon_nav.current_room.view_monster_count(True)
            elif command.upper() == "FORWARD":
                try:
                    self.dungeon_nav.current_room.exits[self.dungeon_nav.test_forward()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    if len(self.dungeon_nav.current_room.monsters) > 0:
                        for each_monster in self.dungeon_nav.current_room.monsters:
                            each_monster.notice_player(self.player_character.stealth)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                    self.dungeon_nav.enter_room(self.dungeon_nav.test_forward())
            elif command.upper() == "BACKWARD":
                if len(self.dungeon_nav.current_room.monsters) > 0:
                        for each_monster in self.dungeon_nav.current_room.monsters:
                            each_monster.notice_player(self.player_character.stealth)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                self.dungeon_nav.enter_room(self.dungeon_nav.test_backward())
            elif command.upper() == "LEFT":
                try:
                    self.dungeon_nav.current_room.exits[self.dungeon_nav.test_left()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    if len(self.dungeon_nav.current_room.monsters) > 0:
                        for each_monster in self.dungeon_nav.current_room.monsters:
                            each_monster.notice_player(self.player_character.stealth)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                    self.dungeon_nav.enter_room(self.dungeon_nav.test_left())
            elif command.upper() == "RIGHT":
                try:
                    self.dungeon_nav.current_room.exits[self.dungeon_nav.test_right()]
                except: 
                    print("There is no exit that direction.")
                else: 
                    if len(self.dungeon_nav.current_room.monsters) > 0:
                        for each_monster in self.dungeon_nav.current_room.monsters:
                            each_monster.notice_player(self.player_character.stealth)
                            if each_monster.is_aware == True:
                                each_monster.make_attack(self.player_character)
                    self.dungeon_nav.enter_room(self.dungeon_nav.test_right())
            elif command.upper() == "ATTACK":
                if len(self.dungeon_nav.current_room.monsters) == 0:
                    print("\n There are no monsters here to attack.")
                else:
                    print("\n Which monster will you attack?")
                    for each_monster in self.dungeon_nav.current_room.monsters:
                        print(f"""\n{each_monster.type} {each_monster.number}""")
                    attack_choice = input("\n - ")
                    for each_monster in self.dungeon_nav.current_room.monsters:
                        if attack_choice.upper() == each_monster.type + " " + str(each_monster.number) or attack_choice.upper() == each_monster.type + str(each_monster.number):
                            self.player_character.make_attack(each_monster)
                            if each_monster.current_health <= 0:
                                self.dungeon_nav.current_room.dead_monsters.append(each_monster)
                                self.dungeon_nav.current_room.monsters.remove(each_monster)
                                if self.dungeon_nav.current_room.monster_spawning.monster1().type == each_monster.type:
                                    self.dungeon_nav.current_room.monster1_count -= 1
                                else:
                                    self.dungeon_nav.current_room.monster2_count -= 1
                    for each_monster in self.dungeon_nav.current_room.monsters:
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
                    for each_item in self.player_character.inventory.consumables:
                        print(f"""\n {each_item.name}""")
                    item_using = input("\n Which item do you want to use?")
                    for each_item in self.player_character.inventory.consumables:
                        if each_item.name == item_using.upper():
                            #update so the item is also used not just removed
                            self.player_character.inventory.remove_item(each_item)
                            break

            elif command.upper() == "TEST ADD WEAPON":
                self.player_character.inventory.add_item(weapon_options[5])
            elif command.upper() == "TEST ADD CONSUMABLE":
                self.player_character.inventory.add_item(Item("CONSUMABLE", "APPLE", 1))
            elif command.upper() == "TEST LEVEL UP":
                self.player_character.stat_points += 1
                self.player_character.set_player_stats()
            elif command.upper() == "DIE":
                self.player_character.take_damage(int(100))
            elif command.upper() == "TEST HEALING":
                command = input("healing - ")
                self.player_character.recover_health(int(command))
            elif command.upper() == "MENU":
                print("The MENU logic isn't written yet, this is a placeholder.")
            else:
                print("That's not an option here. Input MENU for a list of current options.") # This doesn't work yet
            if self.player_character.current_health <= 0:
                self.player_alive = False
            if self.dungeon_nav.current_room.name == "Go Home":
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
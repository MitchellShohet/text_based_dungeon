from line_spacer import line_spacer
from classes.combatants.combatant import Combatant
from classes.inventory.inventory import Inventory
from lists.items_lists import weapon_options, misc_options,DurabilityGem, armor_options, SmokeBomb, HealthPotion, GreaterHealthPotion

class PlayerCharacter(Combatant):

    def __init__(self):
        self.stealth = 5 #baseline for normal mode is 1
        self.investigation = 2 #baseline for normal mode is 1
        self.stat_points = 0 #baseline for normal mode is 8
        super().__init__(
            type="PLAYER", 
            max_health=10000000, #baseline for normal mode is 10
            current_health=10000000, #baseline for normal mode is 10
            attack=5, #baseline for normal mode is 1
            defense=3, 
            inventory=Inventory(
                weapon=weapon_options["FIST"],
                armor=armor_options["CLOTHES"],
                consumables=[DurabilityGem()], #*** Update this once done testing
                misc=[misc_options["WOOD"], misc_options["WOOD"], misc_options["WOOD"], misc_options["WOOD"], misc_options["WOOD"], misc_options["WOOD"], misc_options["WOOD"], misc_options["APPLES"], armor_options["GAMBESON"], armor_options["GAMBESON"], armor_options["GAMBESON"], armor_options["GAMBESON"], armor_options["GAMBESON"], armor_options["GAMBESON"], armor_options["GAMBESON"], armor_options["GAMBESON"], armor_options["GAMBESON"], weapon_options["SHORTSWORD"], weapon_options["SHORTSWORD"], weapon_options["SHORTSWORD"], weapon_options["SHORTSWORD"], weapon_options["SHORTSWORD"], misc_options["JAW BONE"]], #*** Update this once done testing
                dollar_bills=100 #*** Update this once done testing
                )
            )
        self.hiding_score = 0
        self.hiding = False
        self.initial_setup = True

    def get_player_stats(self):
            print(f"""\n Your CURRENT HEALTH is {self.current_health}.""")
            print(f""" Your MAX HEALTH is {self.max_health}.""")
            print(f""" Your ATTACK is +{self.attack}.""")
            print(f""" Your DEFENSE is {self.defense}.""")
            print(f""" Your STEALTH is +{self.stealth}.""")
            print(f""" Your INVESTIGATION is +{self.investigation}.""")
            print(f""" Your ATTACK BUFF is +{self.attack_buff}.""")
            print(f""" Your DEFENSE BUFF is +{self.defense_buff}.""")
            print(f"""\n You have {self.stat_points} STAT POINTS to spend.""")

    def recover_health(self, amount):
        if self.current_health + amount > self.max_health: amount = self.max_health - self.current_health
        self.current_health += amount
        print(f"""\n CURRENT HEALTH increased by {amount} points.""")

    def increase_stat(self, stat_variable, increased_stat):
        print(f"""\n How many points would you like to increase {increased_stat} by?""")
        command = input("\n - ")
        try: int(command)
        except: print("\n Please input a number.")
        else: 
            command = int(command)
            if self.initial_setup == False and command < 0: print("\n STAT POINTS cannot be traded after initial character setup.") #prevents the player from gaining extra STAT POINTS by trading from other stats post game setup
            elif command > self.stat_points: print("\n You don't have that many STAT POINTS.") #prevents the player from expending more STAT POINTS then are available
            elif stat_variable + command < 1: print(f"""\n You cannot have less than 1 {increased_stat}""") #prevents the player from lowering a stat below 0
            else:
                stat_variable += command
                self.stat_points -= command
                print(f"""\n {increased_stat} increased by {command} points.""")
                if increased_stat == "MAX HEALTH":
                    self.current_health += command
                    print(f""" CURRENT HEALTH INCREASED BY {command} points. {line_spacer}""")
        return stat_variable

    def set_player_stats(self):
        self.get_player_stats()
        setting_stats = True
        while setting_stats == True:
            if self.stat_points != 0:
                print("\n What would you like to spend points on?")
                print(" MAX HEALTH")
                print(" ATTACK")
                print(" STEALTH")
                print(" INVESTIGATION")
                command = input("\n - ").upper()
                if command == "MAX HEALTH": self.max_health = self.increase_stat(self.max_health, "MAX HEALTH")
                elif command == "ATTACK": self.attack = self.increase_stat(self.attack, "ATTACK")
                elif command == "STEALTH": self.stealth = self.increase_stat(self.stealth, "STEALTH")
                elif command == "INVESTIGATION": self.investigation = self.increase_stat(self.investigation, "INVESTIGATION")
                else:
                    print("\n Sorry that isn't an option. Please select MAX HEALTH, ATTACK, STEALTH, or INVESTIGATION.")
                    print(line_spacer)
                self.get_player_stats()
            else:
                if self.initial_setup == False:
                    setting_stats = False
                    print("\n Your character has been updated! Returning to the game.")
                else:
                    print("\n Thank you for creating your character!")
                    self.get_player_stats()
                    print(line_spacer)
                    setting_stats = False
                    while self.initial_setup == True:
                            self.initial_setup = False
                            print(line_spacer)
                            print(line_spacer)
                            print(line_spacer)
    
    def equip(self, new_item):
        if new_item.type == "ARMOR":
            print(f""" equiping {new_item.name}""")
            self.inventory.misc.append(self.inventory.armor)
            self.inventory.misc.remove(new_item)
            self.inventory.armor = new_item
            self.defense = new_item.defense
        elif new_item.type == "WEAPON":
            print(f""" equiping {new_item.name}""")
            self.inventory.misc.append(self.inventory.weapon)
            self.inventory.misc.remove(new_item)
            self.inventory.weapon = new_item
        elif new_item.name == "SHIELD":
            print(" A SHIELD has been equipped")
    
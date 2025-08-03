import random
from classes.combatants.combatant import Combatant
from lists.items_lists import MagicWand

class Monster(Combatant):

    def __init__(self, type, description, max_health, current_health, attack, defense, inventory, perception, stealth_mod, attack_buff=0, defense_buff=0):
        super().__init__(type, max_health, current_health, attack, defense, inventory, attack_buff=attack_buff, defense_buff=defense_buff)
        self.description = description
        self.perception = perception
        self.is_aware = False
        self.invest_requirement = 6
        self.stealth_mod = stealth_mod
        self.action_words = []
        self.can_investigate = True

    def notice_player(self, stealth_check, player_request=False):
        print(f""" Your stealth is: {stealth_check}. {self.type} {self.number}'s perception is: {self.perception}.""")
        if stealth_check <= self.perception:
            if self.is_aware == True: print(f"""\n {self.type} {self.number} is aware of you!""")
            else: 
                self.is_aware = True
                print(f"""\n {self.type} {self.number} noticed you!""")
        elif stealth_check >= self.perception and player_request == True and self.is_aware == True:
            self.is_aware = False
            print(f"""\n {self.type} {self.number} lost you!""")
        else: print(f"""\n {self.type} {self.number} hasn't noticed you!""")
        return self.is_aware

    def investigate(self, player, room): #named like this to coincide with other interactables, but the player is the one investigating the monster here
        if player.investigation + random.randint(1,5) >= self.invest_requirement:
            if self.current_health > 0:
                print(f"""\n You were able to OBSERVE {self.type} {self.number} and glean some info about it.""")
                print(f"""\n {self.type} {self.number}'s attack is {self.attack}.""")
                print(f""" {self.type} {self.number}'s defense is {self.defense}.""")
                print(f""" {self.type} {self.number}'s health is {self.current_health}.""")
                print(f""" {self.type} {self.number}'s weapon is {self.inventory.weapon.name}.""")
                print(f""" {self.type} {self.number}'s defense buff is {self.defense_buff}.""")
                print(f""" {self.type} {self.number}'s attack buff is {self.attack_buff}.""")
            else:
                print(f"""\n You searched {self.type} {self.number} and found a {self.inventory.weapon.name}, """)
                if self.inventory.weapon.name == "MAGIC WAND": player.inventory.add_item(MagicWand())
                else: player.inventory.add_item(self.inventory.weapon)
                for each_misc in self.inventory.misc:
                    print(f""" a {each_misc.name}, """)
                    player.inventory.add_item(each_misc)
                for each_consumable in self.inventory.consumables:
                    print(f""" a {each_consumable.name}, """)
                    player.inventory.add_item(each_consumable)
                print(f""" and {self.inventory.dollar_bills} dollar bills.""")
                player.inventory.dollar_bills += self.inventory.dollar_bills
                self.can_investigate = False
        else:
            print(f"""\n You investigated {self.type} {self.number}, there wasn't much to find.""")
            self.can_investigate = False
        




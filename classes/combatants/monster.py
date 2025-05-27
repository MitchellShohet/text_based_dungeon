import random
from classes.combatants.combatant import Combatant

class Monster(Combatant):

    def __init__(self, type, description, max_health, current_health, attack, defense, inventory, perception, stealth_mod):
        super().__init__(type, max_health, current_health, attack, defense, inventory)
        self.description = description
        self.perception = perception
        self.is_aware = False
        self.invest_requirement = 5
        self.stealth_mod = stealth_mod
        self.can_investigate = True
        self.action_words = None

    def display_stats(self):
        print(f"""\n The {self.type}'S attack is {self.attack}.
            \n The {self.type}'S defense is {self.defense}.
            \n The {self.type}'S health is {self.health}.
            \n The {self.type}'S weapon is {self.inventory["weapon"]["type"]}.
            """)

    def notice_player(self, stealth_check, player_request=False):
        print(f"""\n stealth: {stealth_check}. Perception: {self.perception}.""")
        if stealth_check <= self.perception:
            self.is_aware = True
            print(f"""\n {self.type} {self.number} noticed you!""")
        elif stealth_check >= self.perception and player_request == True and self.is_aware == True:
            self.is_aware = False
            print(f"""\n {self.type} {self.number} lost you!""")
        else:
            print(f"""\n {self.type} {self.number} hasn't noticed you!""")
        return self.is_aware

    def investigate(self, player):
        if player.investigation + random.randint(1,5) >= self.invest_requirement:
            print(f"""\n You searched {self.type} {self.number} and found a {self.inventory.weapon.name}, """)
            player.inventory.misc.append(self.inventory.weapon)
            for each_misc in self.inventory.misc:
                print(f"""a {each_misc.name}, """)
                player.inventory.misc.append(each_misc)
            if len(self.inventory.consumables) > 0:
                for each_consumable in self.inventory.consumables:
                    print(f"""a {each_consumable.name}, """)
                    player.inventory.misc.append(each_consumable)
            print(f""" and {self.inventory.dollar_bills} dollar bills.""")
            player.inventory.dollar_bills += self.inventory.dollar_bills
        else:
            print(f"""\n You searched {self.type} {self.number}, there wasn't much to find.""")
        self.invest_requirement = 1000
        self.can_investigate = False
        




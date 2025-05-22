import random
from classes.combatants.combatant import Combatant

class Monster(Combatant):

    def __init__(self, type, description, max_health, current_health, attack, defense, inventory, perception):
        super().__init__(type, max_health, current_health, attack, defense, inventory)
        self.description = description
        self.perception = perception
        self.is_aware = False

    def display_stats(self):
        print(f"""\n The {self.type}'S attack is {self.attack}.
            \n The {self.type}'S defense is {self.defense}.
            \n The {self.type}'S health is {self.health}.
            \n The {self.type}'S weapon is {self.inventory["weapon"]["type"]}.
            """)

    def notice_player(self, stealth):
        stealth_check = stealth + random.randint(1,5)
        print(f"""\n stealth: {stealth_check}. Perception: {self.perception}.""")
        if stealth_check < self.perception:
            self.is_aware = True
            print(f"""\n {self.type} {self.number} noticed you!""")
        return self.is_aware


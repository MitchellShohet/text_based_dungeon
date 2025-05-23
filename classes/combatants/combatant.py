import random
from line_spacer import line_spacer

class Combatant:

    def __init__(self, type, max_health, current_health, attack, defense, inventory):
        self.type = type
        self.number = 0
        self.max_health = max_health
        self.current_health = current_health
        self.attack = attack
        self.defense = defense
        self.inventory = inventory

    def make_attack(self, defender):
        attack_roll = random.randint(int(self.inventory.weapon.attack_odds1), int(self.inventory.weapon.attack_odds2)) + self.attack
        if self.type == "PLAYER":
            print(f"""\n You attacked the {defender.type} with {attack_roll} attack!""")
        else:
            print(f"""\n {self.type} {self.number} attacked with {attack_roll} attack!""")
        if attack_roll >= defender.defense:
            print(f"""\n THE ATTACK HITS!""")
            damage = random.randint(int(self.inventory.weapon.damage_odds1), int(self.inventory.weapon.damage_odds2)) + self.attack
            print(f"""\n The attack deals {damage} damage!""")
        else:
            print("\n The attack misses!")
            damage = 0
        defender.take_damage(damage)

    def take_damage(self, incoming_damage):
        self.current_health -= incoming_damage
        if self.current_health < 0:
            if self.type != "PLAYER":
                print(f"""{self.type} {self.number} has died.""")
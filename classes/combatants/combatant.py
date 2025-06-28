import random
from line_spacer import line_spacer
from lists.items_lists import misc_options

class Combatant:

    def __init__(self, type, max_health, current_health, attack, defense, inventory, number="", attack_buff=0, defense_buff=0):
        self.type = type
        self.number = number
        self.max_health = max_health
        self.current_health = current_health
        self.attack = attack
        self.defense = defense
        self.inventory = inventory
        self.attack_buff = attack_buff
        self.defense_buff = defense_buff

    def make_attack(self, defender):
        attack_roll = random.randint(int(self.inventory.weapon.attack_odds1), int(self.inventory.weapon.attack_odds2)) + self.attack + self.attack_buff
        if misc_options["SHIELD"] in defender.inventory.misc: defender.defense_buff += 1
        if self.type == "PLAYER": print(f""" You attacked the {defender.type} with {attack_roll} attack!""")
        else:
            if self.attack_buff == 5: print(f""" {self.type} {self.number} casts FIREBALL!""")
            print(f""" {self.type} {self.number} attacked with {attack_roll} attack!""")
        if attack_roll >= defender.defense + defender.defense_buff:
            print(f""" THE ATTACK HITS!""")
            damage = random.randint(int(self.inventory.weapon.damage_odds1), int(self.inventory.weapon.damage_odds2)) + self.attack + self.attack_buff
            print(f""" The attack deals {damage} damage!""")
        else:
            if defender.defense_buff == 5: print(f""" {defender.type} {defender.number} casts SHIELD SPELL!""")
            print(" The attack misses!")
            damage = 0
        defender.take_damage(damage)
        self.attack_buff = 0
        defender.defense_buff = 0

    def take_damage(self, incoming_damage, print_damage=False):
        self.current_health -= incoming_damage
        if self.current_health <= 0 and self.type != "PLAYER":
            if self.type == "GLOWING CRYSTAL" or self.type == "THE LOCK" or self.type == "TREE": print(f""" {self.type} {self.number} has been destroyed.""")
            else: print(f""" {self.type} {self.number} has died.""")
        if print_damage == True and self.type == "PLAYER": print(f""" You took {incoming_damage} damage!""")
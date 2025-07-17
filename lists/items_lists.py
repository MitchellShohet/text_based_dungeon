import random
from classes.inventory.items import Item, Weapon, Armor, Consumable
from abc import ABC

#---------------------------------------------

weapon_options = {
    "FIST" : Weapon(1, "WEAPON", "FIST", 1, 3, 1, 1, 0),
    "CLUB" : Weapon(2, "WEAPON", "CLUB", 1, 7, 1, 3, 1),
    "GOLEM FIST" : Weapon(3, "WEAPON", "GOLEM FIST", 2, 8, 0, 2, 25),
    "SHORTSWORD" : Weapon(4, "WEAPON", "SHORTSWORD", 2, 8, 1, 4, 7),
    "TRIDENT" : Weapon(5, "WEAPON", "TRIDENT", 2, 9, 2, 4, 24),
    "MIMIC TOOTH" : Weapon(5, "WEAPON", "MIMIC TOOTH", 2, 9, 2, 4, 24),
    "LONGSWORD" : Weapon(6, "WEAPON", "LONGSWORD", 3, 9, 2, 4, 55),
    "BATTLE AXE" : Weapon(7, "WEAPON", "BATTLE AXE", 3, 10, 3, 6, 80),
    "MAGIC SWORD" : Weapon(8, "WEAPON", "MAGIC SWORD", 4, 12, 3, 9, 120),
    "MAGIC WAND" : Weapon(0, "WEAPON", "MAGIC WAND", 1, 7, 1, 4, 0)
}

#----------------------------------------------

armor_options = {
    "CLOTHES" : Armor(1, "ARMOR", "CLOTHES", 3, 1),
    "GAMBESON" : Armor(2, "ARMOR", "GAMBESON", 5, 12),
    "CHAINMAIL" : Armor(3, "ARMOR", "CHAINMAIL", 7, 35),
    "PLATEMAIL" : Armor(4, "ARMOR", "PLATEMAIL", 9, 100), #don't sell platemail in regular shops
    "MAGIC PLATE" : Armor(5, "ARMOR", "MAGIC PLATE", 12, 250)
}

#---------------------------------------------

misc_options = {
    "BLADE OF GRASS": Item("MISC", "BLADE OF GRASS", 0),
    "WOOD" : Item("MISC", "WOOD", 1),
    "GOBLIN HORN" : Item("MISC", "GOBLIN HORN", 3),
    "NOT ENOUGH APPLES" : Item("MISC", "NOT ENOUGH APPLES", 0),
    "APPLES": Item("MISC", "APPLES", 3),
    "JAW BONE" : Item("MISC", "JAW BONE", 5),
    "GLOWING FRUIT" : Item("MISC", "GLOWING FRUIT", 10),
    "SEA CREATURE MEAT" : Item("MISC", "SEA CREATURE MEAT", 12),
    "KEY" : Item("MISC", "KEY", 20),
    "RUBY DUST" : Item("MISC", "RUBY DUST", 20),
    "GOLEM EYE" : Item("MISC", "GOLEM EYE", 20),
    "MINOTAUR HORN" : Item("MISC", "MINOTAUR HORN", 30),
    "SHIELD" : Item("MISC", "SHIELD", 35),
    "MAGIC BRIDGE": Item("MISC", "MAGIC BRIDGE", 50)
}

#-------------------
#CONSUMABLE OPTIONS
#-------------------

class HealingItem(Consumable, ABC):
    def __init__(self, name, description, value, healing):
        self.healing = healing
        super().__init__(name, description, value=value, is_healing=True)

    def effect(self, player_character):
        print(f"""\n You used the {self.name}!""")
        player_character.recover_health(self.healing)

#------------------------------------------------------------------------------------

class HealthPotion(HealingItem):
    def __init__(self):
        super().__init__(
            name="HEALTH POTION",
            description="A small vial with a red liquid; it smells of cherries. Using will heal between 5-7 health.",
            value=10,
            healing=random.randint(5,7)
        )

#------------------------------------------------------------------------------------

class GreaterHealthPotion(HealingItem):
    def __init__(self):
        super().__init__(
            name="GREATER HEALTH POTION",
            description="A small vial with a pink liquid; it smells of fresh sourdough. Using will heal between 10-15 health.",
            value=20,
            healing=random.randint(10,15)
        )

#------------------------------------------------------------------------------------

class Pie(HealingItem):
    def __init__(self):
        super().__init__(
            name="PIE",
            description="A nicely baked pie, can be made from a variety of ingredients. Using will heal between 7-10 health.",
            value=16,
            healing=random.randint(7,10)
        )

#------------------------------------------------------------------------------------

class StatMedallion(Consumable):
    def __init__(self):
        super().__init__(
            name="STAT MEDALLION",
            description="A lime-green coin that's warm to the touch. Using will allow you to increase your stats by 2 points.",
            value=46
        )

    def effect(self, player_character):
        print(f"""\n You used the {self.name}!""")
        player_character.stat_points += 2
        player_character.set_player_stats()

#------------------------------------------------------------------------------------

class PowerBerry(Consumable):
    def __init__(self):
        super().__init__(
            name="POWER BERRY",
            description="A massive berry the size of a fist; yet light, like eating a cloud. Using will give a bonus +3 to your next attack and the damage if that attack hits (does not stack).",
            value=5
        )

    def effect(self, player_character):
        print(f"""\n You used the {self.name}!""")
        print(" ATTACK AND DAMAGE increased by 3 for your next attack.")
        player_character.attack_buff = 3

#------------------------------------------------------------------------------------

class DurabilityGem(Consumable):
    def __init__(self):
        super().__init__(
            name="DURABILITY GEM",
            description="A small, sharp, ceramic gemestone. Using will give a bonus +3 to your defense against the next attack against you (does not stack).",
            value=8
        )

    def effect(self, player_character):
        print(f"""\n You used the {self.name}!""")
        print(" DEFENSE increased by 3 for the next attack.")
        player_character.defense_buff = 3

#------------------------------------------------------------------------------------

class SmokeBomb(Consumable):
    def __init__(self):
        super().__init__(
            name = "SMOKE BOMB",
            description = "A round clump of a charcoal-like substance. Using will give a bonus +3 to your stealth until you leave the current room.",
            value = 9
        )

    def effect(self, player_character):
        print(f"""\n You used the {self.name}!""")
        print(f""" previous hiding score: {player_character.hiding_score}.""")
        player_character.hiding_score += 3
        print(f""" new hiding score: {player_character.hiding_score}""")

#------------------------------------------------------------------------------------

class MagicWand(Consumable):
    def __init__(self):
        super().__init__(
            name="MAGIC WAND",
            description="A Stick made out of wood- no wait, metal? Clay? It's hard to tell but using will give a bonus +2 to your next attack, the damage if that attack hits, and your defense for the next attack against you (These do not stack with other items with similar effects).",
            value=13
        )

    def effect(self, player_character):
        print(f"""\n You used the {self.name}!""")
        print(" ATTACK and DAMAGE increased by 2 for your next attack, and DEFENSE increased by 2 for the next attack")
        player_character.attack_buff = 2
        player_character.defense_buff = 2
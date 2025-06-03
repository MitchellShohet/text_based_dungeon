import random
from classes.inventory.items import Item, Weapon, Armor, Consumable

#---------------------------------------------

#These all *should* be fine as dictionary elements. If problems with multiples arise, each might need to be it's own class.

weapon_options = {
    "FIST" : Weapon(1, "WEAPON", "FIST", 1, 2, 1, 1, 0),
    "CLUB" : Weapon(2, "WEAPON", "CLUB", 1, 5, 1, 3, 1),
    "GOLEM FIST" : Weapon(3, "WEAPON", "GOLEM FIST", 2, 6, 1, 3, 25),
    "SHORTSWORD" : Weapon(4, "WEAPON", "SHORTSWORD", 2, 6, 1, 4, 7),
    "LONGSWORD" : Weapon(5, "WEAPON", "LONGSWORD", 2, 8, 2, 4, 30),
    "BATTLE AXE" : Weapon(6, "WEAPON", "BATTLE AXE", 3, 9, 3, 6, 80),
    "MAGIC SWORD" : Weapon(7, "WEAPON", "MAGIC SWORD", 4, 11, 3, 9, 120),
    "MAGIC WAND" : Weapon(0, "WEAPON", "MAGIC WAND", 1, 6, 1, 4, 0)
}

#----------------------------------------------

armor_options = {
    "CLOTHES" : Armor(1, "ARMOR", "CLOTHES", 3, 1),
    "GAMBESON" : Armor(2, "ARMOR", "GAMBESON", 5, 12),
    "CHAINMAIL" : Armor(3, "ARMOR", "CHAINMAIL", 7, 35),
    "PLATE" : Armor(4, "ARMOR", "PLATE", 9, 100),
    "MAGIC PLATE" : Armor(5, "ARMOR", "MAGIC PLATE", 12, 250)
}

#---------------------------------------------

misc_options = {
    "GOBLIN HORN" : Item("MISC", "GOBLIN HORN", 3),
    "BLADE OF GRASS": Item("MISC", "BLADE OF GRASS", 0),
    "JAW BONE" : Item("MISC", "JAW BONE", 5),
    "RUBY DUST" : Item("MISC", "RUBY DUST", 20),
    "PAIR OF GOLEM EYES" : Item("MISC", "PAIR OF GOLEM EYES", 20),
    "MINOTAUR HORN" : Item("MISC", "MINOTAUR HORN", 30),
    "SHIELD" : Item("MISC", "SHIELD", 35),
}

#-------------------
#CONSUMABLE OPTIONS
#-------------------

class HealthPotion(Consumable):
    def __init__(self):
        self.name = "HEALTH POTION"
        self.description = "A small vial with a red liquid; it smells of cherries. Using will heal between 5-7 health."
        self.value = 14
        super().__init__(
            name=self.name,
            description=self.description,
            value=self.value
        )

    def effect(player_character):
        amount_healed = random.randint(5,7)
        if player_character.current_health + amount_healed > player_character.max_health:
            player_character.current_health = player_character.max_health
        else:
            player_character.current_health += amount_healed

#------------------------------------------------------------------------------------

class StatMedallion(Consumable):
    def __init__(self):
        self.name = "STAT MEDALLION"
        self.description = "A lime-green coin that's warm to the touch. Using will allow you to increase your stats by 2 points."
        self.value = 40
        super().__init__(
            name=self.name,
            description=self.description,
            value=self.value
        )

    def effect(player_character):
        player_character.stat_points += 2
        player_character.set_player_stats()

#------------------------------------------------------------------------------------

class PowerBerry(Consumable):
    def __init__(self):
        self.name = "POWER BERRY"
        self.description = "A massive berry the size of a fist; yet light, like eating a cloud. Using will give a bonus +3 to your next attack and the damage if that attack hits."
        self.value = 9
        super().__init__(
            name=self.name,
            description=self.description,
            value=self.value
        )

    def effect(player_character):
        player_character.attack_buff = 3

#------------------------------------------------------------------------------------

class DurabilityGem(Consumable):
    def __init__(self):
        self.name = "DURABILITY GEM"
        self.description = "A small, sharp, ceramic gemestone. Using will give a bonus +3 to your defense against the next attack against you."
        self.value = 13
        super().__init__(
            name=self.name,
            description=self.description,
            value=self.value
        )

    def effect(player_character):
        player_character.defense_buff = 3

#------------------------------------------------------------------------------------

class SmokeBomb(Consumable):
    def __init__(self):
        self.name = "SMOKE BOMB"
        self.description = "A round clump of a charcoal-like substance. Using will give a bonus +3 to your stealth until you leave the current room."
        self.value = 13
        super().__init__(
            name=self.name,
            description=self.description,
            value=self.value
        )

    def effect(player_character):
        print(f"""\n random number: {player_character.hiding_score}""")
        player_character.hiding_score += 3
        print(f"""\n new hiding score: {player_character.hiding_score}""")

#------------------------------------------------------------------------------------

class GreaterHealthPotion(Consumable):
    def __init__(self):
        self.name = "GREATER HEALTH POTION"
        self.description = "A small vial with a pink liquid; it smells of fresh sourdough. Using will heal between 10-15 health."
        self.value = 26
        super().__init__(
            name=self.name,
            description=self.description,
            value=self.value
        )

    def effect(player_character):
        amount_healed = random.randint(10,15)
        if player_character.current_health + amount_healed > player_character.max_health:
            player_character.current_health = player_character.max_health
        else:
            player_character.current_health += amount_healed

#------------------------------------------------------------------------------------

class MagicWand(Consumable):
    def __init__(self):
        self.name = "MAGIC WAND"
        self.description = "A Stick made out of wood- no wait, metal? Clay? It's hard to tell but using will give a bonus +2 to your next attack, the damage if that attack hits, and your defense for the next attack against you (These do not stack with other items with similar effects)."
        self.value = 18
        super().__init__(
            name=self.name,
            description=self.description,
            value=self.value
        )

    def effect(player_character):
        player_character.attack_buff = 2
        player_character.damage_buff = 2
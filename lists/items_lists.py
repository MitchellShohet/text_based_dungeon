import random
from classes.inventory.items import Item, Weapon, Armor, Consumable

#---------------------------------------------

weapon_options = {
    "FIST" : Weapon(1, "WEAPON", "FIST", 1, 2, 1, 1, 0),
    "CLUB" : Weapon(2, "WEAPON", "CLUB", 1, 5, 1, 3, 0),
    "SHORTSWORD" : Weapon(3, "WEAPON", "SHORTSWORD", 2, 6, 1, 4, 4),
    "LONGSWORD" : Weapon(4, "WEAPON", "LONGSWORD", 2, 8, 2, 4, 12),
    "BATTLE AXE" : Weapon(5, "WEAPON", "BATTLE AXE", 3, 9, 3, 6, 25),
    "MAGIC SWORD" : Weapon(6, "WEAPON", "MAGIC SWORD", 4, 11, 3, 9, 120),
}

#----------------------------------------------

armor_options = {
    "CLOTHES" : Armor(1, "ARMOR", "CLOTHES", 3, 1),
    "GAMBESON" : Armor(2, "ARMOR", "GAMBESON", 5, 12),
    "CHAINMAIL" : Armor(3, "ARMOR", "CHAINMAIL", 7, 30),
    "PLATE" : Armor(4, "ARMOR", "PLATE", 9, 100),
    "MAGIC PLATE" : Armor(5, "ARMOR", "MAGIC PLATE", 12, 350)
}

#---------------------------------------------

misc_options = {
    "GOBLIN HORN" : Item("MISC", "GOBLIN HORN", 2),
    "BLADE OF GRASS": Item("MISC", "BLADE OF GRASS", 0),
    "SHIELD" : Item("MISC", "SHIELD", 35)
}

#-------------------
#CONSUMABLE OPTIONS
#-------------------

class HealthPotion(Consumable):
    def __init__(self):
        self.name = "HEALTH POTION"
        self.description = "A small vial with a red liquid; it smells of cherries. Using will heal between 5-7 health."
        self.value = 12
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
        self.value = 35
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
        self.value = 7
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
        self.value = 10
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
        self.value = 10
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
        self.value = 20
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
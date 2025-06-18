from abc import ABC, abstractmethod

class Item:

    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value

#------------------------------------------------

class Armor(Item):

    def __init__(self, rating, type, name, defense, value):
        super().__init__(type, name, value)
        self.rating = rating
        self.defense = defense

#------------------------------------------------

class Weapon(Item):

    def __init__(self, rating, type, name, attack_odds1, attack_odds2, damage_odds1, damage_odds2, value):
        super().__init__(type, name, value)
        self.rating = rating
        self.attack_odds1 = attack_odds1
        self.attack_odds2 = attack_odds2
        self.damage_odds1 = damage_odds1
        self.damage_odds2 = damage_odds2

#--------------------------------------------------

class Consumable(Item, ABC):

    def __init__(self, name, description, value, is_healing=False):
        self.type = "CONSUMABLE"
        self.description = description
        self.is_healing = is_healing
        super().__init__(
            type=self.type,
            name=name, 
            value=value
            )

    @abstractmethod
    def effect(player_character):
        pass

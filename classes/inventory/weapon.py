from classes.inventory.item import Item

class Weapon(Item):

    def __init__(self, rating, type, name, attack_odds1, attack_odds2, damage_odds1, damage_odds2, value):
        super().__init__(type, name, value)
        self.rating = rating
        self.attack_odds1 = attack_odds1
        self.attack_odds2 = attack_odds2
        self.damage_odds1 = damage_odds1
        self.damage_odds2 = damage_odds2

weapon_options = [
    Weapon(1, "WEAPON", "Fist", 1, 2, 1, 1, 0),
    Weapon(2, "WEAPON", "Club", 1, 5, 1, 3, 0),
    Weapon(3, "WEAPON", "Shortsword", 2, 6, 1, 4, 4),
    Weapon(4, "WEAPON", "Longsword", 2, 8, 2, 4, 12),
    Weapon(5, "WEAPON", "Battle Axe", 3, 9, 3, 6, 25),
    Weapon(6, "WEAPON", "Magic Sword", 4, 11, 3, 9, 120),
]
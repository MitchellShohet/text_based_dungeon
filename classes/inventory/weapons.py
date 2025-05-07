class Weapon:

    def __init__(self, type, attack_odds1, attack_odds2, damage_odds1, damage_odds2):
        self.type = type
        self.attack_odds1 = attack_odds1
        self.attack_odds2 = attack_odds2
        self.damage_odds1 = damage_odds1
        self.damage_odds2 = damage_odds2

weapons = [
    Weapon("Fist", 1, 2, 1, 1),
    Weapon("Club", 1, 3, 1, 2),
    Weapon("Shortsword", 1, 4, 1, 3),
    Weapon("Longsword", 1, 5, 1, 4),
    Weapon("Battle Axe", 1, 6, 2, 4),
    Weapon("Magic Sword", 2, 6, 3, 5),
]
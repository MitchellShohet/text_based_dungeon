from classes.inventory.item import Item

class Armor(Item):

    def __init__(self, type, name, defense, value):
        super().__init__(type, name, value)
        self.defense = defense

armor_options = [
    Armor("ARMOR", "Clothes", 3, 1),
    Armor("ARMOR", "Gambeson", 5, 12),
    Armor("ARMOR", "Chainmail", 6, 25),
    Armor("ARMOR", "Plate", 8, 50),
    Armor("ARMOR", "Magic Plate", 11, 120)
]
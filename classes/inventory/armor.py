from classes.inventory.item import Item

class Armor(Item):

    def __init__(self, type, name, defense, value):
        super().__init__(type, name, value)
        self.defense = defense

armor_options = [
    Armor("ARMOR", "Clothes", 3, 1),
    Armor("ARMOR", "Gambeson", 5, 12),
    Armor("ARMOR", "Chainmail", 7, 30),
    Armor("ARMOR", "Plate", 9, 100),
    Armor("ARMOR", "Magic Plate", 12, 350)
]
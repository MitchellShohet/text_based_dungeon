from classes.inventory.item import Item

class Armor(Item):

    def __init__(self, rating, type, name, defense, value):
        super().__init__(type, name, value)
        self.rating = rating
        self.defense = defense
    

armor_options = [
    Armor(1, "ARMOR", "Clothes", 3, 1),
    Armor(2, "ARMOR", "Gambeson", 5, 12),
    Armor(3, "ARMOR", "Chainmail", 7, 30),
    Armor(4, "ARMOR", "Plate", 9, 100),
    Armor(5, "ARMOR", "Magic Plate", 12, 350)
]
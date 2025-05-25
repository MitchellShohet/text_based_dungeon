from classes.inventory.item import Item
from abc import ABC, abstractmethod

class Consumable(Item, ABC):

    def __init__(self, name, description, value):
        self.type = "CONSUMABLE"
        self.description = description
        super().__init__(
            name, 
            value, 
            type=self.type
            )

    @abstractmethod
    def effect(player_character):
        pass
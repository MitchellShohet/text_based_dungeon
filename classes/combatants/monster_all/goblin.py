from classes.inventory.inventory import Inventory
from classes.inventory.weapon import weapon_options
from classes.inventory.item import Item
from classes.inventory.consumables_list import HealthPotion, StatMedallion, SmokeBomb, DurabilityGem, PowerBerry
from classes.combatants.monster_all.monster import Monster
import random

class Goblin(Monster):
    def __init__(self):
        self.difficulty = random.randint(3,5)
        if self.difficulty == 3:
            self.attack = 0
        else:
            self.attack = 1 
        super().__init__(
            type="GOBLIN", 
            max_health=self.difficulty,
            current_health=self.difficulty,
            attack=self.attack,
            defense=self.difficulty, 
            perception=3 + self.difficulty,
            stealth_mod=1,
            description="lil gross potato",
            inventory=Inventory(weapon=weapon_options[1],
                consumables=[HealthPotion(), StatMedallion(), SmokeBomb(), DurabilityGem(), PowerBerry()],
                misc=[Item("MISC", "Goblin Horn", 2), Item("MISC", "Grass", 0)], #*** Make sure to update
                dollar_bills=self.difficulty-3
                )
            )


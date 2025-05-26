from classes.inventory.inventory import Inventory
from classes.inventory.weapon import weapon_options
from classes.combatants.monster_all.monster import Monster
import random

class Skeleton(Monster):
    def __init__(self):
        self.difficulty = random.randint(5,6)
        super().__init__(
            type="SKELETON", 
            max_health=self.difficulty+2,
            current_health=self.difficulty+2,
            attack=2,
            defense=self.difficulty+1, 
            perception=self.difficulty,
            stealth_mod=1,
            description="Walkin', talkin', weapon-swingin' jumble of bones. Minus the talkin'.",
            inventory=Inventory(
                weapon_options[2],
                consumables=[],  #*** Make sure to update once you build consumable options
                misc=[], #*** Make sure to update
                dollar_bills=self.difficulty-1
                )
            )
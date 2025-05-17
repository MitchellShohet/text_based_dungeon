from classes.inventory.weapons import weapons
from classes.combatants.monster_all.monster import Monster
import random

class Skeleton(Monster):
    def __init__(self):
        self.difficulty = random.randint(4,5)
        super().__init__(
            type="SKELETON", 
            max_health=self.difficulty,
            current_health=self.difficulty,
            attack=1,
            defense=self.difficulty, 
            perception= 4,
            description="Walkin', talkin', weapon-swingin' jumble of bones. Minus the talkin'.",
            inventory={"weapon" : weapons[2],
                    "armor" : "none",
                    "items" : [],  #*** Make sure to update once you build inventory options
                    "consumables" : [],  #*** Make sure to update once you build inventory options
                    }
            )
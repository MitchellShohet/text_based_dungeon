from classes.inventory.weapons import weapons
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
            description="lil gross potato",
            inventory={"weapon" : weapons[1],
                    "armor" : "none",
                    "items" : [],  #*** Make sure to update once you build inventory options
                    "consumables" : [],  #*** Make sure to update once you build inventory options
                    }
            )


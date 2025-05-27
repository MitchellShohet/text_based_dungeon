import random
from classes.inventory.inventory import Inventory
from classes.combatants.monster import Monster
from lists.items_lists import weapon_options, misc_options, HealthPotion, StatMedallion, SmokeBomb, DurabilityGem, PowerBerry

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
            description="Lil gross potato",
            inventory=Inventory(weapon=weapon_options["CLUB"],
                consumables=[HealthPotion(), StatMedallion(), SmokeBomb(), DurabilityGem(), PowerBerry()],
                misc=[misc_options["GOBLIN HORN"], misc_options["BLADE OF GRASS"]],
                dollar_bills=self.difficulty-3
                )
            )

#-------------------------------------------------------------

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
                weapon=weapon_options["SHORTSWORD"],
                consumables=[],  #*** Make sure to update once you build consumable options
                misc=[], #*** Make sure to update
                dollar_bills=self.difficulty-1
                )
            )
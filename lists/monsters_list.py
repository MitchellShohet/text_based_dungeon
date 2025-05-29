import random
from classes.inventory.inventory import Inventory
from classes.combatants.monster import Monster
from lists.items_lists import weapon_options, armor_options, misc_options, HealthPotion, StatMedallion, SmokeBomb, DurabilityGem, PowerBerry, GreaterHealthPotion

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
            perception=self.difficulty+self.attack,
            stealth_mod=1,
            description="Lil gross potato",
            inventory=Inventory(weapon=weapon_options["CLUB"],
                consumables=[HealthPotion(), StatMedallion(), SmokeBomb(), DurabilityGem(), PowerBerry()], #*** Update when done testing
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
            perception=self.difficulty+2,
            stealth_mod=1,
            description="Walkin', talkin', weapon-swingin' jumble of bones. Minus the talkin'.",
            inventory=Inventory(
                weapon=weapon_options["SHORTSWORD"],
                misc=[misc_options["JAW BONE"]],
                dollar_bills=self.difficulty-1
                )
            )

#-------------------------------------------------------------

class Wizard(Monster):
    def __init__(self):
        self.difficulty = random.randint(5,6)
        if self.difficulty == 5:
            self.attack = 2
        else:
            self.attack = 3 
        super().__init__(
            type="WIZARD", 
            max_health=self.difficulty-1,
            current_health=self.difficulty-1,
            attack=self.attack,
            defense=self.difficulty-2, 
            perception=self.difficulty+4,
            stealth_mod=2,
            description="Weird old person with magical abilities.",
            inventory=Inventory(weapon=weapon_options["MAGIC WAND"],
                consumables=[HealthPotion(), SmokeBomb()],
                misc=[misc_options["RUBY DUST"]],
                dollar_bills=self.difficulty+5
                ),
            attack_buff=5,
            defense_buff=5
            )

#-------------------------------------------------------------

class  MudGolem(Monster):
    def __init__(self):
        self.difficulty = random.randint(5,6)
        super().__init__(
            type="MUD GOLEM", 
            max_health=self.difficulty*10,
            current_health=self.difficulty*10,
            attack=3,
            defense=self.difficulty+2, 
            perception=self.difficulty+2,
            stealth_mod=5,
            description="A massive construct of hardened mud. Two piercing green marbles form its eyes, eminating magical energy. The smell is putrid.",
            inventory=Inventory(
                weapon=weapon_options["GOLEM FIST"],
                consumables=[GreaterHealthPotion()], 
                misc=[misc_options["PAIR OF GOLEM EYES"]], 
                dollar_bills=self.difficulty+5
                )
            )

#-------------------------------------------------------------

class  Minotaur(Monster):
    def __init__(self):
        self.difficulty = random.randint(7,9)
        super().__init__(
            type="MINOTAUR", 
            max_health=self.difficulty*4,
            current_health=self.difficulty*4,
            attack=4,
            defense=self.difficulty+1, 
            perception=self.difficulty+6,
            stealth_mod=5,
            description="12 feet tall, half-man, half bull. No joke.",
            inventory=Inventory(
                weapon=weapon_options["BATTLE AXE"],
                consumables=[GreaterHealthPotion(), PowerBerry(), StatMedallion()], 
                misc=[misc_options["MINOTAUR HORN"]],
                dollar_bills=self.difficulty+5
                )
            )

#----------------------------------------------------------------

class  Avatar(Monster):
    def __init__(self):
        self.difficulty = 12
        super().__init__(
            type="AVATAR OF DYNAE", 
            max_health=80,
            current_health=80,
            attack=4,
            defense=self.difficulty, 
            perception=self.difficulty+6,
            stealth_mod=7,
            description="An monsterous abomination. A snake creature with 7 heads, waves of electrical energy surge around its form.",
            inventory=Inventory(
                weapon=weapon_options["MAGIC SWORD"],
                consumables=[GreaterHealthPotion(), PowerBerry(), StatMedallion()],
                misc=[armor_options["MAGIC PLATE"]],
                dollar_bills=self.difficulty+5
                )
            )
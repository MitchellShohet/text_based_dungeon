import random
from classes.inventory.inventory import Inventory
from classes.combatants.monster import Monster
from lists.items_lists import weapon_options, armor_options, misc_options, HealthPotion, StatMedallion, SmokeBomb, DurabilityGem, PowerBerry, GreaterHealthPotion, MagicWand

class Goblin(Monster):
    def __init__(self, type="GOBLIN", descriptor="", defense_buff=0):
        self.difficulty = random.randint(3,5)
        if self.difficulty == 3: self.attack = 0
        else: self.attack = 1 
        super().__init__(
            type=type, 
            max_health=self.difficulty,
            current_health=self.difficulty,
            attack=self.attack+1,
            defense=self.difficulty, 
            perception=self.difficulty+1,
            stealth_mod=1,
            description="Lil gross potato" + descriptor,
            inventory=Inventory(weapon=weapon_options["CLUB"],
                consumables=[],
                misc=[misc_options["GOBLIN HORN"], misc_options["BLADE OF GRASS"]],
                dollar_bills=self.difficulty-3
                )
            )

#-------------------------------------------------------------

class Skeleton(Monster):
    def __init__(self):
        self.difficulty = random.randint(5,7)
        super().__init__(
            type="SKELETON", 
            max_health=self.difficulty+2,
            current_health=self.difficulty+2,
            attack=3,
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

class MonsterMimic(Monster):
    def __init__(self):
        self.difficulty = random.randint(5,7)
        super().__init__(
            type="MIMIC", 
            max_health=self.difficulty*2,
            current_health=self.difficulty*2,
            attack=3,
            defense=self.difficulty+3, 
            perception=self.difficulty+1,
            stealth_mod=1,
            description="A thing pretending to be a different thing.",
            inventory=Inventory(
                weapon=weapon_options["MIMIC TOOTH"],
                misc=[],
                dollar_bills=self.difficulty-1
                )
            )
        
#-------------------------------------------------------------

class Wizard(Monster):
    def __init__(self):
        self.difficulty = random.randint(5,7)
        if self.difficulty == 5: self.attack = 2
        else: self.attack = 4 
        super().__init__(
            type="WIZARD", 
            max_health=self.difficulty-1,
            current_health=self.difficulty-1,
            attack=self.attack,
            defense=self.difficulty-1, 
            perception=self.difficulty+3,
            stealth_mod=2,
            description="Weird old person with magical abilities.",
            inventory=Inventory(weapon=weapon_options["MAGIC WAND"],
                consumables=[HealthPotion(), SmokeBomb()],
                misc=[misc_options["RUBY DUST"]],
                dollar_bills=self.difficulty+3
                ),
            attack_buff=5,
            defense_buff=5
            )

#-------------------------------------------------------------

class  MudGolem(Monster):
    def __init__(self):
        self.difficulty = random.randint(5,7)
        super().__init__(
            type="MUD GOLEM", 
            max_health=self.difficulty*10,
            current_health=self.difficulty*10,
            attack=3,
            defense=self.difficulty+2, 
            perception=self.difficulty+1,
            stealth_mod=5,
            description="A massive construct of hardened mud. Two piercing green marbles form its eyes, eminating magical energy. The smell is putrid.",
            inventory=Inventory(
                weapon=weapon_options["GOLEM FIST"],
                consumables=[GreaterHealthPotion()], 
                misc=[misc_options["GOLEM EYE"]], 
                dollar_bills=self.difficulty+5
                )
            )

#-------------------------------------------------------------

class  Minotaur(Monster):
    def __init__(self):
        self.difficulty = random.randint(7,10)
        super().__init__(
            type="MINOTAUR", 
            max_health=self.difficulty*4,
            current_health=self.difficulty*4,
            attack=4,
            defense=self.difficulty+3, 
            perception=self.difficulty+2,
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

class FlyingGoblin(Goblin):
    def __init__(self):
        super().__init__(
            type="FLYING GOBLIN", 
            descriptor="- flying variety.",
            defense_buff=2
            )
#----------------------------------------------------------------

class SeaCreature(Monster):
    def __init__(self, multiplier=1):
        self.difficulty = random.randint(6,9)
        self.multiplier = multiplier
        super().__init__(
            type="SEA CREATURE", 
            max_health=self.difficulty+(5*self.multiplier),
            current_health=self.difficulty+(5*self.multiplier),
            attack=2+self.multiplier,
            defense=self.difficulty+1, 
            perception=self.difficulty,
            stealth_mod=2,
            description="An sea creature of some sort. It's hard to make out the details underwater.",
            inventory=Inventory(
                weapon=weapon_options["TRIDENT"],
                misc=[misc_options["SEA CREATURE MEAT"], misc_options["SEA CREATURE MEAT"], misc_options["SEA CREATURE MEAT"], misc_options["SEA CREATURE MEAT"]],
                dollar_bills=0
                )
            )

#----------------------------------------------------------------

class  Avatar(Monster):
    def __init__(self):
        super().__init__(
            type="AVATAR OF DYNAE", 
            max_health=80,
            current_health=80,
            attack=4,
            defense=14, 
            perception=18,
            stealth_mod=7,
            description="An monsterous abomination. A snake creature with 7 heads, waves of electrical energy surge around its form.",
            inventory=Inventory(
                weapon=weapon_options["MAGIC SWORD"],
                consumables=[GreaterHealthPotion(), PowerBerry(), StatMedallion()],
                misc=[armor_options["MAGIC PLATE"]],
                dollar_bills=20
                ),
            )
    
    def make_attack(self, defender):
        attack_roll = random.randint(int(self.inventory.weapon.attack_odds1), int(self.inventory.weapon.attack_odds2)) + self.attack
        if misc_options["SHIELD"] in defender.inventory.misc: defender.defense_buff += 1
        print(f""" The {self.type} attacked with {attack_roll} attack!""")
        if attack_roll >= defender.defense + defender.defense_buff:
            print(f""" THE ATTACK HITS!""")
            damage = random.randint(int(self.inventory.weapon.damage_odds1), int(self.inventory.weapon.damage_odds2)) + self.attack
            print(f""" The attack deals {damage} damage!""")
        else:
            print(" The attack misses!")
            damage = 0
        defender.take_damage(damage)

    def take_damage(self, incoming_damage, print_damage=False):
        self.current_health -= incoming_damage
        if self.current_health <= 0:
                print(f""" THE {self.type} has died.""")

    def notice_player(self, stealth_check, player_request=False):
        print(f""" Your stealth is: {stealth_check}. The {self.type}'s perception is: {self.perception}.""")
        if stealth_check <= self.perception:
            if self.is_aware == True: print(f"""\n The {self.type} is aware of you!""")
            else: 
                self.is_aware = True
                print(f"""\n The {self.type} noticed you!""")
        elif stealth_check >= self.perception and player_request == True and self.is_aware == True:
            self.is_aware = False
            print(f"""\n The {self.type} lost you!""")
        else: print(f"""\n The {self.type} hasn't noticed you!""")
        return self.is_aware

    def investigate(self, player, room): #named like this to coincide with other interactables, but the player is the one investigating the monster here
        if player.investigation + random.randint(1,5) >= self.invest_requirement:
            if self.current_health > 0:
                print(f"""\n You were able to observe the {self.type} and glean some info about it.""")
                print(f"""\n The {self.type}'s attack is {self.attack}.""")
                print(f""" The {self.type}'s defense is {self.defense}.""")
                print(f""" The {self.type}'s health is {self.current_health}.""")
                print(f""" The {self.type}'s weapon is {self.inventory.weapon.name}.""")
                print(f""" The {self.type}'s defense buff is {self.defense_buff}.""")
                print(f""" The {self.type}'s attack buff is {self.attack_buff}.""")
            else:
                print(f"""\n You searched the {self.type} and found a {self.inventory.weapon.name}, """)
                player.inventory.add_item(self.inventory.weapon)
                for each_misc in self.inventory.misc:
                    print(f""" a {each_misc.name}, """)
                    player.inventory.add_item(each_misc)
                for each_consumable in self.inventory.consumables:
                    print(f""" a {each_consumable.name}, """)
                    player.inventory.add_item(each_consumable)
                print(f""" and {self.inventory.dollar_bills} dollar bills.""")
                player.inventory.dollar_bills += self.inventory.dollar_bills
                self.can_investigate = False
        else:
            print(f"""\n You investigated the {self.type}, but couldn't find anything.""")
            self.can_investigate = False
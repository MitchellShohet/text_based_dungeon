import random
from classes.dungeon.room_components import Interactable
from classes.combatants.combatant import Combatant
from lists.items_lists import weapon_options, armor_options, misc_options, HealthPotion, StatMedallion, PowerBerry, DurabilityGem, SmokeBomb, GreaterHealthPotion

class Pool(Interactable):

    def __init__(self, number, action_words, descriptor, action1_avail=True, action2_avail=False, action3_avail=False):
        self.type = "POOL"
        self.description = "A pool of water " + descriptor
        self.invest_requirement = 0
        self.stealth_mod = 0
        super().__init__(
            self.type, 
            number, 
            action_words, 
            self.description, 
            self.invest_requirement, 
            self.stealth_mod, 
            action1_avail, 
            action2_avail, 
            action3_avail)

    def run_interaction(self, action_word, player, room):
        if action_word == "SWIM":
            if self.action1_avail == True:
                if player.inventory.armor.rating == 3 or player.inventory.armor.rating == 4:
                    print(f"""\n Your {player.inventory.armor.name} is too heavy to swim in!""")
                    player.take_damage(2)
                    if player.current_health > 0:
                        print("You make it back to solid ground. Swimming in heavy armor could lead to drowning.")
                elif player.current_health == player.max_health:
                    print("\n Your health is currently full. Come back later to regain some in the POOL.")
                else:
                    print("\n You took a quick dip in the refreshing water!")
                    player.recover_health(4)
                    self.action1_avail == False
                    self.action_words.remove("SWIM")
            else:
                print("You've already gone swimming here. Best not to get pruny.")
        elif action_word == "THROW ROCKS":
            if self.action2_avail == True:
                print(f"""\n You throw some rocks into the water, it makes a lot of noise. \n You skip one rock {random.randint(1,6)} times!""")
                room.spawn_monster()

#---------------------------------------------------------

class GlowingCrystal(Interactable):

    def __init__(self, number, action_words, descriptor, action1_avail=True, action2_avail=False, action3_avail=False):
        self.type = "GLOWING CRYSTAL"
        self.description = "A large cluster of gems with a mysterious light sourced from within. Roughly the size of a" + descriptor
        self.invest_requirement = number*3
        self.stealth_mod = number
        super().__init__(
            self.type, 
            number, 
            action_words, 
            self.description, 
            self.invest_requirement, 
            self.stealth_mod, 
            action1_avail, 
            action2_avail, 
            action3_avail)

    def run_interaction(self, action_word, player, room):
        if action_word == "BREAK": #maybe connect this with ATTACK command later
            if self.action1_avail == True:
                crystal_def = Combatant("GLOWING CRYSTAL", 1, 1, 0, self.number*3+2, None, self.number)
                player.make_attack(crystal_def)
                if crystal_def.current_health <= 0:
                    if self.number == 1:
                        player.inventory.add_item(misc_options["RUBY DUST"])
                        print(f"""\n You found some RUBY DUST""")
                    if self.number == 2:
                        player.inventory.add_item(DurabilityGem())
                        print(f"""\n You found a DURABILITY GEM""")
                    if self.number == 3:
                        player.inventory.add_item(StatMedallion())
                        print(f"""\n You found a STAT MEDALLION""")
                    self.action_words.remove("BREAK")
                    if "INVESTIGATE FURTHER" in self.action_words:
                        self.action_words.remove("INVESTIGATE FURTHER")
                    self.type = "DESTROYED CRYSTAL PILE"
                    self.description = "The shattered remains of what used to by a GLOWING CRYSTAL"
                else:
                    print(f"""\n You couldn't break GLOWING CRYSTAL {self.number}.""")
                self.action1_avail = False
            elif self.type == "DESTROYED CRYSTAL PILE":
                print(f"""\n You've already destroyed GLOWING CRYSTAL {self.number}.""")
            else:
                print(f"""\n You've already tried breaking GLOWING CRYSTAL {self.number}.""")
        elif action_word == "INVESTIGATE FURTHER":
            if self.action2_avail == True and self.action1_avail == True:
                if player.investigation + random.randint(1,5) >= self.invest_requirement:
                    self.invest_requirement = 0
                    print("\n After some time you start to understand the secrets of the GLOWING CRYSTAL. \n You're able to extract the magic and recover some health.")
                    if player.current_health == player.max_health:
                        print("\n Your health is currently full. Come back later to regain some from the GLOWING CRYSTAL.")
                    else:
                        player.recover_health(self.number*3)
                        self.action2_avail == False
                        self.action_words.remove("INVESTIGATE FURTHER")
                else:
                    print(f"""\n The secrets of GLOWING CRYSTAL {self.number} elude you.""")
                    self.action2_avail = False
                    self.action_words.remove("INVESTIGATE FURTHER")
            elif self.type == "DESTROYED CRYSTAL PILE":
                print(f"""\n You've already destroyed GLOWING CRYSTAL {self.number}.""")
            else:
                print(f"""\n You've already investigated GLOWING CRYSTAL {self.number} further.""")

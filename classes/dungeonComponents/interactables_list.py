import random
from classes.dungeonComponents.interactable import Interactable

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
                room.spawn_monsters()

#---------------------------------------------------------

class GlowingCrystal(Interactable):

    def __init__(self, number, action_words, descriptor, action1_avail=True, action2_avail=False, action3_avail=False):
        self.type = "GLOWING CRYSTAL"
        self.description = "A large cluster of gems with a mysterious light sourced from within. Roughly the size of a" + descriptor
        self.invest_requirement = 4
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
        pass
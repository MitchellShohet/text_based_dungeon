import random
from abc import ABC, abstractmethod

class Interactable(ABC):

    def __init__(self, type, number, action_words, description, invest_requirement, stealth_mod, action1_avail=True, action2_avail=False, action3_avail=False):
        self.name = type
        self.number = number
        self.action_words = action_words
        self.description = description
        self.invest_requirement = invest_requirement
        self.stealth_mod = stealth_mod
        self.action1_avail=action1_avail
        self.action2_avail=action2_avail
        self.action3_avail=action3_avail
        self.can_investigate = True

    @abstractmethod
    def run_interaction(self, action_word, player, room): # doesn't work yet, look into it later
        pass

    def investigate(self, player):
        if player.investigation + random.randint(1,5) >= self.invest_requirement:
            print(f"""\n {self.description}""")
            if len(self.action_words) > 0:
                print("\n You could try to ")
                for each_action_word in self.action_words:
                    print(f"""{ each_action_word}""")
            self.invest_requirement = 0
        else:
            print("There's not much to find here.")
            self.invest_requirement = 1000

#------------------------------------------------------------------

class MonsterSpawning:

    def __init__(self, threshold1, monster1, threshold2=None, monster2=None):
        self.threshold1 = threshold1
        self.monster1 = monster1
        self.threshold2 = threshold2
        self.monster2 = monster2

#----------------------------------------------------------------

class Exit:
    def __init__(self, exit_number, link=None):
        self.exit_number = exit_number
        self.link = link

    def set_link(self, link):
        self.link = link
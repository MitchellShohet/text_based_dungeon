from abc import ABC, abstractmethod

class Exit:
    def __init__(self, number, link=None):
        self.number = number
        self.link = link

#----------------------------------------------------------------

class MonsterSpawning:

    def __init__(self, threshold1, monster1, threshold2=None, monster2=None):
        self.threshold1 = threshold1
        self.monster1 = monster1
        self.threshold2 = threshold2
        self.monster2 = monster2

#------------------------------------------------------------------

class Interactable(ABC):

    def __init__(self, type, number=0, action_words=[], description="", invest_requirement=0, stealth_mod=0):
        self.type = type
        self.number = number
        self.action_words = action_words
        self.description = description
        self.invest_requirement = invest_requirement
        self.stealth_mod = stealth_mod
        self.can_investigate = True

    @abstractmethod
    def run_interaction(self, action_word, player, room):
        pass

    def investigate(self, player, room):
        print(f"""\n {self.description}""")
        if len(self.action_words) > 0:
            print(" You could try to ")
            for each_action_word in self.action_words: print(f""" {each_action_word}""")
        else: print(" There's not much to do.")

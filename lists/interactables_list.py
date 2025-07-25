import random, math
from abc import ABC, abstractmethod
from confirm_sequence import confirm_sequence
from line_spacer import line_spacer
from classes.dungeon.room_components import Interactable
from classes.combatants.combatant import Combatant
from classes.dungeon.room import Room
from classes.dungeon.room_components import Exit, MonsterSpawning
from classes.inventory.inventory import Inventory
from classes.inventory.items import Weapon
from lists.monsters_list import Goblin, Skeleton, Wizard, MudGolem, Minotaur, SeaCreature, MonsterMimic
from lists.items_lists import weapon_options, armor_options, misc_options, HealthPotion, Pie, StatMedallion, PowerBerry, DurabilityGem, SmokeBomb, GreaterHealthPotion
from lists.adjustments_list import check_for_heavy_armor, add_monsters, sleeping_minotaur_defeated, run_sea_creature, run_shatter, punchline_test, run_inspect, inspect_crystal, inspect_tree, change_room, teleport_sequence, block_exit, change_room_description

#-------------------------------------------------------
#----------- PARENT INTERACTABLES ----------------------
#-------------------------------------------------------


class NPC(Interactable):

    def __init__(self, number, action_words, descriptor, name, pronouns, convo, invest_requirement, inventory=[misc_options["APPLES"], weapon_options["SHORTSWORD"]]):
        self.name = name
        self.pronouns = pronouns
        self.convo = convo
        self.inventory = inventory
        self.dollar_bills = invest_requirement*3
        self.refresh_requirement = 0
        super().__init__(
            type=name, 
            number=number, 
            action_words=action_words, 
            description=descriptor, 
            invest_requirement=invest_requirement, 
            stealth_mod=-1
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "TALK" and "TALK" in self.action_words:
            self.talk()
        elif action_word == "ROB" and "ROB" in self.action_words:
            self.attempt_robbery(player)

    def talk(self):
        if self.refresh_requirement == 100000: print(f""" {self.name}: {self.convo[2]} """)
        else: print(f""" {self.name}: {self.convo[0]} """)

    def attempt_robbery(self, player):
        if len(self.inventory) > 0: rand_num = random.randint(0, len(self.inventory)-1)
        else: rand_num = -1
        if player.hiding_score >= self.invest_requirement * 1.7:
            print(f""" You successfully robbed {self.name} without {self.pronouns[1]} noticing!""")
            new_items = []
            for each_item in self.inventory:
                player.inventory.add_item(each_item)
                if each_item.name not in new_items:
                    new_items.append(each_item.name)
            for each_new_item_name in new_items:
                print(f""" You got {sum(1 for each_item in self.inventory if each_item.name == each_new_item_name)} {each_new_item_name}!""")
            print(f""" You got {self.dollar_bills} dollar bills!""")
            player.inventory.dollar_bills += math.ceil(self.dollar_bills)
            self.inventory.clear()
            self.dollar_bills = 0
            self.invest_requirement *= 2
        elif player.hiding_score >= self.invest_requirement:
            if self.dollar_bills < 30: self.dollar_bills += 30
            print(f""" You robbed {self.name} a little without {self.pronouns[1]} noticing!""")
            if rand_num != -1:
                print(f""" You got 1 {self.inventory[rand_num].name}!""")
                player.inventory.add_item(self.inventory[rand_num])
                self.inventory.pop(rand_num)
            print(f""" You got {self.dollar_bills} dollar bills!""")
            player.inventory.dollar_bills += self.dollar_bills
            self.dollar_bills = 0
            self.invest_requirement = math.ceil(self.invest_requirement * 1.4)
        else:
            print(f""" {self.name}: {self.convo[1]}""")
            print(f""" {self.name} caught you trying to rob {self.pronouns[1]}""")
            if self.invest_requirement < 12:
                if rand_num != -1:
                    print(f""" You still managed to swipe a {self.inventory[rand_num].name}""")
                    player.inventory.add_item(self.inventory[rand_num])
                    self.inventory.pop(rand_num)
                else: 
                    print(f""" You still managed to swipe {math.ceil(self.dollar_bills /5)} dollar bills!""")
                    player.inventory.dollar_bills += math.ceil(self.dollar_bills /5)
                    self.dollar_bills -= math.ceil(self.dollar_bills /5)
            self.refresh_requirement = 100000
            self.invest_requirement = math.ceil(self.invest_requirement * 1.7)

#---------------------------------------------------------

class Breakable(Interactable):

    def __init__(self, type, number, action_words, description, invest_requirement, stealth_mod, challenge=1, contents=None, punchline=None):
        self.challenge = challenge
        self.contents = contents
        self.punchline = punchline
        super().__init__(
            type, 
            number, 
            action_words, 
            description, 
            invest_requirement, 
            stealth_mod)
    
    def run_interaction(self, action_word, player, room):
        if action_word == "SHATTER" and "SHATTER" in self.action_words or action_word == "BREAK" and "BREAK" in self.action_words or action_word == "CHOP" and "CHOP" in self.action_words or action_word == "SMASH" and "SMASH" in self.action_words:
            run_shatter(self, player, room)
        else: punchline_test(self, action_word)

#---------------------------------------------------------

class Inspectable(Interactable):

    def __init__(self, type, number, action_words, description, invest_requirement, stealth_mod, effect=None):
        self.effect = effect
        self.refresh_requirement = 0
        super().__init__(
            type, 
            number, 
            action_words, 
            description, 
            invest_requirement, 
            stealth_mod)
    
    def run_interaction(self, action_word, player, room):
        if action_word == "INSPECT" and "INSPECT" in self.action_words or action_word == "INSPECT FIRST DIAL" and "INSPECT FIRST DIAL" in self.action_words or action_word == "INSPECT SECOND DIAL" and "INSPECT SECOND DIAL" in self.action_words:
            print("GLKJASDF")
            run_inspect(self, player, room)

#---------------------------------------------------------

class Lockable(Interactable, ABC):

    def __init__(self, type, number, action_words, description, stealth_mod, challenge=0):
        self.challenge = challenge
        super().__init__(
            type=type, 
            number=number, 
            action_words=action_words, 
            description=description, 
            invest_requirement=number, 
            stealth_mod=stealth_mod
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "OPEN" and "OPEN" in self.action_words:
            if self.challenge > 0: self.select_unlock_method(player, room)
            else: 
                print(f""" You opened the {self.type}!""")
                self.open(player)
        elif action_word == "BREAK THE LOCK" and "BREAK THE LOCK" in self.action_words:
            self.attempt_to_break(player, room)
        elif action_word == "USE A KEY" and "USE A KEY" in self.action_words:
            self.use_key(player, room)
    
    @abstractmethod
    def open(self, player):
        pass

    def select_unlock_method(self, player, room):
        selection_loop = True
        while selection_loop == True:
            print(f""" The {self.type} is locked. How would you like to open it?""")
            for each_option in self.action_words:
                if each_option != "OPEN": print(f"""{each_option}""")
            print("NEVERMIND")
            selection = input("- ").upper()
            if selection == "NEVERMIND": selection_loop = False
            for each_option in self.action_words:
                if selection == each_option:
                    self.run_interaction(selection, player, room)
                    selection_loop = False
            if selection_loop == True: print(" That's not an option here.")

    def attempt_to_break(self, player, room):
        lock_def = Combatant("LOCK", 1, 1, 0, self.challenge, Inventory())
        player.make_attack(lock_def)
        if lock_def.current_health <= 0: self.unlock_success(player, room)
        else:
            print(" You jammed THE LOCK into the closed position. You can try again but it'll be even more difficult now.")
            self.challenge*=2
            self.description += " THE LOCK has been jammed closed."
            if "USE A KEY" in self.action_words: self.action_words.remove("USE A KEY")
    
    def use_key(self, player, room):
        if misc_options["KEY"] in player.inventory.misc:
            player.inventory.misc.remove(misc_options["KEY"])
            print(" You used your KEY to open THE LOCK. It then dissintegrates, it's task in this world complete.")
            self.unlock_success(player, room)
        else: print(" You don't have a KEY to use.")

    def unlock_success(self, player, room):
        self.challenge = 0
        self.action_words.remove("BREAK THE LOCK")
        if "USE A KEY" in self.action_words: self.action_words.remove("USE A KEY")
        self.action_words.append("OPEN")
        self.run_interaction("OPEN", player, room)

#---------------------------------------------------------

class Tree(Breakable):

    def __init__(self, number, action_words, descriptor, stealth_mod=1, challenge=0, fruit=misc_options["APPLES"], type="TREE", punchline=None, contents=misc_options["WOOD"]):
        self.fruit = fruit
        self.punchline = punchline
        super().__init__(
            type=type, 
            number=number, 
            action_words=action_words, 
            description="A" + descriptor + " tree.", 
            invest_requirement=challenge, 
            stealth_mod=stealth_mod,
            challenge = challenge,
            contents=contents
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "PICK FRUIT" and "PICK FRUIT" in self.action_words:
            self.pick_fruit(player)
        elif action_word == "CHOP" and "CHOP" in self.action_words:
            self.chop(player, room)
        else: punchline_test(self, action_word)

    def pick_fruit(self, player):
        if "APOLOGIZE" not in self.action_words:
            print(f""" You picked some of the tree's {self.fruit.name}!""")
            player.inventory.add_item(self.fruit)
            self.action_words.remove("PICK FRUIT")
        else: print(f""" The {self.type} won't let you pick it's fruit.""")

    def chop(self, player, room):
        run_shatter(self, player, room)
        for each_interactable in room.interactables:
            if "TREE REMAINS" in each_interactable.type: room.interactables.remove(each_interactable)

#---------------------------------------------------------

class RedHerring(Interactable):

    def __init__(self, type, number=0, action_words=[], description="", invest_requirement=0, stealth_mod=0, punchline=None):
        self.punchline = punchline
        super().__init__(
            type=type, 
            number=number, 
            action_words=action_words, 
            description=description, 
            invest_requirement=invest_requirement, 
            stealth_mod=stealth_mod
            )

    def run_interaction(self, action_word, player, room):
        punchline_test(self, action_word)

#---------------------------------------------------------

class Crossing(Interactable, ABC):

    def __init__(self, type, number, action_words, description, exit_hold, jump_challenge, bridge):
        self.exit_hold = exit_hold
        self.jump_challenge = jump_challenge
        self.bridge = bridge
        super().__init__(
            type=type, 
            number=number, 
            action_words=action_words, 
            description=description, 
            invest_requirement=0, 
            stealth_mod=0
            )

    def run_interaction(self, action_word, player, room): 
        if action_word == "JUMP" and "JUMP" in self.action_words or action_word == "WALK PAST" and "WALK PAST" in self.action_words:
            self.jump(player, room)
        elif action_word == "BUILD BRIDGE" and "BUILD BRIDGE" in self.action_words:
            self.build_bridge(player)
        elif action_word == "CROSS BRIDGE" and "CROSS BRIDGE" in self.action_words:
            self.cross_bridge(player, room)
        elif action_word == "TAKE BRIDGE" and "TAKE BRIDGE" in self.action_words:
            self.take_bridge(player)
        elif action_word == "THROW ROCKS" and "THROW ROCKS" in self.action_words:
            self.throw_rocks(player, room)
        elif action_word == "SNEAK ATTACK" and "SNEAK ATTACK" in self.action_words:
            self.sneak_attack(player, room)

    def switch_sides(self, room):
        try: room.exits[0].number
        except: 
            room.exits[0] = self.exit_hold
            self.exit_hold = room.exits[1]
            room.exits.pop(1)
        else: 
            room.exits.append(self.exit_hold)
            self.exit_hold = room.exits[0]
            room.exits[0] = None

    def jump(self, player, room):
        jump_score = random.randint(1,8)
        if jump_score >= self.jump_challenge:
            print(f""" With a running start, you successfully leap clear across the {self.type}!""")
            self.switch_sides(room)
        else: self.jump_failure(jump_score, player, room)

    def build_bridge(self, player):
        if misc_options["MAGIC BRIDGE"] in player.inventory.misc:
            print(f""" You placed the MAGIC BRIDGE over the {self.type}!""")
            self.bridge = "MAGIC"
            player.inventory.misc.remove(misc_options["MAGIC BRIDGE"])
            self.action_words.remove("BUILD BRIDGE")
            self.action_words.append("CROSS BRIDGE")
            self.action_words.append("TAKE BRIDGE")
        elif misc_options["WOOD"] in player.inventory.misc:
            wood_count = 0
            for each_item in player.inventory.misc:
                if each_item.name == "WOOD": wood_count += 1
            if wood_count >= 3:
                print(f""" You built a WOOD BRIDGE over the {self.type}!""")
                self.bridge = "WOOD"
                for x in range(3):
                    player.inventory.misc.remove(misc_options["WOOD"])
                self.action_words.remove("BUILD BRIDGE")
                self.action_words.append("CROSS BRIDGE")
            else: print(" You don't have enough wood to build a bridge.")
        else: print(" You don't have the materials to build a bridge.")

    def cross_bridge(self, player, room):
        print(f""" You crossed the {self.bridge} BRIDGE over the {self.type}""")
        self.switch_sides(room)
        if self.bridge == "WOOD" or self.bridge == "RICKETY OLD":
            self.wood_failure(player, room)
    
    def take_bridge(self, player):
        print(f""" You took the MAGIC BRIDGE and put it in your pocket. The {self.type} is now blocking the opposite path.""")
        self.action_words.remove("CROSS BRIDGE")
        self.action_words.remove("TAKE BRIDGE")
        self.action_words.append("BUILD BRIDGE")
        player.inventory.add_item(misc_options["MAGIC BRIDGE"])
            
    @abstractmethod
    def jump_failure(self, jump_score, player, room):
        pass

    @abstractmethod
    def wood_failure(self, player, room):
        pass

    @abstractmethod
    def throw_rocks(self, player, room):
        pass

    def sneak_attack(self, player, room):
        pass

#-------------------------------------------------------
#--------------- CHILD INTERACTABLES -------------------
#-------------------------------------------------------

class ExitHold(RedHerring): #MUST BE AT POSITION [0] OF ITS ROOM'S INTERACABLES

    def __init__(self, type, action_words, description, punchline=None, exit_hold=None):
        self.exit_hold = exit_hold
        super().__init__(
            type=type, 
            action_words=action_words, 
            description=description, 
            punchline=punchline
            )

#---------------------------------------------------------

class SecretPassage(Inspectable): #MUST BE ACCOMPANIED BY AN EXITHOLD
    def __init__(self, type, number, action_words, description, invest_requirement, stealth_mod, effect=None):
        super().__init__(type, number, action_words, description, invest_requirement, stealth_mod, effect)

    def run_interaction(self, action_word, player, room):
            if action_word == "INSPECT" and "INSPECT" in self.action_words:
                run_inspect(self, player, room)
                if "SECRET TUNNEL" not in self.action_words and "CLIMBING PATH" not in self.action_words: 
                    print(" You can try again later.")
                    self.refresh_requirement += 1
            elif action_word == "SECRET TUNNEL" and "SECRET TUNNEL" in self.action_words or action_word == "CLIMBING PATH" and "CLIMBING PATH" in self.action_words or action_word == "CASTLE DOOR" and "CASTLE DOOR" in self.action_words and self.type == "KEEP" or action_word == "STAIRCASE" and "STAIRCASE" in self.action_words and self.type == "TOWER UPPER FLOORS":
                if room.name == "CHASM SEA CREATURE": room.adjustments[2]["change_room"][0] = room.interactables[0].exit_hold  #**This should apply to all instances of SecretPassage(), but we'll fix that later
                room.adjustments[1].append(change_room)
                print(line_spacer,
                "\n",
                f"""\n You took the {action_word}""")
            elif action_word == "CASTLE DOOR" and "CASTLE DOOR" in self.action_words:
                print(" Magic is keeping the CASTLE DOOR closed.")
            elif action_word == "STAIRCASE" and "STAIRCASE" in self.action_words:
                print(" Magic is keeping the STAIRCASE blocked.")

#---------------------------------------------------------

class Chest(Lockable):

    def __init__(self, number, action_words, descriptor="", challenge=0, contents=[10]):
        self.contents = contents
        super().__init__(
            type="CHEST", 
            number=number, 
            action_words=action_words, 
            description="A treasure chest" + descriptor, 
            stealth_mod=1,
            challenge=challenge
            )
    
    def open(self, player):
        reward_num = random.randint(1, len(self.contents))-1
        try:
            self.contents[reward_num].type
            player.inventory.add_item(self.contents[reward_num])
            print(f""" You found a {self.contents[reward_num].name}!""")
        except: 
            player.inventory.dollar_bills += self.contents[reward_num]
            print(f""" You found {self.contents[reward_num]} dollar bills!""")
        self.action_words.remove("OPEN")
        self.description = f"""A {self.type} that's been opened."""

#---------------------------------------------------------

class Container(Lockable):

    def __init__(self, type, number, action_words, descriptor, contents=None, stealth_mod=1):
        self.contents = contents
        super().__init__(
            type=type, 
            number=number, 
            action_words=action_words, 
            description=descriptor, 
            stealth_mod=stealth_mod,
            challenge=0
            )
    
    def open(self, player):
        if self.contents == None: print(" There was nothing inside.")
        else:
            try:
                self.contents.type
                player.inventory.add_item(self.contents)
                print(f""" You found a {self.contents.name}!""")
            except: 
                player.inventory.dollar_bills += self.contents
                print(f""" You found {self.contents} dollar bills!""")
        self.action_words.remove("OPEN")
        self.description = f"""A {self.type} that's been opened."""
#---------------------------------------------------------

class Mimic(Lockable):

    def __init__(self, type, number, action_words, description, challenge=0, stealth_mod=1):
        self.contents = None
        super().__init__(
            type=type, 
            number=number, 
            action_words=action_words, 
            description=description, 
            stealth_mod=stealth_mod,
            challenge=challenge 
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "SHATTER" and "SHATTER" in self.action_words or action_word == "BREAK" and "BREAK" in self.action_words or action_word == "CHOP" and "CHOP" in self.action_words or action_word == "SMASH" and "SMASH" in self.action_words:
            self.open(player)
        elif action_word == "OPEN" and "OPEN" in self.action_words:
            if self.challenge > 0: self.select_unlock_method(player, room)
            else: 
                print(f""" You opened the {self.type}!""")
                self.open(player)
        elif action_word == "BREAK THE LOCK" and "BREAK THE LOCK" in self.action_words:
            self.attempt_to_break(player, room)
        elif action_word == "USE A KEY" and "USE A KEY" in self.action_words:
            self.use_key(player, room)
        elif action_word == "ATTACK MIMIC" and "ATTACK MIMIC" in self.action_words:
            self.get_accused(player, room)

    def open(self, player):
        print(f""" It's a MIMIC!""")
        player.take_damage(2, True)
        if "ATTACK MIMIC" not in self.action_words: self.action_words.append("ATTACK MIMIC")
        print(f""" You escaped the MIMIC""")

    def get_accused(self, player, room):
        if self.type == "MIMIC":
            print(f""" Woah! That was a MIMIC!""")
            room.spawn_monster(MonsterMimic)
            room.monsters[len(room.monsters)-1].is_aware = True
            if self.contents != None: room.monsters[len(room.monsters)-1].inventory.misc.append(self.contents)
            player.make_attack(room.monsters[len(room.monsters)-1])
            self.type = "COMPROMISED MIMIC"
            for each_interactable in room.interactables:
                if each_interactable.type == "COMPROMISED MIMIC": room.interactables.remove(each_interactable)
        else: print(f""" What're you talking about? That's a {self.type}?""")
        
    def reveal(self):
        self.type = "MIMIC"
        self.number = 0
        if "ATTACK MIMIC" not in self.action_words: self.action_words.append("ATTACK MIMIC")

#---------------------------------------------------------

class GlowingCrystal(Breakable):

    def __init__(self, number, action_words, descriptor, challenge=1):
        if number == 1: self.contents = misc_options["RUBY DUST"]
        elif number == 2: self.contents = DurabilityGem()            
        elif number == 3: self.contents = StatMedallion()
        self.run_effect = False
        self.effect = inspect_crystal
        super().__init__(
            type="GLOWING CRYSTAL", 
            number=number, 
            action_words=action_words, 
            description="A large cluster of gems with a mysterious light sourced from within. Roughly the size of a" + descriptor, 
            challenge=challenge,
            invest_requirement=challenge, 
            stealth_mod=challenge,
            contents=self.contents
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "SHATTER" and "SHATTER" in self.action_words:
            run_shatter(self, player, room)
        elif action_word == "INSPECT" and "INSPECT" in self.action_words:
            run_inspect(self, player, room)

#---------------------------------------------------------

class GlowingTree(Tree):

    def __init__(self, number, action_words, descriptor=" glowing", stealth_mod=1, challenge=7):
        self.gift_given = False
        self.run_effect = False
        self.refresh_requirement = 0
        self.effect = inspect_tree
        if challenge == 15:
            self.reward = weapon_options["MAGIC SWORD"]
            self.monster = Minotaur()
        elif challenge == 10:
            self.reward = armor_options["CHAINMAIL"]
            self.monster = MudGolem()
        else: 
            self.reward = GreaterHealthPotion()
            self.monster = Wizard()
        super().__init__(
            type="GLOWING TREE", 
            number=number, 
            action_words=action_words, 
            descriptor=descriptor, 
            stealth_mod=stealth_mod,
            challenge=challenge,
            fruit=misc_options["GLOWING FRUIT"]
            )
    
    def run_interaction(self, action_word, player, room):
        if action_word == "PICK FRUIT" and "PICK FRUIT" in self.action_words:
            self.pick_fruit(player)
        elif action_word == "CHOP" and "CHOP" in self.action_words:
            self.chop(player, room)
        elif action_word == "INSPECT" and "INSPECT" in self.action_words:
            run_inspect(self, player, room)
            if self.gift_given == False: 
                print(" Though, it will allow you to try again later.")
                self.refresh_requirement += 2
        elif action_word == "APOLOGIZE" and "APOLOGIZE" in self.action_words: print(" The GLOWING TREE does not accept your apology.")

    def chop(self, player, room):
        tree_def = Combatant(self.type, 1, 1, 3, self.challenge, Inventory(weapon=Weapon(0, "WEAPON", "", self.challenge/5, self.challenge, self.challenge, self.challenge, 0)), self.number)
        if self.gift_given == True:
            print(" Betrayed, the GLOWING TREE attacks you with it's magic!")
            tree_def.make_attack(player)
        run_shatter(self, player, room)
        for each_interactable in room.interactables:
            if "TREE REMAINS" in each_interactable.type: room.interactables.remove(each_interactable)
        if self.type == "GLOWING TREE":
            print(" The GLOWING TREE hardened itself with magic. You can no longer CHOP or INSPECT it.")
            if "INSPECT" in self.action_words: self.action_words.remove("INSPECT")
            self.action_words.append("APOLOGIZE")

#---------------------------------------------------------

class MoneyTree(Tree):

    def __init__(self, action_words):
        self.refresh_requirement = 0

        super().__init__(
            type="MONEY TREE", 
            number=0, 
            action_words=action_words, 
            descriptor="money", 
            stealth_mod=2,
            fruit=20,
            challenge=0
            )

    def pick_fruit(self, player):
        print(f""" You picked {self.fruit} dollar bills from the tree!""")
        player.inventory.dollar_bills += self.fruit
        self.fruit = 0
        self.action_words.remove("PICK FRUIT")

#---------------------------------------------------------

class Chasm(Crossing):

    def __init__(self, number, action_words, descriptor, challenge=4, bridge=None):
        self.descriptor = descriptor
        self.fail_count = 0
        self.fail_limit = random.randint(1,5)
        super().__init__(
            type="CHASM", 
            number=number, 
            action_words=action_words, 
            description="A chasm that drops into nothingness", 
            exit_hold=Exit(1),
            jump_challenge=challenge,
            bridge=bridge,
            )

    def jump_failure(self, jump_score, player, room):
        print(" You attempt to leap over the abyss, but your footing was off and you tumble into the dark.")
        print(room.adjustments[2]["jump_failure"][0])
        if room.adjustments[2]["jump_failure"][1] > 0: player.take_damage(room.adjustments[2]["jump_failure"][1], True)
        if player.current_health > 0: 
            room.adjustments[1].append(change_room)

    def wood_failure(self, player, room):
        if self.bridge == "RICKETY OLD":
            wood_creak = random.randint(1,4)
            self.fail_count += 1
            if wood_creak == 1 or self.fail_count >= self.fail_limit:
                print(" As you pass there's a loud crack and the rickety bridge collapses under your foot!")
                print(room.adjustments[2]["jump_failure"][0])
                if room.adjustments[2]["jump_failure"][1] > 0: player.take_damage(room.adjustments[2]["jump_failure"][1], True)
                if player.current_health > 0: 
                    room.adjustments[1].append(change_room)
                if room.adjustments[2]["wood_failure"][0]: room.description = room.adjustments[2]["wood_failure"][0]
                self.action_words.append("BUILD BRIDGE")
                self.action_words.remove("CROSS BRIDGE")
                self.bridge = None
            else: print(" As you pass there's a loud crack! You hold your breath, but the bridge holds fine and you cross without issue.")

    def throw_rocks(self, player, room):
        print(f""" You throw some rocks into the chasm{self.descriptor}""")
        room.spawn_monster()

#---------------------------------------------------------

class MagmaRiver(Crossing):

    def __init__(self, number, action_words, descriptor, exit_hold, jump_challeng=7):
        super().__init__(
            type="MAGMA RIVER", 
            number=number, 
            action_words=action_words, 
            description=f"""A {descriptor}wide river of flowing lava.""", 
            exit_hold = exit_hold,
            jump_challenge=jump_challeng,
            bridge=None,
            )

    def jump_failure(self, jump_score, player, room):
        if jump_score == 1:
            print(" The ash in the room choking you, you attempt to leap across the MAGMA RIVER and land less than halfway across.")
            player.take_damage(random.randint(7,11), True)
            if player.current_health > 0: print(" You make it back onto land. You weren't able to cross, but you did survive jumping into lava.")
        elif jump_score > 1:
            print(" With a running start you successfully leap most of the way accross MAGMA RIVER! You land just short of the opposite bank.")
            player.take_damage(random.randint(2,4), True)
            if player.current_health > 0:
                print(" You made it to the opposite bank with minimal burns considering you jumped a MAGMA RIVER. However the opposite side is now blocked.")
                self.switch_sides(room)

    def wood_failure(self, player, room):
        print(" Afterward the bridge catches fire and incinerates. The opposite path is blocked by the MAGMA RIVER again.")
        self.action_words.append("BUILD BRIDGE")
        self.action_words.remove("CROSS THE BRIDGE")

    def throw_rocks(self, player, room):
        print(f""" You throw some rocks into the lava, they sink immediately.""")
        room.spawn_monster()

#---------------------------------------------------------

class SleepingMinotaur(Crossing):

    def __init__(self, description):
        self.fail_limit = random.randint(1,5)
        self.fail_count = 0
        super().__init__(
            type="SLEEPING MINOTAUR", 
            number=0, 
            action_words=["WALK PAST", "BUILD BRIDGE", "THROW ROCKS", "SNEAK ATTACK"], 
            description=description, 
            exit_hold = Exit(1, Room("SLEEPING MINOTAUR PASSAGE", 
                                        "A tunnel beyond the sleeping minotaur opens to a hallway with a chest. The path forks in two directions.", 
                                        [Exit(0), Exit(1)], 
                                        MonsterSpawning(7, Skeleton), 
                                        [Chest(3, ["BREAK THE LOCK", "USE A KEY"]," placed over a fur rug.", contents=[weapon_options["BATTLE AXE"], armor_options["CHAINMAIL"], StatMedallion(), 65])])),
            jump_challenge = 15,
            bridge = None
            )

    def jump(self, player, room):
        if player.hiding_score >= self.jump_challenge:
            print(f""" Cautiously, you successfully tiptoe past the {self.type}!""")
            self.switch_sides(room)
        else: self.jump_failure(player.hiding_score, player, room)
    
    def jump_failure(self, hiding_score, player, room):
        print(" MINOTAURS are highly perceptive, even in their sleep.")
        self.wake_minotaur(player, room)

    def wood_failure(self, player, room):
        wood_creak = random.randint(1,4)
        self.fail_count += 1
        if wood_creak == 1 or self.fail_count >= self.fail_limit:
            print(" As you pass there's a loud creak! Guess you should've stayed in carpentry school.")
            self.wake_minotaur(player, room)
        else: print(" Wood bridges are notorious for being quiet.")

    def throw_rocks(self, player, room):
        self.fail_count += 2
        if self.fail_count >= self.fail_limit:
            print(" You chuck a rock at the MINOTAUR and bean it in the head. Pissed it jumps up and spots you. Seems like it was having a good dream too.")
            self.wake_minotaur(player, room)
        else: 
            print(" You throw a rock in the opposite corner of the room as you sneak past. The MINOTAUR wakes and looks toward the sound. After a tense moment it goes back to sleep and you successfully cross past it.")
            self.switch_sides(room)

    def sneak_attack(self, player, room):
        if player.hiding_score >= self.jump_challenge:
            print(f""" Cautiously, you successfully tiptoe up to the {self.type}!""")
            self.wake_minotaur(player, room, True)
        else:
            print(" MINOTAURS are highly perceptive, even in their sleep.")
            self.wake_minotaur(player, room)

    def wake_minotaur(self, player, room, is_attacked=False):
        room.adjustments[2]["add_monsters"][0] = room.visits
        room.adjustments[2]["change_room_description"][0] = room.visits
        room.adjustments[1].append(sleeping_minotaur_defeated)
        add_monsters(room, 0)
        if is_attacked == True: player.make_attack(room.monsters[0])
        print(" You woke the SLEEPING MINOTAUR!")
        room.monsters[0].is_aware = True
        room.monsters[0].make_attack(player)
        if self.exit_hold.number == 1: room.exits.append(self.exit_hold)
        else: room.exits[0] = self.exit_hold
        if self.bridge == "MAGIC": player.inventory.add_item(misc_options["MAGIC BRIDGE"])
        room.interactables.clear()

#---------------------------------------------------------

class Merchant(NPC):

    def __init__(self, number, action_words, descriptor, name, pronouns, convo, invest_requirement, inventory=[misc_options["APPLES"], weapon_options["SHORTSWORD"]]):
        super().__init__(
            number=number, 
            action_words=action_words, 
            descriptor=descriptor, 
            name = name,
            pronouns = pronouns,
            convo = convo,
            invest_requirement=invest_requirement, 
            inventory = inventory,
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "TALK" and "TALK" in self.action_words:
            self.talk()
        elif action_word == "ROB" and "ROB" in self.action_words:
            self.attempt_robbery(player)
        elif action_word == "SELL" and "SELL" in self.action_words:
            self.run_sell_sequence(player)

    def run_sell_sequence(self, player):
        if self.refresh_requirement == 100000: print(f""" {self.name}: {self.convo[2]} """)
        elif len(player.inventory.misc + player.inventory.consumables) <= 0: print(f""" {self.name}: {self.convo[5]}""")
        else:
            all_options = self.build_sell_product_list(player)
            selection_loop = True
            while selection_loop == True:
                print(f""" {self.name}: {self.convo[3]}""")
                print(" OFFER | PRODUCT | NUMBER IN INVENTORY")
                for each_product in all_options:
                    if math.ceil(each_product.value * .75) <= 9:
                        print(f""" {math.ceil(each_product.value * .75)}  | {each_product.name} x{sum(1 for each_item in player.inventory.misc if each_item.name == each_product.name) + sum(1 for each_item in player.inventory.consumables if each_item.name == each_product.name)}""")
                    else: print(f""" {math.ceil(each_product.value * .75)} | {each_product.name} x{sum(1 for each_item in player.inventory.misc if each_item.name == each_product.name) + sum(1 for each_item in player.inventory.consumables if each_item.name == each_product.name)}""")
                print(" NEVERMIND")
                selection = input("\n - ").upper()
                if selection == "NEVERMIND": selection_loop = False
                for each_product in all_options:
                    if selection == each_product.name:
                        quantity = self.determine_quantity(player.inventory.misc + player.inventory.consumables, each_product)
                        if quantity > 0: 
                            if confirm_sequence(f""" Sell {quantity} {each_product.name} to {self.name} for {math.ceil(each_product.value * .75 * quantity)}?""", f""" {self.name}: {self.convo[4]}""", f""" {self.name} looks dissapointed but understands."""): 
                                self.sell_product(player, each_product, quantity)
                        else: print(f""" {self.name} looks dissapointed but understands.""")
                        selection_loop = False
                if selection_loop == True: print(f""" {self.name} You don't have any {selection} to sell.""")

    def build_sell_product_list(self, player):
        all_options = []
        for each_misc in player.inventory.misc:
            if each_misc.name not in all_options and each_misc.name != "FIST": all_options.append(each_misc.name)
        for each_misc in player.inventory.misc:
            if each_misc.name in all_options: all_options[all_options.index(each_misc.name)] = each_misc
        for each_consumable in player.inventory.consumables:
            if each_consumable.name not in all_options: all_options.append(each_consumable.name)
        for each_consumable in player.inventory.consumables:
            if each_consumable.name in all_options: all_options[all_options.index(each_consumable.name)] = each_consumable
        return all_options
    
    def determine_quantity(self, inventory, product, seller="PLAYER"):
        quantity = 1
        if sum(1 for each_item in inventory if each_item.name == product.name) > 1:
            quantity_loop = True
            while quantity_loop == True:
                if seller == "PLAYER": print(f""" You have {sum(1 for each_item in inventory if each_item.name == product.name)} {product.name}. How many would you like to sell?""")
                else: print(f""" {self.name} has {sum(1 for each_item in inventory if each_item.name == product.name)} {product.name}. How many would you like to buy?""")
                quantity = (input("\n - "))
                try: int(quantity)
                except: print(" Please input a number.")
                else: 
                    quantity = int(quantity)
                    if quantity > sum(1 for each_item in inventory if each_item.name == product.name) and seller == "PLAYER": print(f""" You don't have that many {product.name}.""")
                    elif quantity > sum(1 for each_item in inventory if each_item.name == product.name): print(f""" {self.name} doesn't have that many {product.name}.""")
                    elif quantity < 0 and seller == "PLAYER": print(" You cannot sell a negative amount.")
                    elif quantity < 0: print(" You cannot buy a negative amount.")
                    elif quantity == 0: 
                        if seller== "PLAYER": print(" Cancel your sale?")
                        else: print(" Cancel your purchase?")
                        command = input("\n - ").upper()
                        if command == "YES" or command == "YEAH" or command == "YEP" or command == "Y": quantity_loop = False
                    else: quantity_loop = False
        return quantity
    
    def sell_product(self, player, product, quantity):
        print(f""" You sold {quantity} {product.name} to {self.name} for {math.ceil(product.value * .75) * quantity} dollar bills!""")
        for x in range(quantity):
            self.inventory.append(product)
            if self.dollar_bills >= math.ceil(product.value * .75) + 30: self.dollar_bills -= math.ceil(product.value * .75)
            player.inventory.dollar_bills += math.ceil(product.value * .75)
            if product.type == "CONSUMABLE":
                for each_consumable in player.inventory.consumables:
                    if each_consumable.name == product.name:
                        player.inventory.remove_item(each_consumable)
                        break
            else: player.inventory.remove_item(product)

#---------------------------------------------------------

class Artisan(Merchant):

    def __init__(self, number, action_words, descriptor, name, pronouns, convo, invest_requirement, price=0, service=None, inventory=[misc_options["APPLES"], weapon_options["SHORTSWORD"]], item_req=None, item_quantity_req=None):
        self.price = price
        self.service = service
        self.item_req = item_req
        self.item_quantity_req = item_quantity_req
        super().__init__(
            number=number, 
            action_words=action_words, 
            descriptor=descriptor, 
            name=name,
            pronouns=pronouns,
            convo=convo,
            invest_requirement=invest_requirement,
            inventory=inventory
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "TALK":
            self.talk()
        elif action_word == "ROB" and "ROB" in self.action_words:
            self.attempt_robbery(player)
        elif action_word == "SELL":
            self.run_sell_sequence(player)
        elif action_word == "TRADE" and "TRADE" in self.action_words or action_word == "HIRE" and "HIRE" in self.action_words or action_word == "TELEPORT" and "TELEPORT" in self.action_words or action_word == "ENCHANT" and "ENCHANT" in self.action_words:
            self.trade(player, room, action_word)

    def trade(self, player, room, action_word):
        if self.refresh_requirement == 100000: print(f""" {self.name}: {self.convo[2]} """)
        elif self.item_req != None and sum(1 for each_item in player.inventory.misc if each_item.name == self.item_req.name) < self.item_quantity_req: print(f""" {self.name}: You don't have enough {self.item_req.name} in your inventory.""")
        elif player.inventory.dollar_bills < self.price: print(f""" {self.name}: {self.convo[6]} You don't have enough dollar bills though..""")
        else:
            if confirm_sequence(f""" {self.name}: {self.convo[6]}""", f""" {self.name} {self.convo[4]}""", f""" {self.name} looks dissappointed but understands."""):
                room.adjustments[1].append(self.service)
                self.charge_fee(player, action_word)

    def charge_fee(self, player, action_word):
        if self.item_req != None:
            for x in range(self.item_quantity_req):
                self.inventory.append(self.item_req)
                player.inventory.misc.remove(self.item_req)
        self.dollar_bills += self.price
        player.inventory.dollar_bills -= self.price

#---------------------------------------------------------

class Fairy(Artisan):

    def __init__(self, number, descriptor, name, pronouns, convo, invest_requirement):
        super().__init__(
            number=number, 
            action_words=["TALK", "ROB", "SELL", "TELEPORT"], 
            descriptor=descriptor, 
            name = name,
            pronouns = pronouns,
            convo = convo,
            invest_requirement=invest_requirement, 
            inventory = [misc_options["BLADE OF GRASS"], misc_options["BLADE OF GRASS"], misc_options["BLADE OF GRASS"], misc_options["BLADE OF GRASS"]],
            price=40,
            service=teleport_sequence
            )
        
    def trade(self, player, room, action_word):
        if self.refresh_requirement == 100000: print(f""" {self.name}: {self.convo[2]} """)
        elif player.inventory.dollar_bills < 40 and sum(1 for each_item in player.inventory.misc if each_item.name == "BLADE OF GRASS") < 20: print(f""" {self.name}: You don't have enough money or grass!""")
        else:
            if confirm_sequence(f""" {self.name}: {self.convo[6]}""", f""" {self.name} {self.convo[7]}""", f""" {self.name} looks dissappointed but understands."""):
                room.adjustments[1].append(self.service)
                self.charge_fee(player, action_word)

    def charge_fee(self, player, action_word):
        if sum(1 for each_item in player.inventory.misc if each_item.name == "BLADE OF GRASS") >= 20:
            for x in range(20):
                self.inventory.append(misc_options["BLADE OF GRASS"])
                player.inventory.misc.remove(misc_options["BLADE OF GRASS"])
        else: 
            self.dollar_bills += self.price
            player.inventory.dollar_bills -= self.price

#---------------------------------------------------------

class ShopOwner(Merchant):

    def __init__(self, number, action_words, descriptor, name, pronouns, convo, invest_requirement, inventory, markup=1.5):
        self.markup = markup
        super().__init__(
            number=number, 
            action_words=action_words, 
            descriptor=descriptor, 
            name = name,
            pronouns = pronouns,
            convo = convo,
            invest_requirement=invest_requirement, 
            inventory = inventory,
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "TALK" and "TALK" in self.action_words:
            self.talk()
        elif action_word == "ROB" and "ROB" in self.action_words:
            self.attempt_robbery(player)
        elif action_word == "BUY" and "BUY" in self.action_words:
            self.run_buy_sequence(player)
        elif action_word == "SELL" and "SELL" in self.action_words:
            self.run_sell_sequence(player)

    def run_buy_sequence(self, player):
        if self.refresh_requirement == 100000: print(f""" {self.name}: {self.convo[2]} """)
        elif len(self.inventory) <= 0: print(f""" {self.name}: {self.convo[7]}""")
        else: 
            products = self.build_buy_product_list()
            selection_loop = True
            while selection_loop == True:
                print(f"""\n {self.name}: {self.convo[6]} """)
                print(" PRICE | PRODUCT | STOCK")
                for each_product in products:
                    if math.ceil(each_product.value * self.markup) <= 9:
                        print(f""" {math.ceil(each_product.value * self.markup)}  | {each_product.name} x{sum(1 for each_item in self.inventory if each_item.name == each_product.name)}""")
                    else: print(f""" {math.ceil(each_product.value * self.markup)} | {each_product.name} x{sum(1 for each_item in self.inventory if each_item.name == each_product.name)}""")
                print(" NEVERMIND")
                selection = input("\n - ").upper()
                if selection == "NEVERMIND": selection_loop = False
                for each_product in products:
                    if selection == each_product.name:
                        selection_loop = self.confirm_buy_details(player, each_product)
                if selection_loop == True: print(f""" {self.name}: Sorry, no can do. Buy something else?""")

    def build_buy_product_list(self):
        products = []
        for each_item in self.inventory:
            if each_item.name not in products: products.append(each_item.name)
        for each_item in self.inventory:
            if each_item.name in products: products[products.index(each_item.name)] = each_item
        return products
    
    def confirm_buy_details(self, player, product):
        if product.type == "CONSUMABLE": print(f""" {product.name}- {product.description}""")
        elif product.type == "ARMOR": print(f""" {product.name}- Sets DEFENSE to {product.defense}.""")
        elif product.type == "WEAPON": print(f""" {product.name}- Weapon rank {product.rating}/8.""")
        elif product.name == "SHIELD": print(f""" {product.name}- Raises DEFENSE by 1 while in your inventory.""")
        elif product.name == "MAGIC BRIDGE": print(f""" {product.name}- Can be placed over any barrier that requires a bridge and reclaimed once crossed.""")
        quantity = self.determine_quantity(self.inventory, product, "NPC")
        if quantity > 0: 
            if player.inventory.dollar_bills >= math.ceil(product.value * self.markup * quantity):
                confirm = confirm_sequence(f""" {self.name}: {quantity} {product.name} for {math.ceil(product.value * self.markup * quantity)} dollar bills?""", f"""\n {self.name}: {self.convo[4]}""", f""" {self.name} looks dissapointed but understands.""")
                if confirm: 
                    self.buy_product(player, product, quantity)
            else: print(f""" {self.name}: You don't have enough dollar bills though!""")
        else: print(f""" {self.name} looks dissapointed but understands.""")
        return False

    def buy_product(self, player, product, quantity):
            if quantity == 1: print(f""" You bought {self.name}'s {product.name}!""")
            else: print(f""" You bought {quantity} of {self.name}'s {product.name}!""")
            for i in range(quantity): player.inventory.add_item(product)
            player.inventory.dollar_bills -= math.ceil(product.value * self.markup * quantity)
            self.dollar_bills += math.ceil(product.value * self.markup * quantity)
            updated_inventory = []
            for each_item in self.inventory:
                if quantity > 0 and each_item.name == product.name: quantity -= 1
                else: updated_inventory.append(each_item)
            self.inventory = updated_inventory

#---------------------------------------------------------

class Owl(RedHerring):

    def __init__(self):
        super().__init__(
            type="OWL", 
            action_words=["PET", "HOOT", "WAVE ARMS", "GLARE BACK"],
            description="A great horned owl perched on a rocky outcropping. It's glaring at you with a big frown.", 
            punchline = " It keeps glaring at you."
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "PET":
            print(" It's too far away to reach." + self.punchline)
        if action_word == "HOOT":
            print(" You mimic the owl, it doesn't look amused.")
        if action_word == "WAVE ARMS":
            print(" You flap around at the owl and look kinda stupid." + self.punchline)
        if action_word == "GLARE BACK":
            print(" It's a staring contest. The owl wins and you feel a little stupid." + self.punchline)


#-------------------------------------------------------
#------------ INDEPENDENT INTERACTABLES ----------------
#-------------------------------------------------------

class Pool(Interactable):

    def __init__(self, number, action_words, descriptor):
        self.healing_available = True
        self.event_num = random.randint(1,2)
        self.exit_hold = None
        self.words_hold = None
        super().__init__(
            type="POOL", 
            number=number, 
            action_words=action_words, 
            description=descriptor, 
            invest_requirement=0, 
            stealth_mod=0
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "SWIM" and "SWIM" in self.action_words:
            if "INSPECT SHADOW" in self.action_words and self.event_num == 1:
                run_sea_creature(room, player)
            elif player.inventory.armor.rating == 3 or player.inventory.armor.rating == 4:
                self.run_heavy_swim(player)
            elif "INSPECT SHADOW" in self.action_words and self.event_num == 2:
                self.run_find_chest(room)
            elif self.healing_available == True:
                self.run_healing_swim(player)
            else: print("You took another swim in the water! You're gonna get pruny if you keep this up!")
        elif action_word == "THROW ROCKS" and "THROW ROCKS" in self.action_words:
            print(f""" You throw some rocks into the water, it makes a lot of noise. \n You skip one rock {random.randint(1,6)} times!""")
            room.spawn_monster()
        elif action_word == "INSPECT SHADOW" and "INSPECT SHADOW" in self.action_words:
            print(" You can't inspect the SHADOW from outside the pool.")

    def run_healing_swim(self, player):
        if player.current_health == player.max_health: print(" Your health is currently full. Come back later to regain some in the POOL.")
        else:
            print(" You took a quick dip in the refreshing water!")
            player.recover_health(4)
            self.healing_available = False

    def run_heavy_swim(self, player):
        print(f""" Your {player.inventory.armor.name} is too heavy to swim in!""")
        player.take_damage(2, True)
        print(" You make it back to solid ground. Swimming in heavy armor could lead to drowning.")
    
    def run_find_chest(self, room):
        self.action_words.remove("INSPECT SHADOW")
        print(" You found a locked chest!")
        room.description = "A room with a small pond."
        room.interactables.append(Chest(2, ["BREAK THE LOCK", "USE A KEY"]," with a rusted lock.", 2, [HealthPotion(), DurabilityGem(), 15]))

#---------------------------------------------------------

class Cauldron(Interactable):

    def __init__(self, action_words=["RELIGHT FIRE", "COOK"], fire_lit=False):
        self.fire_lit = fire_lit
        super().__init__(
            type="CAULDRON", 
            number=0, 
            action_words=action_words, 
            description="A large cauldron", 
            invest_requirement=0, 
            stealth_mod=2
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "RELIGHT FIRE" and "RELIGHT FIRE" in self.action_words:
            self.relight(player, room)
        if action_word == "COOK" and "COOK" in self.action_words:
            if len(room.monsters) > 0: print(" It's too dangerous to cook with monsters nearby!")
            else:
                ingredient_options = self.determine_elegibility(player)
                if len(ingredient_options) > 0: 
                    ingredient = self.select_ingredient(ingredient_options)
                    self.cook(player, ingredient)
                

    def relight(self, player, room):
        if misc_options["WOOD"] in player.inventory.misc:
            print(" You used some WOOD to relight the fire under the CAULDRON!")
            player.inventory.misc.remove(misc_options["WOOD"])
            self.fire_lit = True
            self.action_words.remove("RELIGHT FIRE")
            room.adjustments[2]["change_room_description"][0] = room.visits
        else: print(" You don't have any WOOD to light a new fire.")

    def determine_elegibility(self, player):
        ingredient_options = []
        if self.fire_lit == True:
            if misc_options["SEA CREATURE MEAT"] in player.inventory.misc: ingredient_options.append(misc_options["SEA CREATURE MEAT"])
            if misc_options["GLOWING FRUIT"] in player.inventory.misc: ingredient_options.append(misc_options["GLOWING FRUIT"])
            if player.inventory.misc.count(misc_options["APPLES"]) >= 4: ingredient_options.append(misc_options["APPLES"])
            elif misc_options["APPLES"] in player.inventory.misc: ingredient_options.append(misc_options["NOT ENOUGH APPLES"])
            if len(ingredient_options) == 0: print(" You don't have any ingredients to cook.")
        else: print(" You need to light the fire if you're going to cook in the cauldron.")
        return ingredient_options

    def select_ingredient(self, ingredient_options):
        ingredient = None
        selection_loop = True
        while selection_loop == True:
            print(" What would you like to cook with?")
            for each_option in ingredient_options:
                print(f""" {each_option.name}""")
            print(" NEVERMIND")
            selection = input("\n - ").upper()
            if selection == "NEVERMIND": selection_loop = False
            for each_option in ingredient_options:
                if each_option.name == selection:
                    ingredient = each_option
                    selection_loop = False
            if selection_loop == True: print(f"""\n {selection} is not an option.""")
        return ingredient
    
    def cook(self, player, ingredient):
        if ingredient is not None:
            if ingredient.name == "NOT ENOUGH APPLES": print(" You can't cook with apples when you don't have enough.")
            else:
                print(f""" Good thing you always carry some spare flour! You cooked some of the {ingredient.name} into a PIE!""")
                player.inventory.misc.remove(ingredient)
                player.inventory.add_item(Pie())
                if ingredient == misc_options["APPLES"]:
                    for x in range(0, 3):
                        player.inventory.misc.remove(ingredient)

#---------------------------------------------------------

class Bed(Breakable):

    def __init__(self, number, type, action_words, descriptor, amount):
        self.healing_available = True
        self.amount = amount
        super().__init__(
            type=type, 
            number=number, 
            action_words=action_words, 
            description=descriptor, 
            invest_requirement=0, 
            stealth_mod=0,
            challenge=0,
            contents=misc_options["WOOD"]
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "REST" and "REST" in self.action_words:
            self.rest(player)
        elif action_word == "CHOP" and "CHOP" in self.action_words:
            run_shatter(self, player, room)

    def rest(self, player):
        if self.healing_available == False: print(" You probably shouldn't nap too much, or it'll be harder to get back up.")
        elif player.current_health == player.max_health: print(" Your health is currently full. Come back later to get some rest.")
        else:
            print(f""" You took a quick nap on the {self.type}!""")
            player.recover_health(self.amount)
            self.healing_available = False
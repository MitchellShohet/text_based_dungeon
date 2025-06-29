import random, math
from abc import ABC, abstractmethod
from classes.dungeon.room_components import Interactable
from classes.combatants.combatant import Combatant
from classes.dungeon.room import Room
from classes.dungeon.room_components import Exit, MonsterSpawning
from classes.inventory.inventory import Inventory
from classes.inventory.items import Weapon
from lists.monsters_list import Goblin, Skeleton, Wizard, MudGolem, Minotaur, SeaCreature
from lists.items_lists import weapon_options, armor_options, misc_options, HealthPotion, Pie, StatMedallion, PowerBerry, DurabilityGem, SmokeBomb, GreaterHealthPotion
from lists.adjustments_list import check_for_heavy_armor


#-------------------------------------------------------
#----------- PARENT INTERACTABLES ----------------------
#-------------------------------------------------------

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
        if action_word == "JUMP" and "JUMP" in self.action_words:
            self.jump(player, room)
        elif action_word == "BUILD BRIDGE" and "BUILD BRIDGE" in self.action_words:
            self.use_bridge(player)
        elif action_word == "CROSS THE BRIDGE" and "CROSS THE BRIDGE" in self.action_words:
            self.cross_bridge(player, room)
        elif action_word == "THROW ROCKS" and "THROW ROCKS" in self.action_words:
                self.throw_rocks(room)

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

    def use_bridge(self, player):
        if misc_options["MAGIC BRIDGE"] in player.inventory.misc:
            print(f""" You placed the MAGIC BRIDGE over the {self.type}!""")
            self.bridge = "MAGIC"
            player.inventory.misc.remove(misc_options["MAGIC BRIDGE"])
            self.action_words.remove("BUILD BRIDGE")
            self.action_words.append("CROSS THE BRIDGE")
        elif misc_options["WOOD"] in player.inventory.misc:
            wood_count = 0
            for each_item in player.inventory.misc:
                if each_item.name == "WOOD": wood_count += 1
            if wood_count >= 3:
                print(f""" You built a WOOD BRIDGE across the {self.type}!""")
                self.bridge = "WOOD"
                for x in range(3):
                    player.inventory.misc.remove(misc_options["WOOD"])
                self.action_words.remove("BUILD BRIDGE")
                self.action_words.append("CROSS THE BRIDGE")
        else: print(" You don't have the materials to build a bridge.")

    def cross_bridge(self, player, room):
        print(f""" You crossed the {self.bridge} BRIDGE over the {self.type}""")
        if self.bridge == "WOOD":
            self.wood_failure(player, room)
            
    @abstractmethod
    def jump_failure(self, jump_score, player, room):
        pass

    @abstractmethod
    def wood_failure(self, player, room):
        pass

    @abstractmethod
    def throw_rocks(self, room):
        pass

#---------------------------------------------------------

class NPC(Interactable):

    def __init__(self, number, action_words, descriptor, name, pronouns, convo, invest_requirement, inventory=[misc_options["APPLES"]]):
        self.name = name
        self.pronouns = pronouns
        self.convo = convo
        self.inventory = inventory
        self.dollar_bills = invest_requirement*4
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
        elif player.hiding_score >= self.invest_requirement * 1.7:
            if self.dollar_bills < 30: self.dollar_bills += 30
            print(f""" You robbed {self.name} a little without {self.pronouns[1]} noticing!""")
            print(f""" You got 1 {self.inventory[0].name}!""")
            print(f""" You got {self.dollar_bills} dollar bills!""")
            player.inventory.add_item(self.inventory[0])
            player.inventory.dollar_bills += self.dollar_bills
            self.inventory.pop(0)
            self.dollar_bills = 0
            self.invest_requirement = math.ceil(self.invest_requirement * 1.4)
        else:
            print(f""" {self.name}: {self.convo[1]}""")
            print(f""" {self.name} caught you trying to rob {self.pronouns[1]}""")
            print(f""" You still managed to swipe a {self.inventory[0].name}""")
            player.inventory.add_item(self.inventory[0])
            self.inventory.pop(0)
            self.refresh_requirement = 100000
            self.invest_requirement = math.ceil(self.invest_requirement * 1.7)
        self.action_words.remove("ROB")

#---------------------------------------------------------

class Tree(Interactable): #make a child class for MagicTree(Tree)

    def __init__(self, number, action_words, descriptor, stealth_mod=1, challenge=0):
        self.challenge = challenge
        self.gift_given = False
        super().__init__(
            type="TREE", 
            number=number, 
            action_words=action_words, 
            description="A" + descriptor + " tree.", 
            invest_requirement=challenge, 
            stealth_mod=stealth_mod
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "PICK FRUIT" and "PICK FRUIT" in self.action_words:
            if self.challenge >= 6:
                print(" You picked some of the tree's GLOWING FRUIT!")
                player.inventory.add_item(misc_options["GLOWING FRUIT"])
            else:
                print(" You picked some of the tree's APPLES!")
                player.inventory.add_item(misc_options["APPLES"])
            self.action_words.remove("PICK FRUIT")
        elif action_word == "CHOP" and "CHOP" in self.action_words:
            tree_def = Combatant("TREE", 1, 1, 3, self.challenge, Inventory(weapon=Weapon(0, "WEAPON", "", self.challenge/5, self.challenge, self.challenge, self.challenge, 0)), self.number)
            if self.challenge >= 5 and self.gift_given == True:
                print(" Betrayed, the GLOWING TREE attacks you with it's magic!")
                tree_def.make_attack(player)
            player.make_attack(tree_def)
            if tree_def.current_health <= 0:
                print(" You got 1 WOOD!")
                player.inventory.add_item(misc_options["WOOD"])
                self.type = "CHOPPED TREE"
                for each_interactable in room.interactables:
                    if each_interactable.type == "CHOPPED TREE": room.interactables.remove(each_interactable)
            elif self.challenge >= 6:
                print(" The GLOWING TREE hardened itself with magic. You can no longer CHOP or INSPECT it.")
                self.action_words.remove("CHOP")
                if "INSPECT" in self.action_words: self.action_words.remove("INSPECT")
                self.action_words.append("APOLOGIZE")
        elif action_word == "INSPECT" and "INSPECT" in self.action_words:
            if player.investigation + random.randint(1,5) >= self.invest_requirement:
                self.invest_requirement = 0
                print(" After some time you start to understand the secrets of the GLOWING TREE. The tree feels seen and offers you a gift from its branches.")
                if self.challenge == 6:
                    reward = StatMedallion()
                    monster = Wizard()
                    monster.number = self.number
                elif self.challenge == 10:
                    reward = armor_options["PLATEMAIL"]
                    monster = MudGolem()
                    monster.number = self.number
                elif self.challenge == 15:
                    reward = weapon_options["MAGIC SWORD"]
                    monster = Minotaur()
                    monster.number = room.monster1_number
                    room.monster1_number += 1
                    room.monster1_count += 1
                print(f""" The GLOWING TREE gifted you a {reward.name}!""")
                player.inventory.add_item(reward)
                self.gift_given = True
                print(f""" A {monster.type} has come to test you.""")
                room.monsters.append(monster)
            else: print(f""" The secrets of the GLOWING TREE elude you. It will allow you to try again later.""") #add the adjustment function for this upon returning
            self.action_words.remove("INSPECT")
        elif action_word == "APOLOGIZE" and "APOLOGIZE" in self.action_words: print(" The GLOWING TREE does not accept your apology.")

#-------------------------------------------------------
#--------------- CHILD INTERACTABLES -------------------
#-------------------------------------------------------

class MagmaRiver(Crossing):

    def __init__(self, number, action_words, descriptor):
        super().__init__(
            type="MAGMA RIVER", 
            number=number, 
            action_words=action_words, 
            description="A 10ft wide river of flowing lava." + descriptor, 
            exit_hold = Exit(1, Room("Magma River Passage", 
                                        "A tunnel beyond the magma river opens to a chamber with a chest. The path forks into two exits onward.", 
                                        [Exit(0), Exit(1), Exit(2)], 
                                        MonsterSpawning(5, Goblin, 9, "twice"), 
                                        [Chest(3, ["BREAK THE LOCK", "USE A KEY"]," with an image of a volcano etched onto its top.",contents=[weapon_options["LONGSWORD"], StatMedallion(), 40])])),
            jump_challenge=7,
            bridge=None,
            invest_requirement=0, 
            stealth_mod=0
            )

    def jump_failure(self, jump_score, player, room):
        if jump_score == 1:
            print(" The ash in the room choking you, you attempt to leap across the MAGMA RIVER and land less than halfway across.")
            player.take_damage(random.randint(7,11), True)
            if player.current_health > 0: print(" You make it back onto land. You weren't able to cross, but you did survive jumping into lava.")
        elif jump_score > 1 and jump_score < 7:
            print(" With a running start you successfully leap most of the way accross MAGMA RIVER! You land just short of the opposite bank.")
            player.take_damage(random.randint(2,4), True)
            if player.current_health > 0:
                print(" You made it to the opposite bank with minimal burns considering you jumped a MAGMA RIVER. However the way behind you is now blocked.")
                self.switch_sides(room)

    def wood_failure(self, player, room):
        print(" Afterward the bridge catches fire and incinerates. The opposite side is blocked by the MAGMA RIVER again.")
        self.action_words.append("BUILD BRIDGE")
        self.action_words.append("JUMP")
        self.action_words.remove("CROSS THE BRIDGE")
        self.switch_sides(room)

    def throw_rocks(self, room):
        print(f""" You throw some rocks into the lava, they sink immediately.""")
        room.spawn_monster()

#---------------------------------------------------------

class Chest(Interactable): #make a parent class for Lockable(Interactable)

    def __init__(self, number, action_words, descriptor, challenge=0, contents=[10]):
        self.challenge = challenge
        self.contents = contents
        super().__init__(
            type="CHEST", 
            number=number, 
            action_words=action_words, 
            description="A treasure chest" + descriptor, 
            invest_requirement=number, 
            stealth_mod=1
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "OPEN" and "OPEN" in self.action_words:
            if self.challenge > 0: self.select_unlock_method(player, room)
            else: self.open(player)
        elif action_word == "BREAK THE LOCK" and "BREAK THE LOCK" in self.action_words:
            self.attempt_to_break(player, room)
        elif action_word == "USE A KEY" and "USE A KEY" in self.action_words:
            self.use_key(player, room)
    
    def open(self, player):
        print(" You opened the CHEST!")
        reward_num = random.randint(1, len(self.contents))-1
        try:
            self.contents[reward_num].type
            player.inventory.add_item(self.contents[reward_num])
            print(f""" You found a {self.contents[reward_num].name}!""")
        except: 
            player.inventory.dollar_bills += self.contents[reward_num]
            print(f""" You found {self.contents[reward_num]} dollar bills!""")
        self.action_words.remove("OPEN")

    def select_unlock_method(self, player, room):
        selection_loop = True
        while selection_loop == True:
            print(" The CHEST is locked. How would you like to open it?")
            for each_option in self.action_words:
                print(f"""{each_option}""")
            print("NEVERMIND")
            selection = input("- ").upper()
            if selection == "NEVERMIND": selection_loop = False
            for each_option in self.action_words:
                if selection == each_option:
                    self.run_interaction(selection, player, room)
                    selection_loop = False
            if selection_loop == True: print(" That's not an option here.")

    def attempt_to_break(self, player, room):
        chest_def = Combatant("THE LOCK", 1, 1, 0, self.challenge, Inventory())
        player.make_attack(chest_def)
        if chest_def.current_health <= 0: self.unlock_success(player, room)
        else:
            print(" You jammed the lock into the closed position. You can try again but it'll be even more difficult now.")
            self.challenge*=2
            self.description += " It's lock has been jammed closed."
    
    def use_key(self, player, room):
        if misc_options["KEY"] in player.inventory.misc:
            player.inventory.misc.remove(misc_options["KEY"])
            print(" You used your key to open the lock. The key then dissintegrates, it's task in this world complete.")
            self.unlock_success(player, room)
        else: print(" You don't have a key to use.")

    def unlock_success(self, player, room):
        self.challenge = 0
        self.action_words.remove("BREAK THE LOCK")
        self.action_words.remove("USE A KEY")
        self.action_words.append("OPEN")
        self.run_interaction("OPEN", player, room)

#---------------------------------------------------------

class ShopOwner(NPC):

    def __init__(self, number, action_words, descriptor, name, pronouns, convo, invest_requirement, inventory):
        super().__init__(
            number=number, 
            action_words=action_words, 
            description=descriptor, 
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
        elif len(self.inventory) <= 0: print(f""" {self.name}: {self.convo[5]}""")
        else: 
            products = self.build_buy_product_list()
            selection_loop = True
            while selection_loop == True:
                print(f"""\n {self.name}: {self.convo[3]} """)
                print(" PRICE | PRODUCT | STOCK")
                for each_product in products:
                    if math.ceil(each_product.value * 1.5) <= 9:
                        print(f""" {math.ceil(each_product.value * 1.5)}  | {each_product.name} x{sum(1 for each_item in self.inventory if each_item.name == each_product.name)}""")
                    else: print(f""" {math.ceil(each_product.value * 1.5)} | {each_product.name} x{sum(1 for each_item in self.inventory if each_item.name == each_product.name)}""")
                print(" NEVERMIND")
                selection = input("\n - ").upper()
                if selection == "NEVERMIND": selection_loop = False
                for each_product in products:
                    if selection == each_product.name:
                        selection_loop = self.buy_product(player, each_product)
                if selection_loop == True: print(f" Sorry, no can do. Buy something else?")

    def build_buy_product_list(self):
        products = []
        for each_item in self.inventory:
            if each_item.name not in products: products.append(each_item.name)
        for each_item in self.inventory:
            if each_item.name in products: products[products.index(each_item.name)] = each_item
        return products
    
    def buy_product(self, player, product):
        if player.inventory.dollar_bills >= math.ceil(product.value * 1.5):
            print(f"""\n {self.name}: {self.convo[4]}""")
            print(f""" You bought {self.name}'s {product.name}!""")
            player.inventory.add_item(product)
            player.inventory.dollar_bills -= math.ceil(product.value * 1.5)
            self.dollar_bills += math.ceil(product.value * 1.5)
            self.inventory.remove(product)
            return False
        else: print(" You don't have enough dollar bills though!")
        return True

    def run_sell_sequence(self, player):
        if self.refresh_requirement == 100000: print(f""" {self.convo[2]} """)
        elif len(player.inventory.misc + player.inventory.consumables) <= 0: print(f""" {self.name}: {self.convo[7]}""")
        else:
            all_options = self.build_sell_product_list(player)
            selection_loop = True
            while selection_loop == True:
                print(f""" {self.name}: {self.convo[6]}""")
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
                        quantity = self.determine_quantity(player, each_product)
                        if quantity > 0: self.sell_product(player, each_product, quantity)
                        else: print(f""" {self.name} looks dissapointed but understands.""")
                        selection_loop = False
                if selection_loop == True: print(f""" You don't have any {selection} to sell.""")

    def build_sell_product_list(self, player):
        all_options = []
        for each_misc in player.inventory.misc:
            if each_misc.name not in all_options: all_options.append(each_misc.name)
        for each_misc in player.inventory.misc:
            if each_misc.name in all_options: all_options[all_options.index(each_misc.name)] = each_misc
        for each_consumable in player.inventory.consumables:
            if each_consumable.name not in all_options: all_options.append(each_consumable.name)
        for each_consumable in player.inventory.consumables:
            if each_consumable.name in all_options: all_options[all_options.index(each_consumable.name)] = each_consumable
        return all_options
    
    def determine_quantity(self, player, product): #Might be able to allow purchasing multiples with some adjusting, would we want to?
        quantity = 1
        if sum(1 for each_item in player.inventory.misc if each_item.name == product.name) + sum(1 for each_item in player.inventory.consumables if each_item.name == product.name) > 1:
            quantity_loop = True
            while quantity_loop == True:
                print(f""" You have {sum(1 for each_item in player.inventory.misc if each_item.name == product.name) + sum(1 for each_item in player.inventory.consumables if each_item.name == product.name)} {product.name}. How many would you like to sell?""")
                quantity = (input(" - "))
                try: int(quantity)
                except: print(" Please input a number.")
                else: 
                    quantity = int(quantity)
                    if quantity > sum(1 for each_item in player.inventory.misc if each_item.name == product.name) + sum(1 for each_item in player.inventory.consumables if each_item.name == product.name): print(f""" You don't have that many {product.name}.""")
                    elif quantity < 0: print(" You cannot sell a negative amount.")
                    elif quantity == 0: 
                        print(" Cancel your sale?")
                        command = input(" - ").upper()
                        if command == "YES" or command == "YEAH" or command == "YEP" or command == "Y": quantity_loop = False
                    else: quantity_loop = False
        return quantity
    
    def sell_product(self, player, product, quantity):
        print(f""" {self.name}: {self.convo[4]}""")
        print(f""" You sold {quantity} {product.name} to {self.name} for {math.ceil(product.value * .75) * quantity} dollar bills!""")
        for x in range(0, quantity):
            self.inventory.append(product)
            if self.dollar_bills >= math.ceil(product.value * .75) + 30: self.dollar_bills -= math.ceil(product.value * .75)
            player.inventory.dollar_bills += math.ceil(product.value * .75)
            player.inventory.remove_item(product)

#-------------------------------------------------------
#------------ INDEPENDENT INTERACTABLES ----------------
#-------------------------------------------------------

class Pool(Interactable):

    def __init__(self, number, action_words, descriptor):
        self.healing_available = True
        self.event_num = random.randint(1,2) #add the third for the body?
        self.exit_hold = None
        super().__init__(
            type="POOL", 
            number=number, 
            action_words=action_words, 
            description="A pool of water " + descriptor, 
            invest_requirement=0, 
            stealth_mod=0
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "SWIM" and "SWIM" in self.action_words:
            if "INSPECT SHADOW" in self.action_words and self.event_num == 1:
                self.run_sea_creature(player, room)
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
            self.healing_available == False

    def run_heavy_swim(self, player):
        print(f""" Your {player.inventory.armor.name} is too heavy to swim in!""")
        player.take_damage(2, True)
        print(" You make it back to solid ground. Swimming in heavy armor could lead to drowning.")
    
    def run_find_chest(self, room):
        self.action_words.remove("INSPECT SHADOW")
        print(" You found a chest!")
        room.description = "A room with a small pond."
        room.interactables.append(Chest(2, ["BREAK THE LOCK", "USE A KEY"]," with a rusted lock.", contents=[HealthPotion(), DurabilityGem(), 15]))

    def run_sea_creature(self, player, room):
        print(" You feel something wrap around your leg and pull you under the water!")
        room.spawn_monster(SeaCreature)
        for each_monster in room.monsters: 
            if each_monster.type == "SEA CREATURE": each_monster.is_aware = True
        self.action_words.clear()
        self.exit_hold = room.exits
        room.exits = None
        player.hiding = True
        if player.inventory.armor.rating == 3 or player.inventory.armor.rating == 4: room.adjustments[1].append(check_for_heavy_armor)

#---------------------------------------------------------

class GlowingCrystal(Interactable):

    def __init__(self, number, action_words, descriptor):
        if self.number == 1: self.contents = misc_options["RUBY DUST"]
        elif self.number == 2: self.contents = DurabilityGem()            
        elif self.number == 3: self.contents = StatMedallion()
        super().__init__(
            type="GLOWING CRYSTAL", 
            number=number, 
            action_words=action_words, 
            description="A large cluster of gems with a mysterious light sourced from within. Roughly the size of a" + descriptor, 
            invest_requirement=number*3, 
            stealth_mod=number
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "SHATTER" and "SHATTER" in self.action_words:
            self.run_shatter(player)
        elif action_word == "INSPECT" and "INSPECT" in self.action_words:
            self.run_inspect(player)
    
    def run_shatter(self, player):
        crystal_def = Combatant("GLOWING CRYSTAL", 1, 1, 0, self.number*3+2, Inventory(), self.number)
        player.make_attack(crystal_def)
        if crystal_def.current_health <= 0:
            player.inventory.add_item(self.contents)
            print(f""" You found 1 {self.contents.name}""")
            if "INSPECT" in self.action_words: self.action_words.remove("INSPECT")
            self.type = "DESTROYED CRYSTAL PILE"
            self.description = "The shattered remains of what used to by a GLOWING CRYSTAL"
            self.stealth_mod-=1
        else: print(f""" You couldn't break GLOWING CRYSTAL {self.number}.""")
        self.action_words.remove("SHATTER")

    def run_inspect(self, player):
        if player.investigation + random.randint(1,5) >= self.invest_requirement:
            self.invest_requirement = 0
            print(" After some time you start to understand the secrets of the GLOWING CRYSTAL.  You're able to extract the magic and recover some health.")
            if player.current_health == player.max_health: print(" Your health is currently full. Come back later to regain some from the GLOWING CRYSTAL.")
            else:
                player.recover_health(self.number*3)
                self.action_words.remove("INSPECT")
        else:
            print(f""" The secrets of GLOWING CRYSTAL {self.number} elude you.""")
            self.action_words.remove("INSPECT")


#---------------------------------------------------------

class Cauldron(Interactable):

    def __init__(self, number, action_words, descriptor):
        self.fire_lit = False
        super().__init__(
            type="CAULDRON", 
            number=number, 
            action_words=action_words, 
            description="A large cauldron" + descriptor, 
            invest_requirement=0, 
            stealth_mod=2
            )
        
    def run_interaction(self, action_word, player, room):
        if action_word == "RELIGHT FIRE" and "RELIGHT FIRE" in self.action_words:
            self.relight(player)
        if action_word == "COOK" and "COOK" in self.action_words:
            ingredient_options = self.determin_elegibility(player)
            if len(ingredient_options) > 0: 
                ingredient = self.select_ingredient(ingredient_options)
                self.cook(player, ingredient)
                

    def relight(self, player):
        if misc_options["WOOD"] in player.inventory.misc:
            print(" You used some WOOD to relight the fire under the CAULDRON!")
            player.inventory.misc.remove(misc_options["WOOD"])
            self.fire_lit = True
            self.action_words.remove("RELIGHT FIRE")
        else: print(" You don't have any WOOD to light a new fire.")

    def determin_elegibility(self, player):
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


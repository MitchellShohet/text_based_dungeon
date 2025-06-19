import random
from classes.dungeon.room_components import Interactable
from classes.combatants.combatant import Combatant
from classes.dungeon.room import Room
from classes.dungeon.room_components import Exit, MonsterSpawning
from classes.inventory.inventory import Inventory
from classes.inventory.items import Weapon
from lists.monsters_list import Goblin, Skeleton, Wizard, MudGolem, Minotaur, SeaCreature
from lists.items_lists import weapon_options, armor_options, misc_options, HealthPotion, StatMedallion, PowerBerry, DurabilityGem, SmokeBomb, GreaterHealthPotion

class Pool(Interactable):

    def __init__(self, number, action_words, descriptor):
        self.healing_available = True
        self.event_num = random.randint(1,2) #add the third for the body
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
            if player.inventory.armor.rating == 3 or player.inventory.armor.rating == 4:
                print(f""" Your {player.inventory.armor.name} is too heavy to swim in!""")
                player.take_damage(2, True)
                self.action_words.append("DROWNING")
            if "INSPECT SHADOW" in self.action_words and self.event_num == 1:
                print(" You feel something wrap around your leg and pull you under the water!")
                room.spawn_monster(SeaCreature)
                self.action_words.append("SKIP")
                self.action_words.remove("INSPECT SHADOW")
                self.action_words.remove("SWIM")
                self.action_words.remove("THROW ROCKS")
                if "DROWNING" in self.action_words:
                    self.action_words.remove("DROWNING")
                self.exit_hold = room.exits
                room.exits = None
            if "DROWNING" in self.action_words and player.current_health > 0:
                print(" You make it back to solid ground. Swimming in heavy armor could lead to drowning.")
                self.action_words.remove("DROWNING")
            elif "SKIP" in self.action_words:
                self.action_words.remove("SKIP")
            elif "INSPECT SHADOW" in self.action_words and self.event_num == 2:
                self.action_words.remove("INSPECT SHADOW")
                print(" You found a chest!")
                room.description = "A room with a small pond."
                room.interactables.append(Chest(2, ["BREAK THE LOCK", "USE A KEY"]," with a rusted lock.", contents=[HealthPotion(), DurabilityGem(), 15]))
            elif self.healing_available == True:
                if player.current_health == player.max_health:
                    print(" Your health is currently full. Come back later to regain some in the POOL.")
                else:
                    print(" You took a quick dip in the refreshing water!")
                    player.recover_health(4)
                    self.healing_available == False
            else:
                print("You took another swim in the water! You're gonna get pruny if you keep this up!")
        elif action_word == "THROW ROCKS" and "THROW ROCKS" in self.action_words:
            print(f""" You throw some rocks into the water, it makes a lot of noise. \n You skip one rock {random.randint(1,6)} times!""")
            room.spawn_monster()
        elif action_word == "INSPECT SHADOW" and "INSPECT SHADOW" in self.action_words:
            print(" You can't inspect the SHADOW from outside the pool.")


#---------------------------------------------------------

class GlowingCrystal(Interactable):

    def __init__(self, number, action_words, descriptor):
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
                crystal_def = Combatant("GLOWING CRYSTAL", 1, 1, 0, self.number*3+2, Inventory(), self.number)
                player.make_attack(crystal_def)
                if crystal_def.current_health <= 0:
                    if self.number == 1:
                        player.inventory.add_item(misc_options["RUBY DUST"])
                        print(f""" You found some RUBY DUST""")
                    if self.number == 2:
                        player.inventory.add_item(DurabilityGem())
                        print(f""" You found a DURABILITY GEM""")
                    if self.number == 3:
                        player.inventory.add_item(StatMedallion())
                        print(f""" You found a STAT MEDALLION""")
                    if "INSPECT" in self.action_words:
                        self.action_words.remove("INSPECT")
                    self.type = "DESTROYED CRYSTAL PILE"
                    self.description = "The shattered remains of what used to by a GLOWING CRYSTAL"
                    self.stealth_mod-=1
                else:
                    print(f""" You couldn't break GLOWING CRYSTAL {self.number}.""")
                self.action_words.remove("SHATTER")
        elif action_word == "INSPECT" and "INSPECT" in self.action_words:
                if player.investigation + random.randint(1,5) >= self.invest_requirement:
                    self.invest_requirement = 0
                    print(" After some time you start to understand the secrets of the GLOWING CRYSTAL.  You're able to extract the magic and recover some health.")
                    if player.current_health == player.max_health:
                        print(" Your health is currently full. Come back later to regain some from the GLOWING CRYSTAL.")
                    else:
                        player.recover_health(self.number*3)
                        self.action_words.remove("INSPECT")
                else:
                    print(f""" The secrets of GLOWING CRYSTAL {self.number} elude you.""")
                    self.action_words.remove("INSPECT")
                
#---------------------------------------------------------

class MagmaRiver(Interactable):

    def __init__(self, number, action_words, descriptor):
        self.exit_hold = Exit(1, Room("Magma River Passage", 
                                    "A tunnel beyond the magma river opens to a chamber with a chest. The path forks into two exits onward.", 
                                    [Exit(0), Exit(1), Exit(2)], 
                                    MonsterSpawning(5, Goblin, 9, "twice"), 
                                    [Chest(3, ["BREAK THE LOCK", "USE A KEY"]," with an image of a volcano etched onto its top.",contents=[weapon_options["LONGSWORD"], StatMedallion(), 40])]))
        super().__init__(
            type="MAGMA RIVER", 
            number=number, 
            action_words=action_words, 
            description="A 10ft wide river of flowing lava." + descriptor, 
            invest_requirement=0, 
            stealth_mod=0
            )

    def run_interaction(self, action_word, player, room):
        if action_word == "JUMP" and "JUMP" in self.action_words:
            jump_score = random.randint(1,8)
            if jump_score == 1:
                print(" The ash in the room choking you, you attempt to leap across the MAGMA RIVER and land less than halfway across.")
                player.take_damage(random.randint(7,11), True)
                if player.current_health > 0:
                    print(" You make it back onto land. You weren't able to cross, but you did survive jumping into lava.")
            elif jump_score > 1 and jump_score < 7:
                print(" With a running start you successfully leap most of the way accross MAGMA RIVER! You land just short of the opposite bank.")
                player.take_damage(random.randint(2,4), True)
                if player.current_health > 0:
                    print(" You made it to the opposite bank with minimal burns considering you jumped a MAGMA RIVER. However the way behind you is now blocked.")
                    self.switch_sides(room)
            else:
                print(" With a running start, you successfully leap clear across the MAGMA RIVER!")
                self.switch_sides(room)
        elif action_word == "BUILD BRIDGE" and "BUILD BRIDGE" in self.action_words:
            if misc_options["MAGIC BRIDGE"] in player.inventory.misc:
                print(" You placed the MAGIC BRIDGE over the MAGMA RIVER!")
                self.action_words.remove("BUILD BRIDGE")
                self.action_words.remove("JUMP")
                player.inventory.misc.remove(misc_options["MAGIC BRIDGE"])
                self.build_bridge(room)
            elif misc_options["WOOD"] in player.inventory.misc:
                wood_count = 0
                for each_item in player.inventory.misc:
                    if each_item.name == "WOOD":
                        wood_count += 1
                if wood_count >= 3:
                    print(" You built a WOOD BRIDGE across the MAGMA RIVER!")
                    self.action_words.append("CROSS THE BRIDGE")
                    self.action_words.remove("JUMP")
                    self.action_words.remove("BUILD BRIDGE")
                    for x in range(3):
                        player.inventory.misc.remove(misc_options["WOOD"])
            else:
                print(" You don't have the materials to build a bridge.")
        elif action_word == "CROSS THE BRIDGE" and "CROSS THE BRIDGE" in self.action_words:
            print(" You crossed the WOOD BRIDGE you built. As you reach the far side the bridge catches fire and incinerates. The opposite side is blocked by the MAGMA RIVER again.")
            self.action_words.append("BUILD BRIDGE")
            self.action_words.append("JUMP")
            self.action_words.remove("CROSS THE BRIDGE")
            self.switch_sides(room)
        elif action_word == "THROW ROCKS" and "THROW ROCKS" in self.action_words:
                print(f""" You throw some rocks into the lava, they sink immediately.""")
                room.spawn_monster()

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
    
    def build_bridge(self, room):
        try: room.exits[0].number == 0
        except: room.exits[0] = self.exit_hold
        else: room.exits.append(self.exit_hold)

#---------------------------------------------------------

class Chest(Interactable):

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
            if self.challenge > 0:
                selection_loop = True
                while selection_loop == True:
                    print(" The CHEST is locked. How would you like to open it?")
                    for each_option in self.action_words:
                        print(f"""{each_option}""")
                    print("NEVERMIND")
                    selection = input("- ").upper()
                    if selection == "NEVERMIND":
                        selection_loop = False
                    for each_option in self.action_words:
                        if selection == each_option:
                            self.run_interaction(selection, player, room)
                            selection_loop = False
                    if selection_loop == True:
                        print(" That's not an option here.")
            else:
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
        elif action_word == "BREAK THE LOCK" and "BREAK THE LOCK" in self.action_words:
            chest_def = Combatant("THE LOCK", 1, 1, 0, self.challenge, Inventory())
            player.make_attack(chest_def)
            if chest_def.current_health <= 0:
                self.unlock_success(player, room)
            else:
                print(" You jammed the lock into the closed position. You can try again but it'll be even more difficult now.")
                self.challenge*=2
                self.description += " It's lock has been jammed closed."
        elif action_word == "USE A KEY" and "USE A KEY" in self.action_words:
            if misc_options["KEY"] in player.inventory.misc:
                player.inventory.misc.remove(misc_options["KEY"])
                print(" You used your key to open the lock. The key then dissintegrates, it's task in this world complete.")
                self.unlock_success(player, room)
            else:
                print(" You don't have a key to use.")

    def unlock_success(self, player, room):
        self.challenge = 0
        self.action_words.remove("BREAK THE LOCK")
        self.action_words.remove("USE A KEY")
        self.action_words.append("OPEN")
        self.run_interaction("OPEN", player, room)

#---------------------------------------------------------

class Tree(Interactable):

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
        if action_word == "CHOP" and "CHOP" in self.action_words:
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
                    if each_interactable.type == "CHOPPED TREE":
                        room.interactables.remove(each_interactable)
            elif self.challenge >= 5:
                print(" The GLOWING TREE hardened itself with magic. You can no longer CHOP or INSPECT it.")
                self.action_words.remove("CHOP")
                if "INSPECT" in self.action_words:
                    self.action_words.remove("INSPECT")
                self.action_words.append("APOLOGIZE")
        if action_word == "INSPECT" and "INSPECT" in self.action_words:
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
            else:
                print(f""" The secrets of the GLOWING TREE elude you. It will allow you to try again later.""") #add the adjustment function for this upon returning
            self.action_words.remove("INSPECT")
        if action_word == "APOLOGIZE" and "APOLOGIZE" in self.action_words:
            print(" The GLOWING TREE does not accept your apology.")

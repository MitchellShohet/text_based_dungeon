class Inventory:

    def __init__(self, weapon, armor=None, consumables=[], misc=[], dollar_bills=0):
        self.weapon = weapon
        self.armor = armor
        self.consumables = consumables
        self.misc = misc
        self.dollar_bills = dollar_bills
        self.has_equipables = False

    def add_item(self, item):
        if item.type == "WEAPON" or item.type == "ARMOR":
            self.has_equipables = True
        if item.type == "CONSUMABLE":
            self.consumables.append(item)
        else:
            self.misc.append(item)
    
    def remove_item(self, item):
        if item.type == "CONSUMABLE":
            self.consumables.remove(item)
        else:
            self.misc.remove(item)
        if item.type == "WEAPON" or item.type == "ARMOR":
            self.has_equipables = False
            for each_item in self.misc:
                if each_item.type == "WEAPON" or each_item.type == "ARMOR":
                    self.has_equipables = True
                    break


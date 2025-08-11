import random
from lists.room_list import room_list
from lists.monsters_list import Avatar
from lists.adjustments_list import enter_idol_state, turn_off_idol_state, set_exit_min, dungeon_exit_idol_test

class Navigation:
    def __init__(self):
        self.room_options = room_list #all of the room options that haven't been added to the dungeon yet
        self.rooms_visited = {"1" : [],
                            "2" : [],
                            "3" : []} #all of the rooms that have been added to the dungeon already with their floor
        self.floor = 1
        self.current_room = self.room_options[self.floor][0] #sets the starting room to "Dungeon Entrance"
        self.previous_room = self.current_room.exits[0].link #sets the starting previous room, this prevents the first test_backward() from crashing the game
        self.unlinked_exits = 2 #counts the total number of unexplored exits currently in the dungeon
        self.dungeon_length = 1
        self.exit_min = 1
        self.idol_state = False

    def enter_room(self, exit):
        self.determine_floor(exit.number)
        self.determine_next_room(exit)
        self.test_link_issues()
        self.run_adjustments()
        self.print_room_description()
        self.current_room.spawn_monster()
        self.run_idol_state()
        self.current_room.view_monster_count()
        if self.current_room.name == "HALLWAY" and len(self.current_room.interactables) > 0: print(" There might be something of interest here.")
    
    def determine_floor(self, exit_number):
        if self.current_room.name == "SECOND FLOOR TUNNEL" and exit_number == 1 or self.current_room.name == "FINAL FLOOR TUNNEL" and exit_number == 1: 
            self.floor+=1
        elif self.current_room.name == "SECOND FLOOR LANDING" and exit_number == 0 or self.current_room.name == "FINAL FLOOR LANDING" and exit_number == 0: 
            self.floor-=1
    
    def determine_next_room(self, exit):
        if exit.link == None: #determines if the exit being taken already has a room linked to it
            self.dungeon_length += 1
            self.unlinked_exits -= 1
            new_room = self.find_unexplored_room()
            exit.link = new_room
            self.rooms_visited[str(self.floor)].append(new_room)
            if new_room.name != "ROOMS MAXED" : self.room_options[self.floor].remove(new_room) #**REMOVE AFTER TESTING**
            self.previous_room = self.current_room #before leaving the current room, establishes it as the previous room
            self.current_room = exit.link #sets the current room to the new one attached to the link
            self.current_room.exits[0].link = self.previous_room
        else:
            self.previous_room = self.current_room
            self.current_room = exit.link

    def test_link_issues(self):
        try: self.current_room.exits[0].link #catches cases where a player reenters a room with an exit that's been blocked.
        except: pass
        else: 
            if self.current_room.exits[0].link == None: self.current_room.exits[0].link = self.previous_room #catches cases where an exit is prelinked to another room, links the second room to the previous one

    def find_unexplored_room(self):
        try: new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)] #checks if every possible room has already been added to the dungeon
        except: new_room = self.room_options[0][0] #***CHANGE THIS TO A FAIRY FOUNTAIN***
        new_room = self.test_floor_elegibility(new_room)
        new_exits = self.check_for_new_exits(new_room)
        attempts = 1
        while new_exits + self.unlinked_exits <= 1: #prevents the dungeon from populating every exit with a dead end
            attempts +=1
            if attempts > 80:
                new_room = self.room_options[0][0] #***ADD A LIST OF FAIRY FOUNTAINS TO CHOOSE FROM***
                break
            new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)]
            new_room = self.test_floor_elegibility(new_room)
            new_exits = self.check_for_new_exits(new_room)
        self.unlinked_exits += new_exits
        return new_room
    
    def test_floor_elegibility(self, new_room):
        testing = True
        while testing == True:
            if new_room.name == "SECOND FLOOR TUNNEL" or new_room.name == "FIRST FLOOR TUNNEL" or new_room.name == "IDOL ROOM" or new_room.name == "DUNGEON EXIT":
                try: self.rooms_visited[str(self.floor)][0].name #prevents dungeon from spawning next floor before a single room has been added to the current floor list
                except: new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)]
                if len(self.rooms_visited[str(self.floor)]) < 5: #prevents dungeon from spawning next floor before the player explores at least 5 rooms on the current one
                    new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)]
                elif new_room.name == "IDOL ROOM" and sum(1 for each_room in self.rooms_visited["3"] if each_room.name == "DUNGEON EXIT") == 1 and self.dungeon_length < self.exit_min or new_room.name == "DUNGEON EXIT" and sum(1 for each_room in self.rooms_visited["3"] if each_room.name == "IDOL ROOM") == 1 and self.dungeon_length < self.exit_min: #prevents player from discovering IDOL ROOM and DUNGEON EXIT back to back
                    new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)]
                else: testing = False
            else: testing = False
        if self.floor == 1 and len(self.rooms_visited["1"]) > 18 and self.room_options[1][len(self.room_options[1])-1].name == "SECOND FLOOR TUNNEL": #prevents dungeon from taking too long to spawn the second floor tunnel
            new_room = self.room_options[1][len(self.room_options[1])-1]
        elif self.floor == 2 and len(self.rooms_visited["2"]) > 18 and self.room_options[2][len(self.room_options[2])-1].name == "FINAL FLOOR TUNNEL": #prevents dungeon from taking too long to spawn the final floor tunnel
            new_room = self.room_options[2][len(self.room_options[2])-1]
        elif self.floor == 3 and len(self.rooms_visited["3"]) > 18 and self.room_options[3][len(self.room_options[3])-1].name == "DUNGEON EXIT" and sum(1 for each_room in self.room_options[3] if each_room.name == "IDOL ROOM") < 1: #prevents dungeon from taking too long to spawn the Dungeon Exit or the Idol Room
            new_room = self.room_options[2][len(self.room_options[2])-1]
        elif self.floor == 3 and len(self.rooms_visited["3"]) > 27 and self.room_options[3][len(self.room_options[3])-1].name == "DUNGEON EXIT": #prevents dungeon from taking too long to spawn the Dungeon Exit after spawing the Idol room
            new_room = self.room_options[2][len(self.room_options[2])-1]
        elif self.floor == 3 and len(self.rooms_visited["3"]) > 27 and sum(1 for each_room in self.room_options[3] if each_room.name == "IDOL ROOM") < 1: #prevents dungeon from taking too long to spawn Idol room after spawning the Dungeon Exit
            for each_room in self.room_options:
                if each_room.name == "IDOL ROOM": new_room = each_room
        return new_room

    def check_for_new_exits(self, room):
        new_exits = 0
        for each_exit in room.exits:
                if each_exit.number != 0: new_exits += 1
        return new_exits
    
    def run_adjustments(self):
        self.current_room.visits += 1
        for each_adjustment in self.current_room.adjustments[0]:
            if each_adjustment == enter_idol_state or each_adjustment == turn_off_idol_state or each_adjustment == set_exit_min: each_adjustment(self)
            else: each_adjustment(self.current_room, self.dungeon_length)

    def print_room_description(self):
        if isinstance(self.current_room.description, list):
            for each_descriptor in self.current_room.description:
                if each_descriptor != "": print(f""" {each_descriptor}""")
        else: print(f""" {self.current_room.description}""")
    
    def run_idol_state(self):
        if enter_idol_state in self.current_room.adjustments[0]: 
            self.current_room.adjustments[0].remove(enter_idol_state)
            print("\n Suddenly a tear in reality opens in front of you! With an eruption of static electricity, a creature emerges from it.")
        if self.idol_state == True and self.current_room.name != "GO HOME": 
            fresh_avatar = True
            for each_monster in self.current_room.monsters:
                if each_monster.type == "AVATAR OF DYNAE": 
                    self.current_room.monsters.remove(each_monster)
                    fresh_avatar = False
                    if each_monster.current_health < each_monster.max_health:
                        print(" The AVATAR OF DYNAE in this room has been fully healed!")
                elif each_monster.type == "AVATAR OF DYNAE":
                    fresh_avatar = False
            if fresh_avatar == True: print(" A new AVATAR OF DYNAE has appeared!")
            self.current_room.monsters.append(Avatar())
    
    def test_backward(self): #returns the exit that is backward from the player's perspective
        for each_exit in self.current_room.exits:
            try: each_exit.link
            except: continue
            if each_exit.link == self.previous_room: return each_exit.number
        return self.current_room.interactables[0].exit_hold.number #in cases where an exit behind the player is removed, this holds that exit information.
    
    def test_forward(self): #returns the exit that is forward from the player's perspective
        backward = self.test_backward()
        if backward % 2 == 0: return backward + 1
        else: return backward - 1
    
    def test_left(self): #returns the exit that is left from the player's perspective
        backward = self.test_backward()
        if backward == 0: return 2
        if backward == 1: return 3
        if backward == 2: return 1
        if backward == 3: return 0
        
    def test_right(self): #returns the exit that is right from the player's perspective
        backward = self.test_backward()
        if backward == 0: return 3
        if backward == 1: return 2
        if backward == 2: return 0
        if backward == 3: return 1
        


import random
from lists.room_list import room_list

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
        self.has_idol = False

    def enter_room(self, number):
        self.determine_floor(number)
        if self.current_room.exits[number].link == None: #determines if the exit being taken already has a room linked to it
            self.unlinked_exits -= 1
            new_room = self.find_unexplored_room()
            self.current_room.set_exit_link(number, new_room)
            self.rooms_visited[str(self.floor)].append(new_room)
            if new_room.name != "Placeholder Rooms Maxed" :
                self.room_options[self.floor].remove(new_room)
            self.previous_room = self.current_room
            self.current_room = self.current_room.exits[number].link
            self.current_room.exits[0].link = self.previous_room
        else:
            self.previous_room = self.current_room
            self.current_room = self.current_room.exits[number].link
        try: self.current_room.exits[0].link #catches cases where a player reenters a room with an exit that's been blocked.
        except: pass
        else:
            if self.current_room.exits[0].link == None: #catches cases where an exit is prelinked to another room, links the second room to the previous one
                self.current_room.exits[0].link = self.previous_room
        print(f""" {self.current_room.description} """)
        self.current_room.spawn_monster()
        self.current_room.view_monster_count()

    def find_unexplored_room(self):
        try : #checks if every possible room has already been added to the dungeon
            new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)]
        except : #later on this should trigger finding the next floor/ the idol/ the exit
            new_room = self.room_options[0][0]
        self.test_floor_elegibility(new_room)
        new_exits = self.check_for_new_exits(new_room)
        attempts = 1
        while new_exits + self.unlinked_exits <= 1: #prevents the dungeon from populating every exit with a dead end
            attempts +=1
            if attempts > 30:
                new_room = self.room_options[0]
                break
            new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)]
            new_room = self.test_floor_elegibility(new_room)
            new_exits = self.check_for_new_exits(new_room)
        self.unlinked_exits += new_exits
        return new_room
    
    def test_floor_elegibility(self, new_room): #alter numbers for game difficulty settings?
        while new_room.name == "Second Floor Tunnel" or new_room.name == "Final Floor Tunnel":
            try: self.rooms_visited[str(self.floor)][0].name #prevents dungeon from spawning next floor before a single room has been added to the current floor list
            except: 
                new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)]
            if len(self.rooms_visited[str(self.floor)]) < 4: #prevents dungeon from spawning next floor before the player explores at least 4 rooms on the current one
                new_room = self.room_options[self.floor][random.randrange(1, len(self.room_options[self.floor])-1)]
        if self.floor == 1 and len(self.rooms_visited["1"]) > 12 and self.room_options[1][len(self.room_options[1])-1].name == "Second Floor Tunnel": #prevents dungeon from taking too long to spawn the second floor tunnel
            new_room = self.room_options[1][len(self.room_options[1]-1)]
        elif self.floor == 2 and len(self.rooms_visited["2"]) > 12 and self.room_options[2][len(self.room_options[2])-1].name == "Final Floor Tunnel": #prevents dungeon from taking too long to spawn the final floor tunnel
            new_room = self.room_options[2][len(self.room_options[2])-1]
        return new_room
    
    def determine_floor(self, number):
        if self.current_room.name == "Second Floor Tunnel" and number == 1 or self.current_room.name == "Final Floor Tunnel" and number == 1:
            self.floor+=1
        elif self.current_room.name == "Second Floor Landing" and number == 0 or self.current_room.name == "Final Floor Landing" and number == 0:
            self.floor-=1

    def check_for_new_exits(self, room):
        new_exits = 0
        for each_exit in room.exits:
                if each_exit.number != 0:
                    new_exits += 1
        return new_exits
    
    def test_backward(self): #returns the exit that is backward from the player's perspective
        for each_exit in self.current_room.exits:
            try: each_exit.link
            except: continue
            if each_exit.link == self.previous_room:
                return each_exit.number
        return self.current_room.interactables[0].exit_hold.number #in the rare case that an exit behind the player is removed, this holds that exit information.
    
    def test_forward(self): #returns the exit that is forward from the player's perspective
        backward = self.test_backward()
        if backward % 2 == 0:
            return backward + 1
        else:
            return backward - 1
    
    def test_left(self): #returns the exit that is left from the player's perspective
        backward = self.test_backward()
        if backward == 0:
            return 2
        if backward == 1:
            return 3
        if backward == 2:
            return 1
        if backward == 3:
            return 0
        
    def test_right(self): #returns the exit that is right from the player's perspective
        backward = self.test_backward()
        if backward == 0:
            return 3
        if backward == 1:
            return 2
        if backward == 2:
            return 0
        if backward == 3:
            return 1
        


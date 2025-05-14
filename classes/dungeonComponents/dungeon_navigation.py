import random
from classes.dungeonComponents.room_list import room_list

class DungeonNavigation:
    def __init__(self):
        self.room_options = room_list #all of the room options that haven't been added to the dungeon yet
        self.rooms_visited = [] #all of the room options that have been added to the dungeon already
        self.current_room = self.room_options["general_explorable"][0] #sets the starting room to "Dungeon Entrance"
        self.previous_room = self.current_room.exits[0].link #sets the starting previous room, this prevents the first test_backward() from crashing the game
        self.unlinked_exits = 2 #counts the total number of unexplored exits generated in the dungeon

    def enter_room(self, exit_number):
        if self.current_room.exits[exit_number].link == None: #determines if the exit being taken already has a room linked to it
            self.unlinked_exits -= 1
            new_room = self.find_unexplored_room()
            self.current_room.set_exit_link(exit_number, new_room)
            self.rooms_visited.append(new_room)
            if new_room.name != "Placeholder Rooms Maxed" :
                self.room_options["general_explorable"].remove(new_room)
            self.previous_room = self.current_room
            self.current_room = self.current_room.exits[exit_number].link
            self.current_room.exits[0].link = self.previous_room
        else: 
            self.previous_room = self.current_room
            self.current_room = self.current_room.exits[exit_number].link

    def find_unexplored_room(self):
        try : #checks if every possible room has already been added to the dungeon
            new_room = self.room_options["general_explorable"][random.randrange(1, len(self.room_options["general_explorable"]))]
        except : #later on this should trigger finding the next floor/ the idol/ the exit
            new_room = self.room_options["placeholder_rooms_maxed"]
        new_exits = self.check_for_new_exits(new_room)
        attempts = 1
        while new_exits + self.unlinked_exits == 0: #prevents the dungeon from populating every exit with a dead end
            attempts +=1
            if attempts > 20:
                new_room = self.room_options["placeholder_rooms_maxed"]
                break
            new_room = self.room_options["general_explorable"][random.randrange(1, len(self.room_options["general_explorable"]))]
            new_exits = self.check_for_new_exits(new_room)
        self.unlinked_exits += new_exits
        return new_room

    def check_for_new_exits(self, room):
        new_exits = 0
        for each_exit in room.exits:
                if each_exit.exit_number != 0:
                    new_exits += 1
        return new_exits
    
    def test_backward(self): #returns the exit that is backward from the player's perspective
        for each_exit in self.current_room.exits:
            if each_exit.link == self.previous_room:
                return each_exit.exit_number
    
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


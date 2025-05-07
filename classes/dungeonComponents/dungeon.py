import random
from classes.dungeonComponents.room_list import room_list

class Dungeon:
    def __init__(self):
        self.room_options = room_list
        self.current_room = self.room_options[0]
        self.previous_room = None

    def enter_room(self, exit_number):
        if self.current_room.exits[exit_number].link == None:
            self.current_room.set_exit_link(exit_number, self.room_options[random.randrange(1, len(self.room_options)-1, 1)])
            self.previous_room = self.current_room
            self.current_room = self.current_room.exits[exit_number] 
            self.current_room.exits[0] = self.previous_room
        else: 
            self.previous_room = self.current_room
            self.current_room = self.current_room.exits[exit_number]

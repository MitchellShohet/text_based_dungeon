import random
from classes.dungeonComponents.room_list import room_list
from line_spacer import line_spacer

class Dungeon:
    def __init__(self):
        self.room_options = room_list
        self.rooms_visited = []
        self.current_room = self.room_options[0]
        self.previous_room = None

    def enter_room(self, exit_number):
        if self.current_room.exits[exit_number].link == None:
            random_room = self.room_options[random.randrange(1, len(self.room_options))]
            self.current_room.set_exit_link(exit_number, random_room)
            self.rooms_visited.append(random_room)
            self.room_options.remove(random_room)
            self.previous_room = self.current_room
            self.current_room = self.current_room.exits[exit_number].link
            self.current_room.exits[0].link = self.previous_room
        else: 
            self.previous_room = self.current_room
            self.current_room = self.current_room.exits[exit_number].link
        print("unexplored rooms")
        for each_room in self.room_options:
            print(each_room.name)
        print(line_spacer)
        print(line_spacer)
        print("explored rooms")
        for each_room in self.rooms_visited:
            print(each_room.name)



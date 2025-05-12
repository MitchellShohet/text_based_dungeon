from classes.dungeonComponents.exit import Exit

class Room:
    def __init__(self, name, description, exits):
        self.name = name
        self.description = description
        self.exits = exits

    def set_exit_link(self, exit_number, room):
        self.exits[exit_number].set_link(room)
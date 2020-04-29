# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
import random


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __repr__(self):
        # if self.e_to is not None:
        #     return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)

    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

        self.previous_room = None
        self.current_room = None

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = self.width//2  # (this will become 0 on the first step)
        y = self.height//2
        room_count = 0
        empty_space = True

        # Start generating rooms to the east
        # 1: east, 2: west, 3: north, 4: south
        direction = random.randint(1, 4)

        # While there are rooms to be created...

        while room_count < num_rooms:

            while empty_space:
                print(tuple((x, y)))
                # Calculate the direction of the room to be created
                if direction == 1 and x < size_x - 1 and self.grid[y][x+1] is None:
                    room_direction = "e"
                    x += 1
                    direction = random.randint(2, 4)
                elif direction == 2 and x > 0 and self.grid[y][x-1] is None:
                    room_direction = "w"
                    x -= 1
                    direction = random.randint(1, 4)
                elif direction == 3 and y < size_y - 1 and self.grid[y+1][x] is None:
                    room_direction = "n"
                    y += 1
                    direction = random.randint(1, 4)
                elif direction == 4 and y > 0 and self.grid[y-1][x] is None:
                    room_direction = "s"
                    y -= 1
                    direction = random.randint(1, 3)
                else:
                    if (x < 0) or (x > size_x - 1):
                        direction = random.randint(3, 4)
                    elif (y < 0) or (y > size_y - 1):
                        direction = random.randint(1, 2)
                    else:
                        self.move(direction, x, y)
                        print("this is a block")
                        empty_space = False
                        continue

                # Create a room in the given direction
                room = Room(room_count, "A Generic Room",
                            "This is a generic room.", x, y)
                # Note that in Django, you'll need to save the room after you create it

                # Save the room in the World grid
                self.grid[y][x] = room
                print(f"this is the room {room}")

                # Connect the new room to the previous room
                if self.previous_room is not None:
                    self.previous_room.connect_rooms(room, room_direction)

                # if self.grid[y][x] is not None:
                #     make connection
                #     if self.previous_room == direction we are going
                #         dont make connection
                #     else:
                #         return

                # Update iteration variables
                self.previous_room = self.current_room
                self.current_room = room
                room_count += 1

            while not empty_space:
                dirs = {1: 'e', 2: 'w', 3: 'n', 4: 's'}
                der = dirs[direction]
                print(f"previous room: {self.previous_room}")
                print(f"current room: {self.grid[x][y]}{x}{y}")
                print(self.grid)
                print(getattr(self.previous_room, f"{der}_to"))
                if getattr(self.previous_room, f"{der}_to") == self.move(direction, x, y):
                    print("look at me now, ma")
                    return
                return
                # if room in direction we are going has connection in that direction...
                # move to room
                # reroll route
                # if empty
                # empty_space = True
                # else if room in direction we are going does not have connection in that direction...
                # move to room
                # connect rooms
                # reroll route
                # if empty
                # empty_space = True

    def move(self, direction, x, y):
        print("we moved")
        if direction == 1:
            x += 1
            self.previous_room = self.current_room
            self.current_room = self.grid[x][y]
            return self.current_room
            print(f"moved to {x}, {y}")
        elif direction == 2:
            x -= 1
            self.previous_room = self.current_room
            self.current_room = self.grid[x][y]
            return self.current_room
            print(f"moved to {x}, {y}")
        elif direction == 3:
            y += 1
            self.previous_room = self.current_room
            self.current_room = self.grid[x][y]
            return self.current_room
            print(f"moved to {x}, {y}")
        elif direction == 4:
            y -= 1
            self.previous_room = self.current_room
            self.current_room = self.grid[x][y]
            return self.current_room
            print(f"moved to {x}, {y}")

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 5
width = 5
height = 5
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")

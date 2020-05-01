# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world
import random
from adventure.models import Room


# class Room:
#     def __init__(self, id, name, description, x, y):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.n_to = None
#         self.s_to = None
#         self.e_to = None
#         self.w_to = None
#         self.x = x
#         self.y = y

#     def __repr__(self):
#         # if self.e_to is not None:
#         #     return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
#         return f"({self.x}, {self.y})"

#     def connect_rooms(self, connecting_room, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
#         reverse_dir = reverse_dirs[direction]
#         setattr(self, f"{direction}_to", connecting_room)
#         setattr(connecting_room, f"{reverse_dir}_to", self)

#     def get_room_in_direction(self, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

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
        previous_room = None
        current_room = None

        def move(direction):
            nonlocal x
            nonlocal y
            if direction == 1 and x < size_x - 1 and self.grid[y][x+1] is not None:
                x += 1
                # print(f"moved to {x}, {y}")
            elif direction == 2 and self.grid[y][x-1] is not None:
                x -= 1
            elif direction == 3 and y < size_y - 1 and self.grid[y+1][x] is not None:
                y += 1
            elif direction == 4 and y > 0 and self.grid[y-1][x] is not None:
                y -= 1
            return self.grid[y][x]

        # Start generating rooms to the east
        # 1: east, 2: west, 3: north, 4: south
        # direction = random.randint(1, 4)

        # While there are rooms to be created...
        while room_count < num_rooms:

            while empty_space:
                direction = random.randint(1, 4)
                # print(direction)
                # print(tuple((x, y)))
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
                        move(direction)
                        empty_space = False
                        break

                # Create a room in the given direction
                room = Room(room_count, "A Generic Room",
                            "This is a generic room.", x, y)
                room.save_coords(y, x)
                # Note that in Django, you'll need to save the room after you create it
                # Save the room in the World grid
                self.grid[y][x] = room
                # Connect the new room to the previous room
                if previous_room is not None:
                    previous_room.connect_rooms(room, room_direction)

                # Update iteration variables
                previous_room = room
                room_count += 1

            while not empty_space:
                dirs = {1: 'e', 2: 'w', 3: 'n', 4: 's'}
                rdirs = {2: 'e', 1: 'w', 4: 'n', 3: 's'}
                der = dirs[direction]
                rders = rdirs[direction]

                if getattr(previous_room, f"{der}_to") is None:
                    # current_room.connect_rooms(room, rders)
                    previous_room.connect_rooms(room, rders)
                    empty_space = True
                    continue
                elif getattr(previous_room, f"{der}_to") is not None:
                    empty_space = True
                    continue
                self.grid[y][x] = room
                previous_room = room
                

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
num_rooms = 100
width = 20
height = 20
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")

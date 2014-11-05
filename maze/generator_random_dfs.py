import random
import operator

class MazeGenerator:
    def __init__(self, maze, start_pos):
        self.maze = maze
        self.cur_pos = start_pos
        self.prev_travelled = [start_pos]
        self.visit = [start_pos]

    def is_valid(self, pos):
        horizontal_validity = 0 <= pos[0] < len(self.maze[0])
        vertical_validity = 0 <= pos[1] < len(self.maze)
        not_previously_travelled = (not pos in self.prev_travelled)
        return horizontal_validity and vertical_validity and not_previously_travelled

    def valid_neighbors(self, pos):
        left = (pos[0] - 2, pos[1])
        right = (pos[0] + 2, pos[1])
        up = (pos[0], pos[1] - 2)
        down = (pos[0], pos[1] + 2)

        neighbors = [left, right, up, down]
        return filter(lambda x: self.is_valid(x), neighbors)

    def update(self):
        neighbors = self.valid_neighbors(self.cur_pos)

        # if there are valid neighbors, move to one at random
        if len(neighbors) > 0:
            next_step = random.choice(neighbors)
            self.prev_travelled.append(next_step)
            self.visit.append(next_step)

            # find the intermediate position
            diff = tuple(map(operator.sub, next_step, self.cur_pos))
            diff = (diff[0] / 2, diff[1] / 2)
            intermediate = tuple(map(operator.add, diff, self.cur_pos))

            # change the corresponding intermediate position in maze
            self.maze[intermediate[0]][intermediate[1]] = False 

            self.cur_pos = next_step
        else:
            self.cur_pos = self.visit.pop()

# Generate a blank maze
def generate_blank_maze(width, height):
    maze = [[True for x in range(width)] for y in range(height)]
    return maze

# make sure the dimensions are odd numbers
# note this includes the border
def generate_checkered_maze(maze):
    for i in range(0, len(maze)):
        # for the odd rows
        if (i % 2) == 0:
            for j in range(0, len(maze[i])):
                # for the odd elements in the odd rows
                if (j % 2) == 0:
                    maze[i][j] = False 
    return maze


# Generates the entire maze
def generate_maze(width, height):
    maze = generate_checkered_maze(generate_blank_maze(width, height))
    gen = MazeGenerator(maze, (0, 0))
    while len(gen.visit) > 0 or len(gen.valid_neighbors(gen.cur_pos)) > 0:
        gen.update()
    return gen.maze





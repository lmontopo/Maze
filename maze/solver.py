from collections import namedtuple

# Fork is a namedtuple
Fork = namedtuple('Fork', ['pos', 'direction'])

# A class of maze solvers
class Solver:
    def __init__(self, maze, start_pos, end_pos):
        self.maze = maze
        self.cur_pos = start_pos
        self.end_pos = end_pos
        self.prev_travelled = set()
        self.solved = False
        self.forks = [] # stores the fork data: location of fork & possible directions

    def check_surroundings(self, maze):
        # returns true or false
        def is_valid(pos):
            horizontal_validity = 0 <= pos[0] < len(maze[0])
            vertical_validity = 0 <= pos[1] < len(maze)
            
            # if we're out of range, return false immediately so that we don't 
            # look up an index out of range in maze
            if (not horizontal_validity) or (not vertical_validity):
                return False
            else:
                not_maze_wall = not maze[pos[1]][pos[0]]
                not_previously_travelled = (not pos in self.prev_travelled)
                return not_maze_wall and not_previously_travelled

        # up, down, left, right = [self.cur_pos[0] + dx, self.cur_pos[1] + dy] for dx, dy in [[-1, 0], [1, 0], ]
        up = (self.cur_pos[0], self.cur_pos[1] - 1)
        down = (self.cur_pos[0], self.cur_pos[1] + 1)
        right = (self.cur_pos[0] + 1, self.cur_pos[1])
        left = (self.cur_pos[0] - 1, self.cur_pos[1])

        # stores the surrounding positions
        surroundings = [down, up, right, left]
        valid_directions = map(is_valid, surroundings)

        # for counting how many valid directions there are
        valid_directions_true_list = filter(lambda x: x, valid_directions)      

        # if valid directions has more than one true, we are at a fork
        cur_pos_copy = self.cur_pos[:]
        if len(valid_directions_true_list) > 1:
            self.forks.append(Fork(cur_pos_copy, valid_directions))

        for spot in [down, up, right, left]:
            if is_valid(spot):
                return spot

        return self.forks.pop().pos

    def update(self, maze):
        # if we haven't solved the maze yet, check our surroundings and make a move
        if not self.solved:
            # Get the direction to move to
            direction = self.check_surroundings(maze)
            cur_pos_copy = tuple(self.cur_pos[:])

            # If we've found a move, add the current position to prev_travelled
            if direction:
                self.prev_travelled.update([cur_pos_copy])

            #move in the desired direction
            self.cur_pos = direction

            # If we've moved onto the maze end, we're done
            if self.cur_pos == self.end_pos:
                self.solved = True


import random
import operator

class MazeGenerator:
    def __init__(self, maze, start_pos):
        self.maze = maze
        self.cur_pos = start_pos
        self.history = [start_pos]
        self.revisit = [start_pos]
        self.complete = False
        self.neighbors = []

    def is_valid(self, pos):
        horizontal_validity = 0 <= pos[0] < len(self.maze[0])
        vertical_validity = 0 <= pos[1] < len(self.maze)
        not_previously_travelled = (not pos in self.history)
        return horizontal_validity and vertical_validity and not_previously_travelled

    def valid_neighbors(self, pos):
        left = (pos[0], pos[1] - 2)
        right = (pos[0], pos[1] + 2)
        up = (pos[0] - 2, pos[1])
        down = (pos[0] + 2, pos[1])

        neighbors = [left, right, up, down]
        return filter(lambda x: self.is_valid(x), neighbors)

    def update(self):
        neighbors = self.valid_neighbors(self.cur_pos)
        self.neighbors = neighbors

        # highlight some stuff
        for pos in self.neighbors:
            draw_square(pos[1], pos[0], BLOCK_SIZE, BLOCK_SIZE, PINK)
        for pos in self.revisit:
            draw_square(pos[1], pos[0], BLOCK_SIZE, BLOCK_SIZE, GREEN)
        draw_square(self.cur_pos[1], self.cur_pos[0], BLOCK_SIZE, BLOCK_SIZE, BLUE)

        # if there are valid neighbors, move to one at random
        if len(neighbors) > 0:
            next_step = random.choice(neighbors)

            self.history.append(next_step)
            self.revisit.append(next_step)

            # find the intermediate position
            diff = tuple(map(operator.sub, next_step, self.cur_pos))
            diff = (diff[0] / 2, diff[1] / 2)
            intermediate = tuple(map(operator.add, diff, self.cur_pos))

            # change the corresponding intermediate position in maze
            self.maze[intermediate[0]][intermediate[1]] = False 

            self.cur_pos = next_step
        else:
            self.cur_pos = self.revisit.pop()

        # if there are no places left to visit and not valid nighbors, we're done
        if len(self.revisit) == 0 and len(self.valid_neighbors(gen.cur_pos)) == 0:
            self.complete = True

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
    while len(gen.revisit) > 0 or len(gen.valid_neighbors(gen.cur_pos)) > 0:
        gen.update()
    return gen.maze

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

import pygame
import pygame.font

WIDTH = 560
HEIGHT = 560
BLOCK_SIZE = 80
done = False

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 20, 147)
BLUE = (0, 0, 255)

# Draws a single square
def draw_square(x, y, width, height, color):
    pygame.draw.rect(screen, color, [x * width, y * height, width, height], 0)

# Takes a list of indices to draw squares, then draws them
def draw_maze(maze):
    for y, row in enumerate(maze):
        for x, element in enumerate(row):
            if element:
                draw_square(x, y, BLOCK_SIZE, BLOCK_SIZE, BLACK)

#makeText is a function that returns a tuple (textSurface, textRect)
pygame.font.init()
def makeText(text, fontName, fontSize, color, center):
    font = pygame.font.Font(fontName, fontSize)
    textSurf = font.render(text, False, color)
    textRect = textSurf.get_rect()
    textRect.center = center
    return (textSurf, textRect)

# Solved text
solvedSurf, solvedRect = makeText('SOLVED', 'Minecraftia.ttf', 48, RED, (WIDTH / 2, HEIGHT / 2))

def game(maze):
    def render():

        # -- update the screen with whatever we've drawn.
        pygame.display.flip()
        # --- frames per second
        clock.tick(5)

    render()

if __name__ == '__main__':
    # Initiate screen and clock
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    maze = generate_checkered_maze(generate_blank_maze(WIDTH / BLOCK_SIZE, HEIGHT / BLOCK_SIZE))
    gen = MazeGenerator(maze, (0, 0))

    screen.fill(WHITE)
    draw_maze(maze)

    #--- Main event loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # fill the background white
                    screen.fill(WHITE)
                    # draw the maze
                    draw_maze(maze)

                    if not gen.complete:
                        gen.update()
                    else:
                        print "done!"

            if event.type == pygame.QUIT:
                done = True

        # Run the maze game
        game(maze)


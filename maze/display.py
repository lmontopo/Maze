#from deterministic_maze import generate_maze
from generator_random_dfs import generate_maze
from solver_bfs import Solver
import pygame
import pygame.font

WIDTH = 420
HEIGHT = 420
BLOCK_SIZE = 20
done = False

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Draws a single square
def draw_square(x, y, width, height):
    pygame.draw.rect(screen, BLACK, [x * width, y * height, width, height], 0)

# Takes a list of indices to draw squares, then draws them
def draw_maze(maze):
    for y, row in enumerate(maze):
        for x, element in enumerate(row):
            if element:
                draw_square(x, y, BLOCK_SIZE, BLOCK_SIZE)

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

def game(solver):
    def render():
        # fill the background white
        screen.fill(WHITE)
        # draw the maze
        draw_maze(solver.maze)
        # draw the solver
        pygame.draw.rect(screen, GREEN, [solver.cur_pos[0] * BLOCK_SIZE, solver.cur_pos[1] * BLOCK_SIZE, 
                            BLOCK_SIZE, BLOCK_SIZE], 0)

        # if we haven't solved the maze, keep updating
        if not solver.solved:
            solver.update(entire_maze)
        else:
            screen.blit(solvedSurf, solvedRect)
            

        # -- update the screen with whatever we've drawn.
        pygame.display.flip()
        
        # --- frames per second
        clock.tick(10)

    render()

if __name__ == '__main__':
    # Initiate screen and clock
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Construct the entire maze
    # entire_maze = generate_maze(WIDTH, HEIGHT, BLOCK_SIZE)
  

    # Construct random maze
    entire_maze = generate_maze(WIDTH / BLOCK_SIZE, HEIGHT / BLOCK_SIZE)

    # Create maze solver object
    solver = Solver(entire_maze, (0, 0), ((WIDTH / BLOCK_SIZE) - 1, (HEIGHT / BLOCK_SIZE) - 1)) 

    #--- Main event loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Run the maze game
        game(solver)



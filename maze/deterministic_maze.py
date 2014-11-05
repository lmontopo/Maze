import random

# Generates the entire maze
def generate_maze(width, height, block_size):
    maze = generate_blank_maze(width / block_size, height / block_size)
    add_border(maze)
    add_block(maze, 6, (height / block_size) - 4, 2, 2)
    add_block(maze, 6, (height / block_size) - 4, 4, 6)
    add_block(maze, 6, (height / block_size) - 4, 8, 2)
    return maze

def generate_random_maze(width, height):
    maze = [[random.choice([True, False]) for x in range(width)] for y in range(height)]
    return maze

# Generate a blank maze
def generate_blank_maze(width, height):
    maze = [[False for x in range(width)] for y in range(height)]
    return maze

# Adds a border surrounding the maze
def add_border(maze):
    # North wall
    for i in range(len(maze[0])):
        maze[0][i] = True

    # South wall
    for i in range(len(maze[-1])):
        maze[-1][i] = True

    # East and West wall
    for i in range(1, len(maze) - 1):
        maze[i][0] = True
        maze[i][-1] = True

    # Make entrance and exit
    maze[0][0] = False
    maze[0][1] = False
    maze[-1][-1] = False
    maze[-1][-2] = False

    return maze

# Adds a block with top left corner (start_x, start_y) with width and height to the maze   
def add_block(maze, width, height, start_x, start_y):
    max_height = len(maze)
    max_width = len(maze[0]) 

    y = start_y
    while y < start_y + height:
        x = start_x
        while x < start_x + width:
            # only change the maze block if the index is in range
            if 0 <= x < max_width and 0 <= y < max_height:
                maze[y][x] = True
            x += 1
        y += 1

    return maze



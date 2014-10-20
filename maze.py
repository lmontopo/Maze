import pygame

# Define some colours:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Define some variables
clock = pygame.time.Clock()
done = False

WIDTH = 500
HEIGHT = 700
block_size = 20

# Initiate screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# An array containing all the black square indices
entire_maze = []

def generate_border(width, height):
	list = []
	y = 0
	x = 0
	while y < height:
		list.append((0, y + block_size)) #west
		list.append((width - block_size,y)) #east
		y += block_size
	list.pop() #to make an exit
	
	while x < width:
		list.append((x + 2 * block_size, 0)) #North
		list.append((x, height - block_size)) #south
		x += 20
	list.pop() #to make an exit
	list.remove((width - block_size, height - 2*block_size)) #to make an exit
	return list
	
#generates a single wall within the maze	
def generate_wall(width, height, x, y):
	list = []
	while y < height:
		list.append((x,y))
		y += block_size
	return list

def draw_square(x,y):
	pygame.draw.rect(screen, BLACK, [x, y, block_size, block_size], 0)

#takes a list of indices to draw squares, then draws them
def draw_maze(list):
	for element in list:
		draw_square(element[0],element[1])

#makes the list of indices to feed to draw_maze		
def generate_maze(width, height):
	list = []
	x = 20
	while x < (width - 20):
		list.extend(generate_wall(WIDTH, HEIGHT - block_size, x, 40))
		list.extend(generate_wall(WIDTH, HEIGHT - 2 * block_size, x + 40, 20))
		x +=80
	return list

# A class of maze solvers
class Solver:
	def __init__(self, start_pos, end_pos, color):
		self.cur_pos = start_pos
		self.end_pos = end_pos
		self.color = color

	def display(self):
		pygame.draw.rect(screen, self.color, [self.cur_pos[0], self.cur_pos[1], 20, 20], 0)

	def check_surroundings(self, maze):
		# check if we can move down
		down = [self.cur_pos[0], self.cur_pos[1] + block_size]
		if (not (down[0], down[1]) in maze) and down[1] < HEIGHT:
			return "DOWN"

		# check if we can move up
		up = [self.cur_pos[0], self.cur_pos[1] - block_size]
		if (not (up[0], up[1]) in maze) and up[1] > 0:
			return "UP"

		# check if we can move right
		right = [self.cur_pos[0] + block_size, self.cur_pos[1]]
		if (not (right[0], right[1]) in maze) and right[0] < WIDTH:
			return "RIGHT"

		# check if we can move right
		left = [self.cur_pos[0] - block_size, self.cur_pos[1]]
		if (not (left[0], left[1]) in maze) and left[0] > 0:
			return "LEFT"


	# direction is a string UP DOWN LEFT RIGHT
	def update(self, maze):
		# Get the direction to move to
		direction = self.check_surroundings(maze)

		# Move
		if direction == "RIGHT":
			self.cur_pos[0] += block_size
		elif direction == "LEFT":
			self.cur_pos[0] -= block_size
		elif direction == "UP":
			self.cur_pos[1] -= block_size
		elif direction == "DOWN":
			self.cur_pos[1] += block_size

#--------------- Construct the entire maze
entire_maze.extend(generate_border(WIDTH, HEIGHT))
entire_maze.extend(generate_maze(WIDTH, HEIGHT))

# Create maze solver object
solver = Solver([0, 0], (WIDTH, HEIGHT), GREEN)

# --------------------------------- Main Program Loop ---------------------------- #
while not done:
	#--- Main event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	
	# -- Game logic should go here
	
	# -- First, clear the screen to white.
	screen.fill(WHITE)
	# -- Drawing should go here
	draw_maze(entire_maze)
	solver.display()
	solver.update(entire_maze)
	
	# -- update the screen with whatever we've drawn.
	pygame.display.flip()
	
	# --- Limit to 60 frames per second
	clock.tick(60)
	
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


# Draws a single square
def draw_square(x,y):
	pygame.draw.rect(screen, BLACK, [x, y, block_size, block_size], 0)

# Takes a list of indices to draw squares, then draws them
def draw_maze(list):
	for element in list:
		draw_square(element[0],element[1])

# Generates the interior of the maze
def generate_maze(width, height):

	# Generates the border surrounding the maze
	def generate_border(width, height):
		list = []
		y = 0
		x = block_size
		while y < height:
			list.append([0, y]) # West wall
			list.append([width - block_size,y]) # East wall
			y += block_size
		
		while x < width - block_size:
			list.append([x, 0]) # North wall
			list.append([x, height - block_size]) # South wall
			x += block_size
		
		#Remouving blocks for entrance and exit:
		list.remove([0,0]) # to make an entrance
		list.remove([block_size,0]) #to make an entrance
		list.remove([width - block_size, height - block_size]) #to make an exit
		list.remove([width - block_size, height - 2*block_size]) # to make an exit
		return list

	# Generates a single wall within the maze	
	def generate_wall(width, height, x, y):
		list = []
		while y < height:
			list.append([x,y])
			y += block_size
		return list

	list = []
	x = 40
	while x < (width - 40):
		list.extend(generate_wall(width, height - block_size, x, 40))
		x += 20
	list.extend(generate_border(width,height))
	return list

# A class of maze solvers
class Solver:
	def __init__(self, start_pos, end_pos, color):
		self.cur_pos = start_pos
		self.end_pos = end_pos
		self.color = color
		self.prev_travelled = []
		self.solved = False
		self.forks = []	# stores the fork data: location of fork & possible directions

	def display(self):
		pygame.draw.rect(screen, self.color, [self.cur_pos[0], self.cur_pos[1], 
							block_size, block_size], 0)

	def check_surroundings(self, maze):
		# returns true or false
		def is_valid(pos):
			horizontal_validity = (0 <= pos[0]) and (pos[0] < WIDTH)
			vertical_validity = (0 <= pos[1]) and (pos[1] < HEIGHT)
			not_maze_wall = (not pos in maze) 
			not_previously_travelled = (not pos in self.prev_travelled)
			return horizontal_validity and vertical_validity and not_maze_wall and not_previously_travelled

		up = [self.cur_pos[0], self.cur_pos[1] - block_size]
		down = [self.cur_pos[0], self.cur_pos[1] + block_size]
		right = [self.cur_pos[0] + block_size, self.cur_pos[1]]
		left = [self.cur_pos[0] - block_size, self.cur_pos[1]]

		# stores the surrounding positions
		surroundings = [down, up, right, left]
		valid_directions = map(is_valid, surroundings)

		# for counting how many valid directions there are
		valid_directions_true_list = filter(lambda x: x, valid_directions)		

		# if valid directions has more than one true, we are at a fork
		cur_pos_copy = self.cur_pos[:]
		if len(valid_directions_true_list) > 1:
			self.forks.append([cur_pos_copy, valid_directions])

		# check if we can move down
		if is_valid(down):
			return down

		# check if we can move up
		if is_valid(up):
			return up

		# check if we can move right
		if is_valid(right):
			return right

		# check if we can move left
		if is_valid(left):
			return left

		print self.forks
		return self.forks.pop()[0]

		# if no direction is found return null
		return None

	def update(self, maze):
		# if we haven't solved the maze yet, check our surroundings and make a move
		if not self.solved:
			# Get the direction to move to
			direction = self.check_surroundings(maze)
			cur_pos_copy = self.cur_pos[:]

			# If we've found a move, add the current position to prev_travelled
			if direction:
				self.prev_travelled.append(cur_pos_copy)

			#move in the desired direction
			self.cur_pos = direction

			# If we've moved onto the maze end, we're done
			if self.cur_pos == self.end_pos:
				self.solved = True

#--------------- Construct the entire maze
entire_maze = generate_maze(WIDTH, HEIGHT)

# Create maze solver object
solver = Solver([0, 0], [WIDTH - block_size, HEIGHT - block_size], GREEN)

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
	if not solver.solved:
		solver.update(entire_maze)
	
	# -- update the screen with whatever we've drawn.
	pygame.display.flip()
	
	# --- Limit to 60 frames per second
	clock.tick(10)
	
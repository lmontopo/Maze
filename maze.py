import pygame

#Define some colours:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()

done = False


def generate_border(width, height):
	list = []
	y = 0
	x = 0
	while y < height:
		list.append((0,y+20)) #west
		list.append((width-20,y)) #east
		y +=20
	list.pop() #to make an exit
	
	while x < width:
		list.append((x+40,0)) #North
		list.append((x,height-20)) #south
		x += 20
	list.pop() #to make an exit
	list.remove((width-20, height - 40)) #to make an exit
	return list
	
#generates a single wall within the maze	
def generate_wall(width, height, x, y):
	list = []
	while y < height:
		list.append((x,y))
		y += 20
	return list
		
	

def draw_square(x,y):
	pygame.draw.rect(screen, BLACK, [x,y,20,20],0)

#takes a list of indices to draw squares, then draws them
def draw_maze(list):
	for element in list:
		draw_square(element[0],element[1])

#makes the list of indices to feed to draw_maze		
def generate_maze(width, height):
	list = []
	x = 20
	while x < (width - 20):
		list.extend(generate_wall(500, 680, x, 40))
		list.extend(generate_wall(500, 660, x + 40, 20))
		x +=80
	return list

#initiate screen
screen = pygame.display.set_mode((500,700))

# --- Main Program Loop
while not done:
	#--- Main event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	
	# -- Game logic should go here
	
	
	# -- First, clear the screen to white.
	screen.fill(WHITE)
	# -- Drawing should go here
	draw_maze(generate_border(500,700)) #draw outer border
	draw_maze(generate_maze(500,700)) #draw maze
	
	# -- update the screen with whatever we've drawn.
	pygame.display.flip()
	
	# --- Limit to 60 frames per second
	clock.tick(60)
	
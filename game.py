import pygame, sys, random
from pygame.locals import *
from level import *

CHAR_SPEED	= 10
CHAR_SIZE	= 50
CELL_SIZE	= 64
WINDOW_SIZE	= 640

class Char_S(pygame.sprite.Sprite):
	def __init__(self, level):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([CHAR_SIZE , CHAR_SIZE])
		self.image.fill((0,0,255))
		self.rect = self.image.get_rect()
		self.level_complete = False

		# set char x start pos
		if level.start_pos[0] == 0:
			self.rect.left = CELL_SIZE + (CELL_SIZE//2 - CHAR_SIZE//2)
		elif level.start_pos[0] == level.width + 1:
			self.rect.right = (level.width + 1) * CELL_SIZE - \
			(CELL_SIZE//2 - CHAR_SIZE//2)
			# adjust camera
			while self.rect.right > WINDOW_SIZE - (CELL_SIZE):
				self.rect.move_ip(-1, 0)
				for sprite in levelMap:
					sprite.rect.move_ip(-1, 0)
		else:
			self.rect.left = CELL_SIZE*level.start_pos[0] + \
			(CELL_SIZE//2 - CHAR_SIZE//2)
			# adjust camera
			while self.rect.right > WINDOW_SIZE//2 + CHAR_SIZE//2:
				self.rect.move_ip(-1, 0)
				for sprite in levelMap:
					sprite.rect.move_ip(-1, 0)
			# make sure no area outside the level is in view
			for s in levelMap:
				if isinstance(s, Wall_S) and s.keyCell:
					while s.rect.right < WINDOW_SIZE:
						self.rect.move_ip(1, 0)
						for sprite in levelMap:
							sprite.rect.move_ip(1, 0)

		# set char y start pos
		if level.start_pos[1] == 0:
			self.rect.top = CELL_SIZE + (CELL_SIZE//2 - CHAR_SIZE//2)
		elif level.start_pos[1] == level.height + 1:
			self.rect.bottom = (level.height + 1) * CELL_SIZE - \
			(CELL_SIZE//2 - CHAR_SIZE//2)
			# adjust camera
			while self.rect.bottom > WINDOW_SIZE - (CELL_SIZE):
				self.rect.move_ip(0, -1)
				for sprite in levelMap:
					sprite.rect.move_ip(0, -1)
		else:
			self.rect.top = CELL_SIZE*level.start_pos[1] + \
			(CELL_SIZE//2 - CHAR_SIZE//2)
			# adjust camera
			while self.rect.bottom > WINDOW_SIZE//2 + CHAR_SIZE//2:
				self.rect.move_ip(0, -1)
				for sprite in levelMap:
					sprite.rect.move_ip(0, -1)
			# make sure no area outside the level is in view
			for s in levelMap:
				if isinstance(s, Wall_S) and s.keyCell:
					while s.rect.bottom < WINDOW_SIZE:
						self.rect.move_ip(0, 1)
						for sprite in levelMap:
							sprite.rect.move_ip(0, 1)

	def up(self):
		if self.rect.top - CHAR_SPEED - CELL_SIZE//2 > 0:
			self.rect.move_ip(0, - CHAR_SPEED)
		else:
			for sprite in levelMap:
				sprite.rect.move_ip(0, CHAR_SPEED) 

		while pygame.sprite.spritecollide(self, collisionMap, False) != []:
			self.rect.move_ip(0, 1)

		if finish.sprites()[0].rect.contains(self.rect):
			self.level_complete = True

	def down(self):
		if self.rect.bottom + CHAR_SPEED + CELL_SIZE//2 < WINDOW_SIZE:
			self.rect.move_ip(0, CHAR_SPEED)
		else:
			for sprite in levelMap:
				sprite.rect.move_ip(0, -CHAR_SPEED)

		while pygame.sprite.spritecollide(self, collisionMap, False) != []:
			self.rect.move_ip(0, -1)

		if finish.sprites()[0].rect.contains(self.rect):
			self.level_complete = True

	def left(self):
		if self.rect.left - CHAR_SPEED - CELL_SIZE//2 > 0:
			self.rect.move_ip(- CHAR_SPEED, 0)
		else:
			for sprite in levelMap:
				sprite.rect.move_ip(CHAR_SPEED, 0)

		while pygame.sprite.spritecollide(self, collisionMap, False) != []:
			self.rect.move_ip(1, 0)

		if finish.sprites()[0].rect.contains(self.rect):
			self.level_complete = True

	def right(self):
		if self.rect.right + CHAR_SPEED + CELL_SIZE//2 < WINDOW_SIZE:
			self.rect.move_ip(CHAR_SPEED, 0)
		else:
			for sprite in levelMap:
				sprite.rect.move_ip(- CHAR_SPEED, 0)

		while pygame.sprite.spritecollide(self, collisionMap, False) != []:
			self.rect.move_ip(-1, 0)

		if finish.sprites()[0].rect.contains(self.rect):
			self.level_complete = True

class Wall_S(pygame.sprite.Sprite):
	def __init__(self, x, y, keyCell):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
		self.image.fill((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = x*CELL_SIZE, y*CELL_SIZE

		self.keyCell = keyCell

class Start_S(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
		self.image.fill((0,255,0))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = x*CELL_SIZE, y*CELL_SIZE

class Finish_S(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
		self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = x*CELL_SIZE, y*CELL_SIZE

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("PCG Maze!")
level_width = 10
level_height = 10
start_wall = None

while True: # game loop
	level_complete = False
	level = Level(level_width, level_height, start_wall)
	levelMap = pygame.sprite.Group()
	collisionMap = pygame.sprite.Group()
	finish = pygame.sprite.Group()
	for cell in level.map:
		if isinstance(level.map[cell], Wall):
			if  level.map[cell].x == level.width  + 1 and \
				level.map[cell].y == level.height + 1:
				keyCell = True
			else:
				keyCell = False
			newSprite = Wall_S( cell[0], cell[1], keyCell )
			levelMap.add(newSprite)
			collisionMap.add(newSprite)
		elif isinstance(level.map[cell], Start):
			newSprite = Start_S( cell[0], cell[1] )
			levelMap.add(newSprite)
			collisionMap.add(newSprite)
		elif isinstance(level.map[cell], Finish):
			newSprite = Finish_S( cell[0], cell[1] )
			levelMap.add(newSprite)
			finish.add(newSprite)
	char = Char_S(level)

	while not level_complete: # level loop
		for event in pygame.event.get():
			# Check if game has been quit and quit
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pressedKeys = pygame.key.get_pressed()
		if pressedKeys[K_UP]:
			char.up()
			level_complete = char.level_complete
		if pressedKeys[K_DOWN]:
			char.down()
			level_complete = char.level_complete
		if pressedKeys[K_LEFT]:
			char.left()
			level_complete = char.level_complete
		if pressedKeys[K_RIGHT]:
			char.right()
			level_complete = char.level_complete

		screen.fill(( 255, 128,   0 ))

		levelMap.draw(screen)
		pygame.draw.rect(screen, (0,0,255), char)

		pygame.display.update()
		fpsClock.tick(30)

	level_width  += random.choice([1, 2, 3, 3, 4, 4, 5, 5, 5])
	level_height += random.choice([1, 2, 3, 3, 4, 4, 5, 5, 5])
	if level.finish == 'N':
		start_wall = 'S'
	elif level.finish == 'S':
		start_wall = 'N'
	elif level.finish == 'E':
		start_wall = 'W'
	elif level.finish == 'W':
		start_wall = 'E'
	else:
		print("\nERROR: Unacceptable value for level.finish\n")
		raise SystemExit
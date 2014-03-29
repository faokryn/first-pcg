import pygame, sys
from pygame.locals import *
from level import *

CHAR_SPEED = 10
CHAR_SIZE = 50
CELL_SIZE = 64
WINDOW_SIZE = 640

class Char_S(pygame.sprite.Sprite):
	def __init__(self, levelMap):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([CHAR_SIZE , CHAR_SIZE])
		self.image.fill((0,0,255))
		self.rect = self.image.get_rect()
		self.rect.left = CELL_SIZE + 1
		self.rect.top = CELL_SIZE + 1

	def up(self):
		if self.rect.top - CHAR_SPEED - CELL_SIZE//2 > 0:
			self.rect.move_ip(0, - CHAR_SPEED)
		else:
			for sprite in levelMap:
				sprite.rect.move_ip(0, CHAR_SPEED) 

		while pygame.sprite.spritecollide(self, levelMap, False) != []:
			self.rect.move_ip(0, 1)

	def down(self):
		if self.rect.bottom + CHAR_SPEED + CELL_SIZE//2 < WINDOW_SIZE:
			self.rect.move_ip(0, CHAR_SPEED)
		else:
			for sprite in levelMap:
				sprite.rect.move_ip(0, -CHAR_SPEED)

		while pygame.sprite.spritecollide(self, levelMap, False) != []:
			self.rect.move_ip(0, -1)

	def left(self):
		if self.rect.left - CHAR_SPEED - CELL_SIZE//2 > 0:
			self.rect.move_ip(- CHAR_SPEED, 0)
		else:
			for sprite in levelMap:
				sprite.rect.move_ip(CHAR_SPEED, 0)

		while pygame.sprite.spritecollide(self, levelMap, False) != []:
			self.rect.move_ip(1, 0)

	def right(self):
		if self.rect.right + CHAR_SPEED + CELL_SIZE//2 < WINDOW_SIZE:
			self.rect.move_ip(CHAR_SPEED, 0)
		else:
			for sprite in levelMap:
				sprite.rect.move_ip(- CHAR_SPEED, 0)

		while pygame.sprite.spritecollide(self, levelMap, False) != []:
			self.rect.move_ip(-1, 0)

class Wall_S(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
		self.image.fill((0,255,0))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = x*CELL_SIZE, y*CELL_SIZE

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Hello World!")


level = Level(30, 30)
levelMap = pygame.sprite.Group()
for cell in level.map:
	if isinstance(level.map[cell], Wall):
		levelMap.add(Wall_S( cell[0], cell[1] ))
char = Char_S(levelMap)

while True: # Game loop
	for event in pygame.event.get():
		# Check if game has been quit and quit
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pressedKeys = pygame.key.get_pressed()
	if pressedKeys[K_UP]:
		char.up()
	if pressedKeys[K_DOWN]:
		char.down()
	if pressedKeys[K_LEFT]:
		char.left()
	if pressedKeys[K_RIGHT]:
		char.right()

	screen.fill(( 255, 128,   0 ))

	levelMap.draw(screen)
	pygame.draw.rect(screen, (0,0,255), char)

	pygame.display.update()
	fpsClock.tick(30)
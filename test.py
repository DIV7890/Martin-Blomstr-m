import pygame as pg
import sys
import time
import pyautogui as pa

pg.init()

RED = (255, 0, 0)
screen_width, screen_height = pa.size()
screen_size = (screen_width, screen_height)
WINDOW_TITLE = "Error!"

HORIZONTAL = 1
UP = 2
DOWN = 0

FRAME_RATE = 60
ANIMATION_FRAME_RATE = 8

WINDOW = pg.display.set_mode((screen_size))
pg.display.set_caption(WINDOW_TITLE)

CLOCK = pg.time.Clock()

background = pg.transform.scale(pg.image.load("room_test.png"), screen_size)
screen = pg.display.set_mode(screen_size)


class StaticObstacle(pg.sprite.Sprite):
	def __init__(self,pos,size,groups):
		super().__init__(groups)
		self.image = pg.Surface(size, pg.SRCALPHA)
		self.image.fill((255, 0, 0, 255))
		self.rect = self.image.get_rect(topleft=pos)
		self.old_rect = self.rect.copy()


class MovingVerticalObstacle(StaticObstacle):
	def __init__(self,pos,size,groups):
		super().__init__(pos, size, groups)
		self.image.fill('green')
		self.pos = pg.math.Vector2(self.rect.topleft)
		self.direction = pg.math.Vector2((0,1))
		self.speed = 850
		self.old_rect = self.rect.copy()

	def update(self,dt):
		self.old_rect = self.rect.copy() # previous frame
		if self.rect.bottom > 600:
			self.rect.bottom = 600
			self.pos.y = self.rect.y
			self.direction.y *= -1
		if self.rect.bottom < 120:
			self.rect.bottom = 120
			self.pos.y = self.rect.y
			self.direction.y *= -1

		self.pos.y += self.direction.y * self.speed * dt
		self.rect.y = round(self.pos.y) # current frame

class MovingHorizontalObstacle(StaticObstacle):
	def __init__(self,pos,size,groups):
		super().__init__(pos, size, groups)
		self.image.fill('purple')
		self.pos = pg.math.Vector2(self.rect.topleft)
		self.direction = pg.math.Vector2((1,0))
		self.speed = 800
		self.old_rect = self.rect.copy()

	def update(self,dt):
		self.old_rect = self.rect.copy()
		if self.rect.right > 1000:
			self.rect.right = 1000
			self.pos.x = self.rect.x
			self.direction.x *= -1
		if self.rect.left < 600:
			self.rect.left = 600
			self.pos.x = self.rect.x
			self.direction.x *= -1

		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)

class Player(pg.sprite.Sprite):
	def __init__(self,groups,obstacles,players,width,height,image):
		super().__init__(groups)

		# image
		self.image = pg.Surface((width,height))
		image = pg.image.load(image).convert()  # Adjust the path to your image
		# Scale the image to match the size of the surface
		image = pg.transform.scale(image, (width,height))
		# Blit the image onto the surface
		self.image.blit(image, (0, 0))

		# position
		self.rect = self.image.get_rect(topleft = (640,360))
		self.old_rect = self.rect.copy()

		# movement
		self.pos = pg.math.Vector2(self.rect.topleft)
		self.direction = pg.math.Vector2()
		self.speed = 200
		self.obstacles = obstacles
		self.players = players  # Add reference to other players

	def collision(self,direction):
		collision_sprites = pg.sprite.spritecollide(self,self.obstacles,False)
		collision_players = pg.sprite.spritecollide(self, self.players, False)  # Check collision with other players
		collision_sprites.extend(collision_players)  # Combine collision lists

		if collision_sprites:
			if direction == 'horizontal':
				for sprite in collision_sprites:
					# collision on the right
					if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
						self.rect.right = sprite.rect.left
						self.pos.x = self.rect.x

					# collision on the left
					if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
						self.rect.left = sprite.rect.right
						self.pos.x = self.rect.x

			if direction == 'vertical':
				for sprite in collision_sprites:
					# collision on the bottom
					if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
						self.rect.bottom = sprite.rect.top
						self.pos.y = self.rect.y

					# collision on the top
					if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
						self.rect.top = sprite.rect.bottom
						self.pos.y = self.rect.y

	def update(self,dt):
		self.old_rect = self.rect.copy()

		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)
		self.collision('horizontal')
		self.pos.y += self.direction.y * self.speed * dt
		self.rect.y = round(self.pos.y)
		self.collision('vertical')

def input():
	keys = pg.key.get_pressed()
	if keys[pg.K_ESCAPE]:
		exit()
		# movement input
	if keys[pg.K_UP]:
		player1.direction.y = -1
	elif keys[pg.K_DOWN]:
		player1.direction.y = 1
	else:
		player1.direction.y = 0

	if keys[pg.K_RIGHT]:
		player1.direction.x = 1
	elif keys[pg.K_LEFT]:
		player1.direction.x = -1
	else:
		player1.direction.x = 0

	if keys[pg.K_w]:
		player2.direction.y = -1
	elif keys[pg.K_s]:
		player2.direction.y = 1
	else:
		player2.direction.y = 0

	if keys[pg.K_d]:
		player2.direction.x = 1
	elif keys[pg.K_a]:
		player2.direction.x = -1
	else:
		player2.direction.x = 0

# group setup
all_sprites = pg.sprite.Group()
collision_sprites = pg.sprite.Group()
player_sprites = pg.sprite.Group()  # Group for players

# sprite setup
StaticObstacle((0, 0),(0.042 * screen_width, screen_height),[all_sprites,collision_sprites])
StaticObstacle((screen_width - 0.042 * screen_width, 0), (0.042 * screen_width, screen_height),[all_sprites,collision_sprites])
StaticObstacle((0, screen_height - 0.034 * screen_height),(screen_width, 0.034 * screen_height),[all_sprites,collision_sprites])
StaticObstacle((0, 0), (screen_width / 2 - screen_width * 0.033, 0.245 * screen_height), [all_sprites,collision_sprites])
StaticObstacle((screen_width / 2 + screen_width * 0.033, 0), (screen_width / 2 - screen_width * 0.033, 0.245 * screen_height), [all_sprites,collision_sprites])
StaticObstacle((0, 0),(screen_width, 0.213 * screen_height),[all_sprites,collision_sprites])


player1 = Player(all_sprites,collision_sprites,player_sprites, 1.5 * 0.0234 * screen_width, 2 * 0.042 * screen_height,"player.png")
player2 = Player(all_sprites,collision_sprites,player_sprites, 1.5 * 0.0234 * screen_width, 2 * 0.042 * screen_height,"player.png")

player_sprites.add(player1, player2)
WINDOW.blit(background, (0, 0))

# loop
last_time = time.time()
while True:

	# delta time
	dt = time.time() - last_time
	last_time = time.time()
	input()

	# event loop
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()

	# drawing and updating the screen
	WINDOW.blit(background, (0, 0))
	all_sprites.update(dt)
	all_sprites.draw(screen)


	# display output
	pg.display.update()
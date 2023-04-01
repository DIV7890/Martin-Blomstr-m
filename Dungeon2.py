import pygame
import random
import time
import math
# Neigour
open = False
openK = False
pickup_weapon = False
play = False
prev_mpos = None

z = 0
pygame.init()

pygame.font.get_init()

TEXT_FONT = pygame.font.Font("dungeon.font.otf",32)
# Constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
Transparant = (0, 0, 0, 0)
WINDOW_SIZE = (1280, 710)
WINDOW_TITLE = "The game"
WINDOW_CENTER = (0, 0)
screen = pygame.display.set_mode((1280 , 720))

BOUNDS_X = (35, 1250)
BOUNDS_Y = (80, 585)

replay = False
Break = False

prev_mouse_state = pygame.mouse.get_pressed()
player = 0
target = 0
damage = 0.5
shoot_cooldown = 0.25
vapen = "pistol"
antal_oppnade_kistor_denna_runda = 0
unlock_chest = False
antal_hjartan = 0
hearts_on_screen = 0
HeartXposs1 = 0
HeartYposs1 = 0
HeartXposs2 = 0
HeartYposs2 = 0
HeartXposs3 = 0
HeartYposs3 = 0
HeartXposs4 = 0
HeartYposs4 = 0
HeartXposs5 = 0
HeartYposs5 = 0
ak47Xposs = 0
ak47Yposs = 0
AWPXposs = 0
AWPYposs = 0
Coin1 = 0
Coin2 = 0
Coin3 = 0
Coin4 = 0
Coin5 = 0
Coin6 = 0
Coin7 = 0
Coin8 = 0
Coin9 = 0
Coin10 = 0
CoinXposs1 = 0
CoinYposs1 = 0
CoinXposs2 = 0
CoinYposs2 = 0
CoinXposs3 = 0
CoinYposs3 = 0
CoinXposs4 = 0
CoinYposs4 = 0
CoinXposs5 = 0
CoinYposs5 = 0
CoinXposs6 = 0
CoinYposs6 = 0
CoinXposs7 = 0
CoinYposs7 = 0
CoinXposs8 = 0
CoinYposs8 = 0
CoinXposs9 = 0
CoinYposs9 = 0
CoinXposs10 = 0
CoinYposs10 = 0
coins_on_screen = 0
antal_coins = 0
ak47 = 0
AWP = 0

room_counter = 10
antal_kistor = 0
open_chest = 0
closed_chest = 0
keys_on_screen = 0
KeyXposs = 0
KeyYposs = 0
antal_nycklar = 1
number_of_enemys = 0
last_activation_time = 0
d = 0
a = 0
s = 0
w = 0
i = random.randint(1, 10)
antal_dorrar = 0
open_door = 0
closed_door = 0
door1 = 0
door0 = 0
HORIZONTAL = 1
UP = 2
DOWN = 0

FRAME_RATE = 60
ANIMATION_FRAME_RATE = 10

WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

CLOCK = pygame.time.Clock()


objects = []
bullets = []
enemies = []
Doors = []
weapons_on_ground = []

class button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self):
        global prev_mouse_state
        global curr_mouse_state
        global Break
        global prev_mpos
        screen.blit(self.image, self.rect.topleft)

        mpos = pygame.mouse.get_pos()
        curr_mouse_state = pygame.mouse.get_pressed()
        if mpos[0] in range(530, 748) and mpos[1] in range(123, 208) and prev_mouse_state[0] and not curr_mouse_state[0]:
            Break = True
        if  mpos[0] in range(528, 748) and mpos[1] in range(309, 393) and prev_mouse_state[0] and not curr_mouse_state[0]:
            print("exit pga du klickade på quit knappen")
            exit()

        prev_mouse_state = curr_mouse_state

class Object:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0, 0]
        self.collider = [width, height]

        objects.append(self)

    def draw(self):
        WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
        self.center = self.get_center()

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2


class Entity(Object):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, None)
        self.speed = speed

        self.tileset = load_tileset(tileset, 16, 16)
        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.frames = [0, 1, 0, 2]
        self.frame_timer = 0

    def change_direction(self):
        if self.velocity[0] < 0:
            self.direction = HORIZONTAL
            self.flipX = True
        elif self.velocity[0] > 0:
            self.direction = HORIZONTAL
            self.flipX = False
        elif self.velocity[1] > 0:
            self.direction = DOWN
        elif self.velocity[1] < 0:
            self.direction = UP

    def draw(self):
        image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction], (self.width, self.height))

        self.change_direction()

        image = pygame.transform.flip(image, self.flipX, False)
        WINDOW.blit(image, (self.x, self.y))

        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.frame = 0
            return

        self.frame_timer += 1

        if self.frame_timer < ANIMATION_FRAME_RATE:
            return

        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0

        self.frame_timer = 0

    def update(self):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()


class Player(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)
        self.health = self.max_health = 5
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        super().update()

        self.x = max(BOUNDS_X[0], min(self.x, BOUNDS_X[1] - self.width))
        self.y = max(BOUNDS_Y[0], min(self.y, BOUNDS_Y[1] - self.height))

        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height


class Enemy(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)
        self.max_width = width
        self.max_height = height
        self.width = 0
        self.height = 0

        if player.health <= 0:
            self.health = 0
        else:
            self.health = 6
        self.collider = [width / 2.5, height / 1.5]
        enemies.append(self)

        self.start_timer = 0

    def cooldown(self):
        if self.start_timer < 1:
            self.start_timer += 0.035
            self.x -= 0.5
            self.y -= 0.5
        self.width = int(self.max_width * self.start_timer)
        self.height = int(self.max_height * self.start_timer)

    def update(self):
        player_center = player.get_center()
        enemy_center = self.get_center()

        self.velocity = [player_center[0] - enemy_center[0], player_center[1] - enemy_center[1]]

        magnitude = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        self.velocity = [self.velocity[0] / magnitude * self.speed, self.velocity[1] / magnitude * self.speed]

        self.cooldown()
        if self.start_timer < 1:
            self.velocity = [0, 0]
        super().update()

    def change_direction(self):
        super().change_direction()

        if self.velocity[1] > self.velocity[0] > 0:
            self.direction = DOWN
        elif self.velocity[1] < self.velocity[0] < 0:
            self.direction = UP

    def take_damage(self, damage, antal_nycklar):
        self.health -= damage
        if self.health <= 0:
            self.destroy()
            r = random.randint(1, 100)
            global KeyXposs
            global KeyYposs
            global Key
            global keys_on_screen
            global HeartXposs1
            global HeartYposs1
            global HeartXposs2
            global HeartYposs2
            global HeartXposs3
            global HeartYposs3
            global HeartXposs4
            global HeartYposs4
            global HeartXposs5
            global HeartYposs5
            global hearts_on_screen
            global Heart1
            global Heart2
            global Heart3
            global Heart4
            global CoinXposs1
            global CoinYposs1
            global CoinXposs2
            global CoinYposs2
            global CoinXposs3
            global CoinYposs3
            global CoinXposs4
            global CoinYposs4
            global CoinXposs5
            global CoinYposs5
            global CoinXposs6
            global CoinYposs6
            global CoinXposs7
            global CoinYposs7
            global CoinXposs8
            global CoinYposs8
            global CoinXposs9
            global CoinYposs9
            global CoinXposs10
            global CoinYposs10
            global coins_on_screen
            global Coin1
            global Coin2
            global Coin3
            global Coin4
            global Coin5
            global Coin6
            global Coin7
            global Coin8
            global Coin9
            global Coin10

            if keys_on_screen == 0:
                if r == 1:
                    KeyXposs = self.x
                    KeyYposs = self.y
                    Key = Object(KeyXposs, KeyYposs, 32, 32, pygame.image.load("key.png"))
                    keys_on_screen += 1
            r = random.randint(1, 30)
            if r == 1:
                if hearts_on_screen < 4:
                    if hearts_on_screen == 0:
                        HeartXposs1 = self.x
                        HeartYposs1 = self.y
                        Heart1 = Object(HeartXposs1, HeartYposs1, 32, 32, pygame.image.load("full_heart.png"))
                        hearts_on_screen += 1

                    elif hearts_on_screen == 1:
                        HeartXposs2 = self.x
                        HeartYposs2 = self.y
                        Heart2 = Object(HeartXposs2, HeartYposs2, 32, 32, pygame.image.load("full_heart.png"))
                        hearts_on_screen += 1

                    elif hearts_on_screen == 2:
                        HeartXposs3 = self.x
                        HeartYposs3 = self.y
                        Heart3 = Object(HeartXposs3, HeartYposs3, 32, 32, pygame.image.load("full_heart.png"))
                        hearts_on_screen += 1

                    elif hearts_on_screen == 3:
                        HeartXposs4 = self.x
                        HeartYposs4 = self.y
                        Heart4 = Object(HeartXposs4, HeartYposs4, 32, 32, pygame.image.load("full_heart.png"))
                        hearts_on_screen += 1
            r = random.randint(1, 2)
            if r == 1:
                if coins_on_screen < 10:
                    if Coin1 not in objects:
                        CoinXposs1 = self.x
                        CoinYposs1 = self.y
                        Coin1 = Object(CoinXposs1 + 5, CoinYposs1 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin2 not in objects:
                        CoinXposs2 = self.x
                        CoinYposs2 = self.y
                        Coin2 = Object(CoinXposs2 + 5, CoinYposs2 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin3 not in objects:
                        CoinXposs3 = self.x
                        CoinYposs3 = self.y
                        Coin3 = Object(CoinXposs3 + 5, CoinYposs3 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin4 not in objects:
                        CoinXposs4 = self.x
                        CoinYposs4 = self.y
                        Coin4 = Object(CoinXposs4 + 5, CoinYposs4 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin5 not in objects:
                        CoinXposs5 = self.x
                        CoinYposs5 = self.y
                        Coin5 = Object(CoinXposs5 + 5, CoinYposs5 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin6 not in objects:
                        CoinXposs6 = self.x
                        CoinYposs6 = self.y
                        Coin6 = Object(CoinXposs6 + 5, CoinYposs6 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin7 not in objects:
                        CoinXposs7 = self.x
                        CoinYposs7 = self.y
                        Coin7 = Object(CoinXposs7 + 5, CoinYposs7 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin8 not in objects:
                        CoinXposs8 = self.x
                        CoinYposs8 = self.y
                        Coin8 = Object(CoinXposs8 + 5, CoinYposs8 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin9 not in objects:
                        CoinXposs9 = self.x
                        CoinYposs9 = self.y
                        Coin9 = Object(CoinXposs9 + 5, CoinYposs9 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

                    elif Coin10 not in objects:
                        CoinXposs10 = self.x
                        CoinYposs10 = self.y
                        Coin10 = Object(CoinXposs10 + 5, CoinYposs10 + 5, 25, 25, pygame.image.load("Coin.png"))
                        coins_on_screen += 1

    def destroy(self):
        objects.remove(self)
        enemies.remove(self)


is_game_over = False
player_input = {"left": False, "right": False, "up": False, "down": False}


class doors():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0, 0]
        self.collider = [width, height]

        objects.append(self)

    def draw(self):
        WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

    def update(self):
        self.draw()

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2


def check_input(key, value):
    global unlock_chest
    global pickup_weapon
    global AWPXposs
    global AWPYposs
    global replay
    if key == pygame.K_a:
        player_input["left"] = value
    elif key == pygame.K_d:
        player_input["right"] = value
    elif key == pygame.K_w:
        player_input["up"] = value
    elif key == pygame.K_s:
        player_input["down"] = value
    elif key == pygame.K_l:
        enemy_spawner1()
    elif key == pygame.K_o:
        ak47def()
    elif key == pygame.K_e:
        if antal_oppnade_kistor_denna_runda == 0:
            if player.x in range(int(WINDOW_SIZE[0] / 2 - 100), int(WINDOW_SIZE[0] / 2)) and player.y in range(int(WINDOW_SIZE[1] / 2 - 50),int(WINDOW_SIZE[1] / 2 + 50)) and closed_chest > 0 and antal_nycklar > 0:
                unlock_chest = True
    if key == pygame.K_e:
        if player.x in range(int(AWPXposs - 35), int(AWPXposs + 35)) and player.y in range(int(AWPYposs - 35), int(AWPYposs + 35)):
            pickup_weapon = True
        if player.x in range(int(ak47Xposs - 35), int(ak47Xposs + 35)) and player.y in range(int(ak47Yposs - 35), int(ak47Yposs + 35)):
            pickup_weapon = True
    elif key == pygame.K_p:
        replay = True
        print("du klickade p")





def load_tileset(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for tile_x in range(0, image_width // width):
        line = []
        tileset.append(line)
        for tile_y in range(0, image_height // height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tileset


def enemy_spawner1():
    for i in range(random.randint(5, 10)):
        enemy_spawner()


def enemy_spawner():
    for i in range(0, 1):
        randomx = random.randint(BOUNDS_X[0], BOUNDS_X[1] - 75)
        randomy = random.randint(BOUNDS_Y[0], BOUNDS_Y[1] - 75)
        enemy = Enemy(randomx, randomy, 55, 55, "goombas.png", 1.1)
        player_center = player.get_center()
        if abs(player_center[0] - enemy.x) < 250 and abs(player_center[1] - enemy.y) < 250:
            enemy.x = random.randint(BOUNDS_X[0], BOUNDS_X[1] - 75)
            enemy.y = random.randint(BOUNDS_Y[0], BOUNDS_Y[1] - 75)


def locked_chest(openK, open_chest, closed_chest, antal_kistor, w):
    global room_counter
    global chest1
    global chest0
    global antal_nycklar
    global key
    global antal_oppnade_kistor_denna_runda
    global unlock_chest
    global HeartXposs5
    global HeartYposs5
    global hearts_on_screen
    global Heart5
    global full_heart
    global chest_rect
    global ak47Xposs
    global ak47Yposs
    global ak47
    global z
    global AWPXposs
    global AWPYposs
    global AWP
    if math.gcd(15,room_counter) == 15 and len(enemies) == 0 and antal_kistor == 0 and room_counter != 0:
        chest1 = Object(WINDOW_SIZE[0] / 2 - 50, WINDOW_SIZE[1] / 2, 100, 100, pygame.image.load("closed_chest.png"))
        chest_rect = pygame.Rect(chest1.x, chest1.y, chest1.width, chest1.height)
        objects.remove(chest1)
        objects.insert(0, chest1)
        antal_kistor += 1
        closed_chest += 1
    if player.x in range(int(WINDOW_SIZE[0] / 2 - 100), int(WINDOW_SIZE[0] / 2)) and player.y in range(
            int(WINDOW_SIZE[1] / 2 - 50), int(WINDOW_SIZE[1] / 2 + 50)) and closed_chest > 0 and antal_nycklar > 0:
        if closed_chest > 0:
            if unlock_chest == True:
                if open_chest < 1:
                    chest0 = Object(WINDOW_SIZE[0] / 2 - 50, WINDOW_SIZE[1] / 2, 100, 100, pygame.image.load("open_chest.png"))
                    objects.remove(chest0)
                    objects.insert(0, chest0)
                    antal_kistor += 1
                    open_chest += 1
                    antal_oppnade_kistor_denna_runda += 1
                    objects.remove(chest1)
                    antal_kistor -= 1
                    closed_chest -= 1
                antal_nycklar -= 1
                unlock_chest = False
                r = random.randint(1, 10)
                if r < 11:
                    HeartXposs5 = (WINDOW_SIZE[0] / 2 - 20)
                    HeartYposs5 = (WINDOW_SIZE[1] / 2 - 100)
                    Heart5 = Object(HeartXposs5, HeartYposs5, 32, 32, pygame.image.load("full_heart.png"))
                    hearts_on_screen += 1
                if "ak47" not in weapons_on_ground:
                    r = random.randint(1, 1)
                    if r == 1:
                        ak47Xposs = (WINDOW_SIZE[0] / 2 + 100)
                        ak47Yposs = (WINDOW_SIZE[1] / 2)
                        ak47 = Object(ak47Xposs, ak47Yposs, 32, 32, pygame.image.load("ak47.png"))
                        weapons_on_ground.append("ak47")
                if "AWP" not in weapons_on_ground:
                    r = random.randint(1, 1)
                    if r == 1:
                        AWPXposs = (WINDOW_SIZE[0] / 2 + 20)
                        AWPYposs = (WINDOW_SIZE[1] / 2 - 50)
                        AWP = Object(AWPXposs, AWPYposs, 32, 32, pygame.image.load("AWP.png"))
                        weapons_on_ground.append("AWP")

    if math.gcd(15,room_counter) != 15 and room_counter != 0:
        if antal_kistor != 0:
            if closed_chest != 0:
                while closed_chest > 0:
                    objects.remove(chest1)
                    closed_chest -= 1
                    antal_kistor -= 1
            if open_chest != 0:
                while open_chest > 0:
                    objects.remove(chest0)
                    open_chest -= 1
                    antal_kistor -= 1
        if "ak47" in weapons_on_ground:
            objects.remove(ak47)
            weapons_on_ground.remove("ak47")
        if "AWP" in weapons_on_ground:
            objects.remove(AWP)
            weapons_on_ground.remove("AWP")

    return openK, open_chest, closed_chest, antal_kistor


def locked_door(closed, open_door, closed_door,antal_dorrar):
    global door1
    global door0
    if closed == False: # dörren ska vara öppen
        if antal_dorrar == 0: #Skapar första dörren
            door0 = Object(WINDOW_SIZE[0] / 2 - 50, 17, 100, 100, pygame.image.load("opened_door.png"))
            objects.remove(door0)
            objects.insert(0,door0)
            open_door += 1
            antal_dorrar += 1
        elif closed_door != 0: #går från en stängd dörr till en öppen dörr
            if open_door == 0:
                objects.remove(door1)
                door0 = Object(WINDOW_SIZE[0] / 2 - 50, 17, 100, 100, pygame.image.load("opened_door.png"))
                objects.remove(door0)
                objects.insert(1, door0)
                open_door += 1
                closed_door -= 1

    if closed == True: # dörren ska vara stängd
        if open_door != 0: #går från en öppen dörr till en stängd dörr
            if closed_door == 0:
                objects.remove(door0)
                door1 = Object(WINDOW_SIZE[0] / 2 - 50, 17, 100, 100, pygame.image.load("closed_door.png"))
                objects.remove(door1)
                objects.insert(1, door1)
                closed_door += 1
                open_door -= 1

    return closed, open_door, closed_door, antal_dorrar


# test_object = Object(400, 400, 500, 500, pygame.image.load("pixilart-drawing (6).png"))
# test_entity = Entity(400, 400, 50, 50, "player-sheet.png", 5)


def ak47def():
    global vapen
    global shoot_cooldown
    global damage
    global weapon
    shoot_cooldown = 0.075
    damage = 1
    vapen = "ak47"
def AWPdef():
    global vapen
    global shoot_cooldown
    global damage
    global weapon
    shoot_cooldown = 1.5
    damage = 100
    vapen = "AWP"
def shoot():
    global last_activation_time
    current_time = time.time()
    if current_time - last_activation_time >= shoot_cooldown:
        player_center = player.get_center()
        bullet = Object(player_center[0], player_center[1], 16, 16, pygame.image.load("bullet.png"))

        target_center = target.get_center()
        bullet.velocity = [target_center[0] - player_center[0], target_center[1] - player_center[1]]

        magnitude = (bullet.velocity[0] ** 2 + bullet.velocity[1] ** 2) ** 0.5

        bullet.velocity = [bullet.velocity[0] / magnitude * 10, bullet.velocity[1] / magnitude * 10]

        bullets.append(bullet)
        last_activation_time = current_time

def check_collisions(obj1, obj2):
    x1, y1 = obj1.get_center()
    x2, y2 = obj2.get_center()
    w1, h1 = obj1.collider[0] / 2, obj1.collider[1] / 2
    w2, h2 = obj2.collider[0] / 2, obj2.collider[1] / 2
    if x1 + w1 > x2 - w2 and x1 - w1 < x2 + w2:
        return y1 + h1 > y2 - h2 and y1 - h1 < y2 + h2
    return False


def display_ui():
    global antal_nycklar
    for i in range(player.max_health):
        img = pygame.image.load("empty_heart.png" if i >= player.health else "full_heart.png")
        img = pygame.transform.scale(img, (50, 50))
        WINDOW.blit(img, (i * 50 + WINDOW_SIZE[0] / 2 - player.max_health * 25 - 300, 25))

    keys_displayed = TEXT_FONT.render(f"{antal_nycklar}", True, BLACK)
    WINDOW.blit(keys_displayed, (765, 45))

    coins_displayed = TEXT_FONT.render(f"{antal_coins}", True, BLACK)
    WINDOW.blit(coins_displayed, (900, 45))

    keys_displayed = TEXT_FONT.render(f"{antal_nycklar}", True, BLACK)
    WINDOW.blit(keys_displayed, (765, 45))
    next_room = TEXT_FONT.render(f"{room_counter + 1}", True, BLACK)
    WINDOW.blit(next_room, (WINDOW_SIZE[0] / 2 - 10, 0))



def update_screen():
    CLOCK.tick(FRAME_RATE)
    pygame.display.update()
def playing():
    print("du är nu I paying")
    global s
    global unlock_chest
    global number_of_enemys
    global shoot_cooldown
    global i
    global replay
    global a
    global b
    global d
    global antal_hjartan
    global antal_coins
    global is_game_over
    global open
    global open_door
    global closed_door
    global antal_dorrar
    global hearts_on_screen
    global coins_on_screen
    global ak47Xposs
    global ak47Yposs
    global AWPXposs
    global AWPYposs
    global openK
    global open_chest
    global closed_chest
    global antal_kistor
    global room_counter
    global keys_on_screen
    global antal_nycklar
    global HeartXposs1
    global HeartYposs1
    global HeartXposs2
    global HeartYposs2
    global HeartXposs3
    global HeartYposs3
    global HeartXposs4
    global HeartYposs4
    global HeartXposs5
    global HeartYposs5
    global hearts_on_screen
    global Heart1
    global Heart2
    global Heart3
    global Heart4
    global CoinXposs1
    global CoinYposs1
    global CoinXposs2
    global CoinYposs2
    global CoinXposs3
    global CoinYposs3
    global CoinXposs4
    global CoinYposs4
    global CoinXposs5
    global CoinYposs5
    global CoinXposs6
    global CoinYposs6
    global CoinXposs7
    global CoinYposs7
    global CoinXposs8
    global CoinYposs8
    global CoinXposs9
    global CoinYposs9
    global CoinXposs10
    global CoinYposs10
    global Coin1
    global Coin2
    global Coin3
    global Coin4
    global Coin5
    global Coin6
    global Coin7
    global Coin8
    global Coin9
    global Coin10
    global pickup_weapon
    global antal_oppnade_kistor_denna_runda
    global player
    global target
    global KeyXposs
    global KeyYposs
    global w
    global damage
    screen.fill((0,0,0))
    pygame.display.update()
    background = pygame.transform.scale(pygame.image.load("background.png"), WINDOW_SIZE)
    player = Player(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, 55, 55, "The_man.png", 3)

    target = Object(0, 0, 40, 40, pygame.image.load("cursor.png"))

    pygame.mouse.set_visible(False)
    run = True
    while run:
        if replay:
            damage = 0.5
            shoot_cooldown = 0.25
            vapen = "pistol"
            antal_oppnade_kistor_denna_runda = 0
            unlock_chest = False
            antal_hjartan = 0
            hearts_on_screen = 0
            HeartXposs1 = 0
            HeartYposs1 = 0
            HeartXposs2 = 0
            HeartYposs2 = 0
            HeartXposs3 = 0
            HeartYposs3 = 0
            HeartXposs4 = 0
            HeartYposs4 = 0
            HeartXposs5 = 0
            HeartYposs5 = 0
            ak47Xposs = 0
            ak47Yposs = 0
            AWPXposs = 0
            AWPYposs = 0
            Coin1 = 0
            Coin2 = 0
            Coin3 = 0
            Coin4 = 0
            Coin5 = 0
            Coin6 = 0
            Coin7 = 0
            Coin8 = 0
            Coin9 = 0
            Coin10 = 0
            CoinXposs1 = 0
            CoinYposs1 = 0
            CoinXposs2 = 0
            CoinYposs2 = 0
            CoinXposs3 = 0
            CoinYposs3 = 0
            CoinXposs4 = 0
            CoinYposs4 = 0
            CoinXposs5 = 0
            CoinYposs5 = 0
            CoinXposs6 = 0
            CoinYposs6 = 0
            CoinXposs7 = 0
            CoinYposs7 = 0
            CoinXposs8 = 0
            CoinYposs8 = 0
            CoinXposs9 = 0
            CoinYposs9 = 0
            CoinXposs10 = 0
            CoinYposs10 = 0
            coins_on_screen = 0
            antal_coins = 0
            ak47 = 0
            AWP = 0

            room_counter = 10
            antal_kistor = 0
            open_chest = 0
            closed_chest = 0
            keys_on_screen = 0
            KeyXposs = 0
            KeyYposs = 0
            antal_nycklar = 1
            number_of_enemys = 0
            d = 0
            a = 0
            s = 0
            w = 0
            i = random.randint(1, 10)
            antal_dorrar = 0
            open_door = 0
            closed_door = 0
            replay = False
        while a < 1:
            player.x = player.x = WINDOW_SIZE[0] / 2 - 25
            player.y = WINDOW_SIZE[1]
            a += 1
        else:
            while d < 1:
                closed_door_bottom = Object(WINDOW_SIZE[0] / 2 - 50, WINDOW_SIZE[1] - 125, 100, 100,pygame.image.load("closed_door_bottom.png"))
                objects.remove(closed_door_bottom)
                objects.insert(0, closed_door_bottom)
                nyckel = Object(700, 37, 48, 48, pygame.image.load("key_display.png"))
                objects.insert(0, nyckel)
                d += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("planerad exit i play funktionen")
                exit()
            elif event.type == pygame.KEYDOWN:
                check_input(event.key, True)
            elif event.type == pygame.KEYUP:
                check_input(event.key, False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shoot()
        mousePos = pygame.mouse.get_pos()
        target.x = mousePos[0] - target.width / 2
        target.y = mousePos[1] - target.height / 2

        player.velocity[0] = player_input["right"] - player_input["left"]
        player.velocity[1] = player_input["down"] - player_input["up"]

        WINDOW.blit(background, WINDOW_CENTER)

        if is_game_over:
            pygame.mouse.set_visible(True)
            update_screen()
            continue

        open, open_door, closed_door, antal_dorrar = locked_door(open, open_door, closed_door, antal_dorrar)

        display_ui()

        for obj in objects:
            obj.update()

        for b in bullets:
            if BOUNDS_X[0] <= b.x <= BOUNDS_X[1] and BOUNDS_Y[0] <= b.y <= BOUNDS_Y[1]:
                continue
            bullets.remove(b)
            objects.remove(b)

        for e in enemies:
            if check_collisions(player, e):
                player.health -= 1
                e.destroy()
                continue
            for b in bullets:
                if check_collisions(b, e):
                    e.take_damage(damage, antal_nycklar)
                    if vapen != "AWP":
                        bullets.remove(b)
                        objects.remove(b)

        if len(enemies) != 0:
            open = True
        elif len(enemies) == 0:
            open = False

        if KeyXposs != 0 and KeyYposs != 0 and keys_on_screen != 0:
            if player.x in range(int(KeyXposs - 70), int(KeyXposs + 70)) and player.y in range(int(KeyYposs - 70),
                                                                                               int(KeyYposs + 70)):
                print("Du har rört en nyckel!")
                antal_nycklar += 1
                objects.remove(Key)
                keys_on_screen -= 1

        if hearts_on_screen != 0:
            if HeartXposs1 != 0 and HeartYposs1 != 0:
                if player.x in range(int(HeartXposs1 - 70), int(HeartXposs1 + 70)) and player.y in range(
                        int(HeartYposs1 - 70), int(HeartYposs1 + 70)) and player.health != 5 and Heart1 in objects:
                    print("Du har rört ett hjärta!")
                    objects.remove(Heart1)
                    hearts_on_screen -= 1
                    player.health += 1

            if HeartXposs2 != 0 and HeartYposs2 != 0:
                if player.x in range(int(HeartXposs2 - 70), int(HeartXposs2 + 70)) and player.y in range(
                        int(HeartYposs2 - 70), int(HeartYposs2 + 70)) and player.health != 5 and Heart2 in objects:
                    print("Du har rört ett hjärta!")
                    objects.remove(Heart2)
                    hearts_on_screen -= 1
                    player.health += 1

            if HeartXposs3 != 0 and HeartYposs3 != 0:
                if player.x in range(int(HeartXposs3 - 70), int(HeartXposs3 + 70)) and player.y in range(
                        int(HeartYposs3 - 70), int(HeartYposs3 + 70)) and player.health != 5 and Heart3 in objects:
                    print("Du har rört ett hjärta!")
                    objects.remove(Heart3)
                    hearts_on_screen -= 1
                    player.health += 1

            if HeartXposs4 != 0 and HeartYposs4 != 0:
                if player.x in range(int(HeartXposs4 - 70), int(HeartXposs4 + 70)) and player.y in range(
                        int(HeartYposs4 - 70), int(HeartYposs4 + 70)) and player.health != 5 and Heart4 in objects:
                    print("Du har rört ett härta!")
                    objects.remove(Heart4)
                    hearts_on_screen -= 1
                    player.health += 1

            if HeartXposs5 != 0 and HeartYposs5 != 0:
                if player.x in range(int(HeartXposs5 - 70), int(HeartXposs5 + 70)) and player.y in range(
                        int(HeartYposs5 - 70), int(HeartYposs5 + 70)) and player.health != 5 and Heart5 in objects:
                    print("Du har rört ett härta!")
                    objects.remove(Heart5)
                    hearts_on_screen -= 1
                    player.health += 1

        if coins_on_screen != 0:
            if CoinXposs1 != 0 and CoinYposs1 != 0:
                if player.x in range(int(CoinXposs1 - 70), int(CoinXposs1 + 70)) and player.y in range(
                        int(CoinYposs1 - 70), int(CoinYposs1 + 70)) and Coin1 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin1)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs2 != 0 and CoinYposs2 != 0:
                if player.x in range(int(CoinXposs2 - 70), int(CoinXposs2 + 70)) and player.y in range(
                        int(CoinYposs2 - 70), int(CoinYposs2 + 70)) and Coin2 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin2)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs3 != 0 and CoinYposs3 != 0:
                if player.x in range(int(CoinXposs3 - 70), int(CoinXposs3 + 70)) and player.y in range(
                        int(CoinYposs3 - 70), int(CoinYposs3 + 70)) and Coin3 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin3)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs4 != 0 and CoinYposs4 != 0:
                if player.x in range(int(CoinXposs4 - 70), int(CoinXposs4 + 70)) and player.y in range(
                        int(CoinYposs4 - 70), int(CoinYposs4 + 70)) and Coin4 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin4)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs5 != 0 and CoinYposs5 != 0:
                if player.x in range(int(CoinXposs5 - 70), int(CoinXposs5 + 70)) and player.y in range(
                        int(CoinYposs5 - 70), int(CoinYposs5 + 70)) and Coin5 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin5)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs6 != 0 and CoinYposs6 != 0:
                if player.x in range(int(CoinXposs6 - 70), int(CoinXposs6 + 70)) and player.y in range(
                        int(CoinYposs6 - 70), int(CoinYposs6 + 70)) and Coin6 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin6)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs7 != 0 and CoinYposs7 != 0:
                if player.x in range(int(CoinXposs7 - 70), int(CoinXposs7 + 70)) and player.y in range(
                        int(CoinYposs7 - 70), int(CoinYposs7 + 70)) and Coin7 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin7)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs8 != 0 and CoinYposs8 != 0:
                if player.x in range(int(CoinXposs8 - 70), int(CoinXposs8 + 70)) and player.y in range(
                        int(CoinYposs8 - 70), int(CoinYposs8 + 70)) and Coin8 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin8)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs9 != 0 and CoinYposs9 != 0:
                if player.x in range(int(CoinXposs9 - 70), int(CoinXposs9 + 70)) and player.y in range(
                        int(CoinYposs9 - 70), int(CoinYposs9 + 70)) and Coin9 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin9)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs10 != 0 and CoinYposs10 != 0:
                if player.x in range(int(CoinXposs10 - 70), int(CoinXposs10 + 70)) and player.y in range(
                        int(CoinYposs10 - 70), int(CoinYposs10 + 70)) and Coin10 in objects:
                    print("Du har rört ett coin!")
                    objects.remove(Coin10)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

        if player.x in range(int(WINDOW_SIZE[0] / 2 - 70), int(WINDOW_SIZE[0] / 2 + 15)) and player.y in range(17, 84):
            if len(enemies) == 0:
                room_counter += 1
                if keys_on_screen != 0:
                    objects.remove(Key)
                    keys_on_screen -= 1
                if hearts_on_screen != 0:
                    if HeartXposs1 != 0 and HeartYposs1 != 0 and Heart1 in objects:
                        objects.remove(Heart1)
                    if HeartXposs2 != 0 and HeartYposs2 != 0 and Heart2 in objects:
                        objects.remove(Heart2)
                    if HeartXposs3 != 0 and HeartYposs3 != 0 and Heart3 in objects:
                        objects.remove(Heart3)
                    if HeartXposs4 != 0 and HeartYposs4 != 0 and Heart4 in objects:
                        objects.remove(Heart4)
                    if HeartXposs5 != 0 and HeartYposs5 != 0 and Heart5 in objects:
                        objects.remove(Heart5)

                if coins_on_screen != 0:
                    if CoinXposs1 != 0 and CoinYposs1 != 0 and Coin1 in objects:
                        CoinXposs1 = 0
                        CoinYposs1 = 0
                        objects.remove(Coin1)
                        coins_on_screen -= 1
                    if CoinXposs2 != 0 and CoinYposs2 != 0 and Coin2 in objects:
                        CoinXposs2 = 0
                        CoinYposs2 = 0
                        objects.remove(Coin2)
                        coins_on_screen -= 1
                    if CoinXposs3 != 0 and CoinYposs3 != 0 and Coin3 in objects:
                        CoinXposs3 = 0
                        CoinYposs3 = 0
                        objects.remove(Coin3)
                        coins_on_screen -= 1
                    if CoinXposs4 != 0 and CoinYposs4 != 0 and Coin4 in objects:
                        CoinXposs4 = 0
                        CoinYposs4 = 0
                        objects.remove(Coin4)
                        coins_on_screen -= 1
                    if CoinXposs5 != 0 and CoinYposs5 != 0 and Coin5 in objects:
                        CoinXposs5 = 0
                        CoinYposs5 = 0
                        objects.remove(Coin5)
                        coins_on_screen -= 1
                    if CoinXposs6 != 0 and CoinYposs6 != 0 and Coin6 in objects:
                        CoinXposs6 = 0
                        CoinYposs6 = 0
                        objects.remove(Coin6)
                        coins_on_screen -= 1
                    if CoinXposs7 != 0 and CoinYposs7 != 0 and Coin7 in objects:
                        CoinXposs7 = 0
                        CoinYposs7 = 0
                        objects.remove(Coin7)
                        coins_on_screen -= 1
                    if CoinXposs8 != 0 and CoinYposs8 != 0 and Coin8 in objects:
                        CoinXposs8 = 0
                        CoinYposs8 = 0
                        objects.remove(Coin8)
                        coins_on_screen -= 1
                    if CoinXposs9 != 0 and CoinYposs9 != 0 and Coin9 in objects:
                        CoinXposs9 = 0
                        CoinYposs9 = 0
                        objects.remove(Coin9)
                        coins_on_screen -= 1
                    if CoinXposs10 != 0 and CoinYposs10 != 0 and Coin10 in objects:
                        CoinXposs10 = 0
                        CoinYposs10 = 0
                        objects.remove(Coin10)
                        coins_on_screen -= 1

                player.x = WINDOW_SIZE[0] / 2 - 25
                player.y = WINDOW_SIZE[1]
                enemy_spawner1()
                antal_oppnade_kistor_denna_runda = 0
                hearts_on_screen = 0
                coins_on_screen = 0

        if player.x in range(int(ak47Xposs - 35), int(ak47Xposs + 35)) and player.y in range(int(ak47Yposs - 35),int(ak47Yposs + 35)) and ak47 in objects and pickup_weapon == True:
            objects.remove(ak47)
            ak47def()
            print("du har rört en ak47")
            pickup_weapon = False
            weapons_on_ground.remove("ak47")
            ak47Xposs = 0
            ak47Yposs = 0

        if player.x in range(int(AWPXposs - 35), int(AWPXposs + 35)) and player.y in range(int(AWPYposs - 35),int(AWPYposs + 35)) and "AWP" in weapons_on_ground and pickup_weapon == True:
            objects.remove(AWP)
            AWPdef()
            print("du har rört en AWP")
            pickup_weapon = False
            weapons_on_ground.remove("AWP")
            AWPXposs = 0
            AWPYposs = 0

        openK, open_chest, closed_chest, antal_kistor = locked_chest(openK, open_chest, closed_chest, antal_kistor, w)

        if closed_chest != 0:
            # vänstra sidan stängd kista
            if player.y < 382 and player.y > 337 and player.x in range(568, 580):
                player.x = 568
            # högra sidan stängd kista
            if player.y < 382 and player.y > 337 and player.x in range(650, 655):
                player.x = 657
            # övre sidan stängd kista
            if player.x < 646 and player.x > 572 and player.y in range(334, 370):
                player.y = 334
            # nedre sidan stängd kista
            if player.x < 646 and player.x > 572 and player.y in range(380, 385):
                player.y = 385
        if open_chest != 0:
            # vänstra sidan öppen ksta
            if player.y < 382 and player.y > 325 and player.x in range(568, 580):
                player.x = 568
            # högra sidan öppen kista
            if player.y < 382 and player.y > 325 and player.x in range(650, 655):
                player.x = 657
            # övre sidan öppen kista
            if player.x < 646 and player.x > 572 and player.y in range(325, 330):
                player.y = 325
            # nedre sidan öppen kista
            if player.x < 646 and player.x > 572 and player.y in range(380, 385):
                player.y = 385
        if player.health <= 0:
            pygame.mouse.set_visible(True)
            run = False
            if door0 in objects:
                objects.remove(door0)
            if door1 in objects:
                objects.remove(door1)
            objects.remove(target)
            update_screen()
            home_screen()
            continue
        update_screen()
def home_screen():
    print("du är nu i home screen")
    global mpos
    global Break
    global replay
    pygame.mouse.set_visible(True)
    mpos = pygame.mouse.get_pos()
    background = pygame.transform.scale(pygame.image.load("home_screen.jpg"), (1280, 720))
    start_image = pygame.image.load("start_button.png").convert_alpha()
    start_button = button(640, 200, start_image, 7)
    quit_image = pygame.image.load("quit_button.png").convert_alpha()
    quit_button = button(640, 400, quit_image, 7)
    while True:
        update_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("planerad exit")
                exit()
        WINDOW.blit(background, WINDOW_CENTER)
        start_button.draw()
        quit_button.draw()
        print(Break)
        if Break == True:
            replay = True
            Break = False
            print(Break)
            playing()
            break

home_screen()

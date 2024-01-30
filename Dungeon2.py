import pygame
import random
import time
import math
from pygame import mixer
# Neigour

open = False
openK = False
pickup_weapon = False
pickup_object = False
play = False
prev_mpos = None
music_playing = True
playlist = ["GD_level1.mp3","GD_level2.mp3"]
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

replay = True
Break = False


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
objects_on_ground = []
players = []


# Instantiate mixer
mixer.init()

# Load audio file
mixer.music.load('GD_level1.mp3')


# Set preferred volume
mixer.music.set_volume(0.2)

# Play the music
mixer.music.play()

def doWork(): # bestämmer hur lång tid en loading bar till reloadingen ska vara (vi hann inte färdigt)
    global loading_finished
    global loading_progress
    for i in range(WORK):
        math_equation = 523687 / 789456 * 89456
        loading_progress = i
    loading_finished = True


def play_music(KEY): # gör en definition som spelar musik
    global music_playing
    global key_down
    global playlist_index
    global playlist
    key_down += 1
    if key_down == 2:
        key_down = 0
    if KEY == pygame.K_p:
        if key_down == 1:
            if music_playing == True:
                # Pause the music
                mixer.music.pause()
                music_playing = False
            else:
                # Resume the music
                mixer.music.unpause()
                music_playing = True

    elif KEY == pygame.K_n:
        if key_down == 1:
            if playlist_index == len(playlist):
                playlist_index = 0
            mixer.music.load(playlist[playlist_index])
            mixer.music.play()
            playlist_index += 1


class button(): #Glör en klass för knappar. Klassen tar i omtanke vad som händer när man skapar en knapp.
    # t.ex ritar upp knappen eller beräknar dess "bounderies"
    def __init__(self,x,y,image,scale): # Skapar knappen
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self): # ritar upp en knapp
        global prev_mouse_state
        global curr_mouse_state
        global Break
        global prev_mpos
        global Finish_screen
        global Home_screen
        global Pause
        global Play_again
        screen.blit(self.image, self.rect.topleft)

        mpos = pygame.mouse.get_pos()
        curr_mouse_state = pygame.mouse.get_pressed()
        if Home_screen or Pause or Play_again:
            if mpos[0] in range(530, 748) and mpos[1] in range(123, 208) and prev_mouse_state[0] and not \
            curr_mouse_state[0]:
                Break = True
                mixer.music.unpause()
            if mpos[0] in range(528, 748) and mpos[1] in range(309, 393) and prev_mouse_state[0] and not \
            curr_mouse_state[0]:
                exit()

        elif Finish_screen:
            if mpos[0] in range(328, 551) and mpos[1] in range(488, 560) and prev_mouse_state[0] and not \
                    curr_mouse_state[0]:
                Break = True
                mixer.music.unpause()
            if mpos[0] in range(728, 948) and mpos[1] in range(488, 560) and prev_mouse_state[0] and not \
                    curr_mouse_state[0]:
                exit()

        prev_mouse_state = curr_mouse_state


class Object: # Gör en klass för "objects". I denna klass finns saker som inte rör sig men man kanske
    # vill interagera med. Exempel på sånt är dörrar som man vill gå igenom.
    # När man vill "spawna" in grejer måste de tillhöra en klass, ofta tilldelar vi de "objects-klassen"
    def __init__(self, x, y, width, height, image): # skapar objektet
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0, 0]
        self.collider = [width, height]

        objects.append(self)

    def draw(self): # ritar upp objektet
        WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
        self.center = self.get_center()

    def update(self): # uppdaterar objektet
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def get_center(self): # bestämmer ett centrum på objektet
        return self.x + self.width / 2, self.y + self.height / 2


class Entity(Object): # Allting är objects som man kan se i classen (värdet som stopppas in i entity classen) Entity är sedanen typ av objects. Entity bestämmer hur en entity beter sig och vad den ska göra.
    def __init__(self, x, y, width, height, tileset, speed): # skapar en entity
        super().__init__(x, y, width, height, None)
        self.speed = speed

        self.tileset = load_tileset(tileset, 16, 16)
        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.frames = [0, 1, 0, 2]
        self.frame_timer = 0

    def change_direction(self): # bestämmer vad som händer när en entity ändrar riktning
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

    def draw(self): # ritar upp entites
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

    def update(self): # Uppdaterar entities
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()


class Player(Entity): # Skapar spelaren och bestämmer vad och hur den ska göra någonting.
    def __init__(self, x, y, width, height, tileset, speed):  #skapar spelaren
        super().__init__(x, y, width, height, tileset, speed)
        self.health = self.max_health = 5
        self.rect = pygame.Rect(x, y, width, height)

    def handle_weapons(self, display): # gör så att vapnet snurrar runt spelaren
        target.x, target.y = pygame.mouse.get_pos()

        rel_x, rel_y = target.x - player.x, target.y - player.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        target.x_b, target.y_b = pygame.mouse.get_pos()

        rel_x_b, rel_y_b = target.x_b - player.x, target.y_b - player.y
        angle_b = (180 / math.pi) * +math.atan2(rel_y_b, rel_x_b)

        Newb_pistol_copy = pygame.transform.rotate(Newb_pistol, angle)
        Newb_pistol_copy2 = pygame.transform.rotate(Newb_pistol_flip, angle)
        if rel_x > 0:
            display.blit(Newb_pistol_copy, (
                self.x + 35 - int(Newb_pistol_copy.get_width() / 2),
                self.y + 35 - int(Newb_pistol_copy.get_height() / 2)))
        else:
            display.blit(Newb_pistol_copy2, (
                self.x + 35 - int(Newb_pistol_copy2.get_width() / 2),
                self.y + 35 - int(Newb_pistol_copy2.get_height() / 2)))

    def update(self): # uppdaterar spelaren
        super().update()
        self.handle_weapons(WINDOW)

        self.x = max(BOUNDS_X[0], min(self.x, BOUNDS_X[1] - self.width))
        self.y = max(BOUNDS_Y[0], min(self.y, BOUNDS_Y[1] - self.height))

        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height


class Enemy(Entity): # Spawnar enemies och bestämmer deras hitbox, snabbhet, liv, osv
    def __init__(self, x, y, width, height, tileset, speed): # skapar en varelse som är en mortståndare
        super().__init__(x, y, width, height, tileset, speed)
        self.max_width = width
        self.max_height = height
        self.width = 0
        self.height = 0

        if player.health <= 0:
            self.health = 0
        elif room_counter <= 20:
            self.health = 3
        else:
            self.health = 7
        self.collider = [width / 2.5, height / 1.5]
        enemies.append(self)

        self.start_timer = 0

    def cooldown(self): # definerar en cooldown
        if self.start_timer < 1:
            self.start_timer += 0.035
            self.x -= 0.5
            self.y -= 0.5
        self.width = int(self.max_width * self.start_timer)
        self.height = int(self.max_height * self.start_timer)

    def update(self): # uppdaterar motstondarna
        player_center = player.get_center()
        enemy_center = self.get_center()

        if player.health <= 0:
            self.health = 0

        self.velocity = [player_center[0] - enemy_center[0], player_center[1] - enemy_center[1]]

        magnitude = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        self.velocity = [self.velocity[0] / magnitude * self.speed, self.velocity[1] / magnitude * self.speed]

        self.cooldown()
        if self.start_timer < 1:
            self.velocity = [0, 0]
        super().update()

    def change_direction(self): # Definerar vad som ska hända när man vill byta riktining
        super().change_direction()

        if self.velocity[1] > self.velocity[0] > 0:
            self.direction = DOWN
        elif self.velocity[1] < self.velocity[0] < 0:
            self.direction = UP

    def take_damage(self, damage, antal_nycklar): # Bestämmer om någonting ska droppas när man dödar en enemy
        self.health -= damage
        if self.health <= 0 or player.health <= 0:
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

    def destroy(self): # kollar om ett objekt ska förstöras
        objects.remove(self)
        enemies.remove(self)


is_game_over = False
player_input = {"left": False, "right": False, "up": False, "down": False}

def check_input(key, value): # kollar om en knapp är nedtryckt
    global unlock_chest
    global pickup_weapon
    global pickup_object
    global AWPXposs
    global AWPYposs
    global replay
    global rounds_left
    global reloading
    global room_counter
    play_music(key)
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
    elif key == pygame.K_u:
        room_counter += 5
    if key == pygame.K_e:
        if player.x in range(int(AWPXposs - 35), int(AWPXposs + 35)) and player.y in range(int(AWPYposs - 35), int(AWPYposs + 35)):
            pickup_weapon = True
        if player.x in range(int(ak47Xposs - 35), int(ak47Xposs + 35)) and player.y in range(int(ak47Yposs - 35), int(ak47Yposs + 35)):
            pickup_weapon = True
        if player.x in range(int(ammoXposs - 35), int(ammoXposs + 35)) and player.y in range(int(ammoYposs - 35), int(ammoYposs + 35)):
            pickup_object = True
    elif key == pygame.K_r:
        reloading = True
    elif key == pygame.K_ESCAPE:
        mixer.music.pause()
        pause()


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


def enemy_spawner1(): #spawnar in mobs
    if room_counter <= 10:
        for i in range(random.randint(3, 6)):
            enemy_spawner()
    elif room_counter <= 20:
        for i in range(random.randint(4, 8)):
            enemy_spawner()
    elif room_counter <= 30:
        for i in range(random.randint(5, 10)):
            enemy_spawner()
    elif room_counter <= 40:
        for i in range(random.randint(6, 12)):
            enemy_spawner()
    else:
        for i in range(random.randint(7, 14)):
            enemy_spawner()

def enemy_spawner(): # Spawnar in mobs
    global enemy
    for i in range(0, 1):
        randomx = random.randint(BOUNDS_X[0], BOUNDS_X[1] - 75)
        randomy = random.randint(BOUNDS_Y[0], BOUNDS_Y[1] - 75)
        enemy = Enemy(randomx, randomy, 55, 55, "goombas.png", 1.1)
        player_center = player.get_center()
        if abs(player_center[0] - enemy.x) < 250 and abs(player_center[1] - enemy.y) < 250:
            enemy.x = random.randint(BOUNDS_X[0], BOUNDS_X[1] - 75)
            enemy.y = random.randint(BOUNDS_Y[0], BOUNDS_Y[1] - 75)


def locked_chest(openK, open_chest, closed_chest, antal_kistor, w): #kollar om kistan ska vara öppen eller stängd
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
    global ammoXposs
    global ammoYposs
    global ammo_box
    if room_counter % 10 == 0 and len(enemies) == 0 and antal_kistor == 0 and room_counter != 0:
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
                if "ak47" not in weapons_on_ground and room_counter == 20:
                    r = random.randint(1, 1)
                    if r == 1:
                        ak47Xposs = (WINDOW_SIZE[0] / 2 + 100)
                        ak47Yposs = (WINDOW_SIZE[1] / 2)
                        ak47 = Object(ak47Xposs, ak47Yposs, 32, 32, pygame.image.load("ak47.png"))
                        weapons_on_ground.append("ak47")
                if "AWP" not in weapons_on_ground and room_counter == 40:
                    r = random.randint(1, 1)
                    if r == 1:
                        AWPXposs = (WINDOW_SIZE[0] / 2 + 20)
                        AWPYposs = (WINDOW_SIZE[1] / 2 - 50)
                        AWP = Object(AWPXposs, AWPYposs, 32, 32, pygame.image.load("AWP.png"))
                        weapons_on_ground.append("AWP")
                if "Ammo" not in objects_on_ground:
                    r = random.randint(1, 1)
                    if r == 1:
                        ammoXposs = (WINDOW_SIZE[0] / 2 -100)
                        ammoYposs = (WINDOW_SIZE[1] / 2 - 50)
                        ammo_box = Object(ammoXposs, ammoYposs, 32, 32, pygame.image.load("ammo_box.png"))
                        objects_on_ground.append("ammo_box")

    if room_counter % 10 != 0 and room_counter != 0:
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
        if "ammo_box" in objects_on_ground:
            objects.remove(ammo_box)
            objects_on_ground.remove("ammo_box")
    return openK, open_chest, closed_chest, antal_kistor


def locked_door(closed, open_door, closed_door,antal_dorrar): # Kollar om dörren ska vara öppen eller stängd
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

def ak47def(): # Definerar allting kring AK47:an
    global vapen
    global shoot_cooldown
    global damage
    global weapon
    global magazin_size
    global reload_time
    global rounds_left
    global spread
    global Newb_pistol
    global Newb_pistol_flip
    global total_ammo
    spread = 0.2
    shoot_cooldown = 0.075
    damage = 1
    vapen = "ak47"
    magazin_size = 30
    reload_time = 3
    rounds_left = 30
    total_ammo = 300
    Newb_pistol = pygame.image.load("ak47.png").convert_alpha()
    Newb_pistol_flip = pygame.transform.flip(Newb_pistol, False, True)
def AWPdef(): # Definerar allting kring AWP
    global rounds_left
    global reload_time
    global vapen
    global shoot_cooldown
    global damage
    global weapon
    global magazin_size
    global spread
    global Newb_pistol
    global Newb_pistol_flip
    global total_ammo
    shoot_cooldown = 1.5
    spread = 0.01
    damage = 10
    vapen = "AWP"
    magazin_size = 10
    reload_time = 4
    rounds_left = 10
    total_ammo = 100
    Newb_pistol = pygame.image.load("AWP.png").convert_alpha()
    Newb_pistol_flip = pygame.transform.flip(Newb_pistol, False, True)
def Ammodef(): # Kollar hur mycket ammo varje vapen ska ha i magazinet från början
    global total_ammo
    if vapen == "ak47":
        total_ammo = 300
    elif vapen == "AWP":
        total_ammo = 100

def shoot(): # Skuter ett skott och håller koll på reloadtime och antal ammo
    global last_activation_time
    global current_time1
    global rounds_fired
    global magazin_size
    global reload_time
    global last_activation_time1
    global rounds_left
    global spread
    global loading_finished
    global loading_progress
    global loading_bar_width
    global total_ammo
    global reloading
    current_time = time.time()
    if rounds_left > 0 and reloading == False:
        if current_time - last_activation_time >= shoot_cooldown:
            player_center = player.get_center()
            bullet = Object(player_center[0], player_center[1], 16, 16, pygame.image.load("bullet.png"))
            target_center = target.get_center()
            i = random.uniform(-1 * spread, spread)
            r = random.uniform(-1 * spread,spread)
            bullet.velocity = [target_center[0] - player_center[0] + i*(target_center[1]-player_center[1]), target_center[1] - player_center[1] + r*(target_center[0]-player_center[0])]

            magnitude = (bullet.velocity[0] ** 2 + bullet.velocity[1] ** 2) ** 0.5

            bullet.velocity = [bullet.velocity[0] / magnitude * 10, bullet.velocity[1] / magnitude * 10]

            bullets.append(bullet)
            last_activation_time = current_time
            rounds_left -= 1
            last_activation_time1 = time.time()
    else:
        current_time1 = time.time()
        LOADING_BG = pygame.image.load("Loading Bar Background.png")
        LOADING_BG_RECT = LOADING_BG.get_rect(center=(640, 360))
        loading_bar = pygame.image.load("Loading Bar.png")
        loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))
        loading_finished = False
        loading_progress = 0
        loading_bar_width = 8
        if current_time1 - last_activation_time1 >= reload_time:
            last_activation_time1 = current_time1
            if reloading == True:
                if total_ammo >= magazin_size:
                    total_ammo -= (magazin_size-rounds_left)
                    rounds_left = magazin_size
                    reloading = False
                else:
                    rounds_left = total_ammo
                    total_ammo = 0
                    reloading = False

            elif total_ammo >= magazin_size:
                rounds_left = magazin_size
                total_ammo -= magazin_size
                reloading = False
            else:
                rounds_left = total_ammo
                total_ammo = 0
                reloading = False

            player_center = player.get_center()
            bullet = Object(player_center[0], player_center[1], 16, 16, pygame.image.load("bullet.png"))
            target_center = target.get_center()
            i = random.uniform(-1 * spread, spread)
            r = random.uniform(-1 * spread, spread)
            bullet.velocity = [target_center[0] - player_center[0] + i * (target_center[1] - player_center[1]),target_center[1] - player_center[1] + r * (target_center[0] - player_center[0])]

            magnitude = (bullet.velocity[0] ** 2 + bullet.velocity[1] ** 2) ** 0.5

            bullet.velocity = [bullet.velocity[0] / magnitude * 10, bullet.velocity[1] / magnitude * 10]

            bullets.append(bullet)
            last_activation_time = current_time
            rounds_left -= 1
            last_activation_time1 = time.time()



def check_collisions(obj1, obj2): # Kollar om två saker kolliderar
    x1, y1 = obj1.get_center()
    x2, y2 = obj2.get_center()
    w1, h1 = obj1.collider[0] / 2, obj1.collider[1] / 2
    w2, h2 = obj2.collider[0] / 2, obj2.collider[1] / 2
    if x1 + w1 > x2 - w2 and x1 - w1 < x2 + w2:
        return y1 + h1 > y2 - h2 and y1 - h1 < y2 + h2
    return False


def display_ui(): # Uppdaterar displays som t.ex antal ammo
    global antal_nycklar
    global rounds_left
    global vapen
    global total_bullets
    global infinity_display_exist
    global infinity_display
    global total_ammo
    for i in range(player.max_health):
        img = pygame.image.load("empty_heart.png" if i >= player.health else "full_heart.png")
        img = pygame.transform.scale(img, (50, 50))
        WINDOW.blit(img, (i * 50 + WINDOW_SIZE[0] / 2 - player.max_health * 25 - 300, 25))

    keys_displayed = TEXT_FONT.render(f"{antal_nycklar}", True, BLACK)
    WINDOW.blit(keys_displayed, (765, 45))

    rounds_left_displayed = TEXT_FONT.render(f"{rounds_left}", True, WHITE)
    WINDOW.blit(rounds_left_displayed, (990, 598))

    coins_displayed = TEXT_FONT.render(f"{antal_coins}", True, BLACK)
    WINDOW.blit(coins_displayed, (900, 45))

    keys_displayed = TEXT_FONT.render(f"{antal_nycklar}", True, BLACK)
    WINDOW.blit(keys_displayed, (765, 45))
    next_room = TEXT_FONT.render(f"{room_counter + 1}", True, BLACK)

    if vapen != "pistol":
        total_bullets_display = TEXT_FONT.render(f"{total_ammo}", True, BLACK)
        WINDOW.blit(total_bullets_display, (470, 597))
        infinity_display_exist = False

        if infinity_display in objects:
            objects.remove(infinity_display)

    else:
        if infinity_display_exist == False:
            infinity_display = Object(470, 597, 48, 48, pygame.image.load("infinity.png"))
            objects.insert(0, infinity_display)
            infinity_display_exist = True

    if room_counter+1 < 10:
        WINDOW.blit(next_room, (WINDOW_SIZE[0] / 2 - 9, 0))
    elif room_counter +1 < 100:
        WINDOW.blit(next_room, (WINDOW_SIZE[0] / 2 - 18, 0))


def update_screen(): # Uppdaterar skärmen
    CLOCK.tick(FRAME_RATE)
    pygame.display.update()
def playing(): # "huvud-funktionen" det är här självaste spelet skapas och allting görs.
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
    global ak47
    global AWPXposs
    global AWPYposs
    global AWP
    global ammoXposs
    global ammoYposs
    global ammo_box
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
    global pickup_object
    global antal_oppnade_kistor_denna_runda
    global player
    global target
    global KeyXposs
    global KeyYposs
    global w
    global damage
    global enemy
    global enemies
    global objects
    global vapen
    global last_activation_time1
    global last_activation_time
    global rounds_left
    global reload_time
    global magazin_size
    global prev_mouse_state
    global curr_mouse_state
    global spread
    global key_down
    global playlist_index
    global Newb_pistol
    global Newb_pistol_flip
    global WORK
    global loading_finished
    global loading_progress
    global loading_bar_width
    global total_ammo
    global infinity_display_exist
    global infinity_display
    global reloading
    global Finish_screen
    global Home_screen
    global Pause
    global Play_again
    screen.fill((0,0,0))
    pygame.display.update()
    background = pygame.transform.scale(pygame.image.load("background.png"), WINDOW_SIZE)
    player = Player(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, 55, 55, "The_man.png", 3)

    target = Object(0, 0, 40, 40, pygame.image.load("cursor.png"))

    pygame.mouse.set_visible(False)
    run = True
    while run:
        if replay:
            damage = 1
            shoot_cooldown = 0.25
            vapen = "pistol"
            antal_oppnade_kistor_denna_runda = 0
            unlock_chest = False
            pickup_weapon = False
            pickup_object = False
            reloading = False
            Finish_screen = False
            Home_screen = False
            Pause = False
            Play_again = False
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
            ammoXposs = 0
            ammoYposs = 0
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
            ammo_box = 0
            last_activation_time1 = 0
            last_activation_time = 0
            room_counter = 20
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
            rounds_left = 10
            reload_time = 3
            magazin_size = 10
            spread = 0.25
            prev_mouse_state = (False, False, False)
            key_down = 0
            playlist_index = 0
            Newb_pistol = pygame.image.load("Gon.png").convert_alpha()
            Newb_pistol_flip = pygame.transform.flip(Newb_pistol, False, True)
            WORK = 10000000
            loading_finished = False
            loading_progress = 0
            loading_bar_width = 8
            total_ammo = 99999999999999999999999999999999999
            reloading = False

            mixer.init()
            mixer.music.load(playlist[0])
            playlist_index += 1
            mixer.music.set_volume(0.2)
            mixer.music.play()
            infinity_display_exist = False
            infinity_display = 0

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
                magazine_size_display = Object(930, 590, 48, 48, pygame.image.load("magazine_size_display.png"))
                objects.insert(0, magazine_size_display)
                total_bullets_display = Object(400, 590, 48, 48, pygame.image.load("total_bullets_display.png"))
                objects.insert(0, total_bullets_display)
                d += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                antal_nycklar += 1
                objects.remove(Key)
                keys_on_screen -= 1

        if hearts_on_screen != 0:
            if HeartXposs1 != 0 and HeartYposs1 != 0:
                if player.x in range(int(HeartXposs1 - 70), int(HeartXposs1 + 70)) and player.y in range(
                        int(HeartYposs1 - 70), int(HeartYposs1 + 70)) and player.health != 5 and Heart1 in objects:
                    objects.remove(Heart1)
                    hearts_on_screen -= 1
                    player.health += 1

            if HeartXposs2 != 0 and HeartYposs2 != 0:
                if player.x in range(int(HeartXposs2 - 70), int(HeartXposs2 + 70)) and player.y in range(
                        int(HeartYposs2 - 70), int(HeartYposs2 + 70)) and player.health != 5 and Heart2 in objects:
                    objects.remove(Heart2)
                    hearts_on_screen -= 1
                    player.health += 1

            if HeartXposs3 != 0 and HeartYposs3 != 0:
                if player.x in range(int(HeartXposs3 - 70), int(HeartXposs3 + 70)) and player.y in range(
                        int(HeartYposs3 - 70), int(HeartYposs3 + 70)) and player.health != 5 and Heart3 in objects:
                    objects.remove(Heart3)
                    hearts_on_screen -= 1
                    player.health += 1

            if HeartXposs4 != 0 and HeartYposs4 != 0:
                if player.x in range(int(HeartXposs4 - 70), int(HeartXposs4 + 70)) and player.y in range(
                        int(HeartYposs4 - 70), int(HeartYposs4 + 70)) and player.health != 5 and Heart4 in objects:
                    objects.remove(Heart4)
                    hearts_on_screen -= 1
                    player.health += 1

            if HeartXposs5 != 0 and HeartYposs5 != 0:
                if player.x in range(int(HeartXposs5 - 70), int(HeartXposs5 + 70)) and player.y in range(
                        int(HeartYposs5 - 70), int(HeartYposs5 + 70)) and player.health != 5 and Heart5 in objects:
                    objects.remove(Heart5)
                    hearts_on_screen -= 1
                    player.health += 1

        if coins_on_screen != 0:
            if CoinXposs1 != 0 and CoinYposs1 != 0:
                if player.x in range(int(CoinXposs1 - 70), int(CoinXposs1 + 70)) and player.y in range(
                        int(CoinYposs1 - 70), int(CoinYposs1 + 70)) and Coin1 in objects:
                    objects.remove(Coin1)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs2 != 0 and CoinYposs2 != 0:
                if player.x in range(int(CoinXposs2 - 70), int(CoinXposs2 + 70)) and player.y in range(
                        int(CoinYposs2 - 70), int(CoinYposs2 + 70)) and Coin2 in objects:
                    objects.remove(Coin2)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs3 != 0 and CoinYposs3 != 0:
                if player.x in range(int(CoinXposs3 - 70), int(CoinXposs3 + 70)) and player.y in range(
                        int(CoinYposs3 - 70), int(CoinYposs3 + 70)) and Coin3 in objects:
                    objects.remove(Coin3)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs4 != 0 and CoinYposs4 != 0:
                if player.x in range(int(CoinXposs4 - 70), int(CoinXposs4 + 70)) and player.y in range(
                        int(CoinYposs4 - 70), int(CoinYposs4 + 70)) and Coin4 in objects:
                    objects.remove(Coin4)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs5 != 0 and CoinYposs5 != 0:
                if player.x in range(int(CoinXposs5 - 70), int(CoinXposs5 + 70)) and player.y in range(
                        int(CoinYposs5 - 70), int(CoinYposs5 + 70)) and Coin5 in objects:
                    objects.remove(Coin5)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs6 != 0 and CoinYposs6 != 0:
                if player.x in range(int(CoinXposs6 - 70), int(CoinXposs6 + 70)) and player.y in range(
                        int(CoinYposs6 - 70), int(CoinYposs6 + 70)) and Coin6 in objects:
                    objects.remove(Coin6)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs7 != 0 and CoinYposs7 != 0:
                if player.x in range(int(CoinXposs7 - 70), int(CoinXposs7 + 70)) and player.y in range(
                        int(CoinYposs7 - 70), int(CoinYposs7 + 70)) and Coin7 in objects:
                    objects.remove(Coin7)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs8 != 0 and CoinYposs8 != 0:
                if player.x in range(int(CoinXposs8 - 70), int(CoinXposs8 + 70)) and player.y in range(
                        int(CoinYposs8 - 70), int(CoinYposs8 + 70)) and Coin8 in objects:
                    objects.remove(Coin8)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs9 != 0 and CoinYposs9 != 0:
                if player.x in range(int(CoinXposs9 - 70), int(CoinXposs9 + 70)) and player.y in range(
                        int(CoinYposs9 - 70), int(CoinYposs9 + 70)) and Coin9 in objects:
                    objects.remove(Coin9)
                    coins_on_screen -= 1
                    t = random.randint(1, 3)
                    antal_coins += t

            if CoinXposs10 != 0 and CoinYposs10 != 0:
                if player.x in range(int(CoinXposs10 - 70), int(CoinXposs10 + 70)) and player.y in range(
                        int(CoinYposs10 - 70), int(CoinYposs10 + 70)) and Coin10 in objects:
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
            pickup_weapon = False
            weapons_on_ground.remove("ak47")
            ak47Xposs = 0
            ak47Yposs = 0

        if player.x in range(int(AWPXposs - 35), int(AWPXposs + 35)) and player.y in range(int(AWPYposs - 35),int(AWPYposs + 35)) and AWP in objects and pickup_weapon == True:
            objects.remove(AWP)
            AWPdef()
            pickup_weapon = False
            weapons_on_ground.remove("AWP")
            AWPXposs = 0
            AWPYposs = 0

        if player.x in range(int(ammoXposs - 35), int(ammoXposs + 35)) and player.y in range(int(ammoYposs - 35),int(ammoYposs + 35)) and ammo_box in objects and pickup_object == True:
            objects.remove(ammo_box)
            Ammodef()
            pickup_object = False
            objects_on_ground.remove("ammo_box")
            ammoXposs = 0
            ammoYposs = 0

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
            enemies = []
            objects = []
            check_input(119, False)
            check_input(97, False)
            check_input(100, False)
            check_input(115, False)

            update_screen()
            play_again()
            continue
        if room_counter == 50:
            pygame.mouse.set_visible(True)
            run = False
            enemies = []
            objects = []
            check_input(119, False)
            check_input(97, False)
            check_input(100, False)
            check_input(115, False)
            finish_screen()
        update_screen()

def play_again(): # gör en skärm till när spelaren får slut på liv dvs dör
    global Play_again
    global mpos
    global Break
    global replay
    Play_again = True
    pygame.mouse.set_visible(True)
    mpos = pygame.mouse.get_pos()
    background = pygame.transform.scale(pygame.image.load("Background.png"), (1280, 720))
    replay_image = pygame.image.load("replay_button.png").convert_alpha()
    replay_button = button(640, 200, replay_image, 7)
    quit_image = pygame.image.load("quit_button.png").convert_alpha()
    quit_button = button(640, 400, quit_image, 7)
    while True:
        update_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        WINDOW.blit(background, WINDOW_CENTER)
        replay_button.draw()
        quit_button.draw()
        if Break == True:
            Play_again = False
            replay = True
            Break = False
            playing()
            break

def pause(): # Gör en skärm om man pausar skärmen"
    global Pause
    global mpos
    global Break
    global replay
    Pause = True
    pygame.mouse.set_visible(True)
    mpos = pygame.mouse.get_pos()
    background = pygame.transform.scale(pygame.image.load("Background.png"), (1280, 720))
    resume_image = pygame.image.load("resume_button.png").convert_alpha()
    resume_button = button(640, 200, resume_image, 7)
    quit_image = pygame.image.load("quit_button.png").convert_alpha()
    quit_button = button(640, 400, quit_image, 7)
    while True:
        update_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        WINDOW.blit(background, WINDOW_CENTER)
        resume_button.draw()
        quit_button.draw()
        if Break == True:
            Pause = False
            Break = False
            pygame.mouse.set_visible(False)
            break
def home_screen(): # Gör en skärm som är en "home screen"
    global mpos
    global Home_screen
    global Break
    global replay
    Home_screen = True
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
                exit()
        WINDOW.blit(background, WINDOW_CENTER)
        start_button.draw()
        quit_button.draw()
        if Break:
            Home_screen = False
            replay = True
            Break = False
            playing()
            break

def finish_screen(): # Gör en skärm när man klarar av spelet.
    global Finish_screen
    global mpos
    global Break
    global replay
    mixer.music.pause()
    Finish_screen = True
    pygame.mouse.set_visible(True)
    mpos = pygame.mouse.get_pos()
    background = pygame.transform.scale(pygame.image.load("you_win.png"), (1280, 720))
    replay_image = pygame.image.load("replay_button.png").convert_alpha()
    replay_button = button(WINDOW_SIZE[0]/2 - 200, 550, replay_image, 7)
    quit_image = pygame.image.load("quit_button.png").convert_alpha()
    quit_button = button(WINDOW_SIZE[0]/2 + 200, 550, quit_image, 7)
    while True:
        update_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        WINDOW.blit(background, WINDOW_CENTER)
        replay_button.draw()
        quit_button.draw()
        if Break == True:
            replay = True
            Break = False
            Finish_screen = False
            playing()
            break

home_screen()


print('w', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'w',
      'w', 'x', 'x', 'x', 'p', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'w')

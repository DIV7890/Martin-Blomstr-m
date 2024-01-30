# Alla imports som krävs för spelet
import time as t
import pygame as pg
import random
import math as m
import pyautogui
import keyboard as k

# Alla variabler samlas här
Frame_Rate = 60
Run = True
Objects = []
Buttons = []
Entitys = []
Black = (0,0,0)


# initierar pygame skärmen och dess tickrate
Clock = pg.time.Clock()
screen_width, screen_height = pyautogui.size()
Window_Center = (screen_width / 2, screen_height / 2)
WINDOW_SIZE = [screen_width, screen_height]
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Error!')



def update_screen():
    Clock.tick(Frame_Rate)
    pg.display.update()


def check_for_input(key):
    if key == pg.K_ESCAPE:
        exit()

def home_screen():
    Start_Button = Button(Window_Center[0], Window_Center[1], 200, 120, pg.image.load("start_button.png").convert_alpha(), "start")
    while Run:
        update_screen()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                check_for_input(event.key)

        for b in Buttons:
            b.is_clicked()

def playing():
    screen.fill(Black)
    entity1 = Entity(Window_Center[0], Window_Center[1], 200, 120, pg.image.load("start_button.png").convert_alpha(), 1)
    while Run:
        update_screen()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                check_for_input(event.key)

        for b in Buttons:
            b.is_clicked()



class Object:

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.position = (self.x - self.width / 2, self.y - self.height / 2)
        screen.blit(pg.transform.scale(self.image, (self.width, self.height)), self.position)
        self.area = (range(int(self.position[0] - self.width), int(self.position[0] + self.width)),range(int(self.position[1] - self.height),int(self.position[1] + self.height)))

        Objects.append(self)
    def remove(self):
        Objects.remove(self)
        print("removed object")


class Button(Object): # knapp klassen är ett object i spelet men tar även argumentet "type" för att välja vilken typ av knapp det är
    def __init__(self, x, y, width, height, image, type):
        super().__init__(x, y, width, height, image)
        self.type = type

        Buttons.append(self)

    def is_clicked(self):
        if int(pg.mouse.get_pos()[0]) in self.area[0] and int(pg.mouse.get_pos()[1]) in self.area[1] and pg.mouse.get_pressed(num_buttons=3)[0]:
            if self.type == "start":
                playing()
            self.remove()
            Object.remove(self)

    def remove(self):
        Buttons.remove(self)

class Entity(Object):
    def __init__(self, x, y, width, height, image, health):
        super().__init__(x, y, width, height, image)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.health = health
        self.position = (self.x - self.width / 2, self.y - self.height / 2)
        self.area = (range(int(self.position[0] - self.width), int(self.position[0] + self.width)), range(int(self.position[1] - self.height), int(self.position[1] + self.height)))

        Entitys.append(self)

        if self.health <= 0:
            self.remove()

    def is_clicked(self):
        if int(pg.mouse.get_pos()[0]) in self.area[0] and int(pg.mouse.get_pos()[1]) in self.area[1] and pg.mouse.get_pressed(num_buttons=3)[0]:
            self.health -= 1

    def remove(self):
        Entitys.remove(self)
        Objects.remove(self)
        self.x = -1
        self.y = -1
        self.width = -1
        self.height = -1
        self.image = "transparent.png"





background = pg.transform.scale(pg.image.load("bg.jpg"), WINDOW_SIZE)
screen.blit(background, (0, 0))


home_screen()


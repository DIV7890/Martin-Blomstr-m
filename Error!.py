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
Window_Center = (0 , 0)

# initierar pygame skärmen och dess tickrate
Clock = pg.time.Clock()
screen_width, screen_height = pyautogui.size()
WINDOW_SIZE = [screen_width, screen_height]
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Error!')


def update_screen():
    Clock.tick(Frame_Rate)
    pg.display.update()


def check_for_input(key):
    if key == pg.K_ESCAPE:
        exit()



class Object:

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

background = pg.transform.scale(pg.image.load("bg.jpg"), WINDOW_SIZE)
screen.blit(background, Window_Center)
while Run:
    update_screen()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            check_for_input(event.key)



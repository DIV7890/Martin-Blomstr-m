# Alla imports som krävs för spelet
import time as t
import pygame as pg
import random
import math as m
import pyautogui

# Alla variabler samlas här
Frame_Rate = 60
Run = True

# initierar pygame skärmen och dess tickrate
Clock = pg.time.Clock()
screen_width, screen_height = pyautogui.size()
WINDOW_SIZE = [screen_width, screen_height]
screen = pg.display.set_mode((screen_width, screen_height))


def update_screen():
    Clock.tick(Frame_Rate)
    pg.display.update()
class Object:

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

Background = Object(0, 0, screen_width, screen_height, pg.image.load("bg.jpg"))

while Run:
    update_screen()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()


import pygame
import random as rd

from game.globals import *


class Ennemy():

    def __init__(self, x, y, width, height, name, win):
        self.x = x
        self.y = y

        self.win = win

        self.width = width
        self.height = height

        self.name = name
        self.speed = 2

        self.txtr = pygame.image.load(f'{PATH}/textures/{self.name}.png')
        self.txtr = pygame.transform.scale(
            self.txtr, (self.width, self.height))

        self.prev_move = rd.choice([-self.speed, self.speed])

    def show(self):
        """
        Display ennemy texture at its coordinates
        """
        try:
            self.win.blit(self.txtr, (self.x, self.y))
        except:
            pass

    def random_move(self, field):
        all_floor = field.floor + field.nx_floor
        has_moved = False

        for i in range(len(all_floor)):
            if all_floor[i][0] == self.x and (i == 0 or all_floor[i-1][1] == HEIGHT):
                self.x += self.speed
                self.prev_move = self.speed
                has_moved = True
                break
            elif all_floor[i][0] == (self.x + self.width) and (i == len(all_floor) - 1 or all_floor[i][1] == HEIGHT):
                self.x -= self.speed
                self.prev_move = -self.speed
                has_moved = True
                break

        if has_moved == False:
            self.x += self.prev_move

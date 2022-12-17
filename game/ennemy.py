from __future__ import annotations

import pygame
import random as rd
from globals import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from field import Field


class Ennemy():
    """Class for the ennemy of the field
    """

    def __init__(self, x:int, y:int, width:int, height:int, name:str, win:pygame.Surface) -> None:
        """Initialise an ennemy

        :param int x: x position of the ennemy
        :param int y: y position of the ennemy
        :param int width: width of the ennemy
        :param int height: height of the ennemy
        :param str name: name of the ennemy
        :param pygame.Surface win: windows where to display the ennemy
        """
        self.x = x
        self.y = y

        self.win = win

        self.width = width
        self.height = height

        self.speed = 2
        self.name = name

        self.txtr = pygame.image.load(f'{PATH}/textures/{self.name}.png')
        self.txtr = pygame.transform.scale(self.txtr, (self.width, self.height))

        self.prev_move = rd.choice([-self.speed, self.speed])


    def show(self) -> None:
        """
        Display ennemy texture at its coordinates
        """
        try:
            self.win.blit(self.txtr, (self.x, self.y))
        except:
            pass

    def random_move(self, field:Field, freeze:bool) -> None:
        """Make a random move

        :param Field field: The field where the ennemy evolves
        :param bool freeze: If True, the ennemy stop to move
        """
        if freeze == False:
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

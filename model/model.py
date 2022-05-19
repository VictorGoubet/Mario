
import pygame
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../game/'))
from globals import HEIGHT
from launcher import game


class Model():

    def __init__(self) -> None:
        self.time_until_next_jump = 0

    def key_function(self, state):
        """
        Return action given a state
        """
        mario, field = state

        keys = {k:False for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]}


        min_x = 9999
        for x, y in field.floor + field.nx_floor:
            dist =  x - (mario.x + mario.width) 
            if y == HEIGHT and min_x > dist >= 0:
                min_x = dist

        if self.time_until_next_jump == 0:
            if min_x < 25:
                keys[pygame.K_UP] = True
                self.time_until_next_jump = 2
            
            keys[pygame.K_RIGHT] = True
        else:
            self.time_until_next_jump -= 1


        return keys


model = Model()

game(model.key_function)
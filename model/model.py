
import pygame
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from game.globals import HEIGHT
from game.__main__ import Game


class Model():

    def __init__(self) -> None:
        self.time_until_next_jump = 0

    def key_function(self, state):
        """
        Return action given a state
        """

        keys = {k:False for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]}


        min_x = 9999
        for x, y in state.field.floor + state.field.nx_floor:
            dist =  x - (state.mario.x + state.mario.width) 
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

mario_game = Game()
model = Model()
mario_game.launch(model.key_function)

import pygame
import sys, os
import random as rd

sys.path.append(os.path.join(os.path.dirname(__file__), '../game/'))
from launcher import game



def key_function(state):
    """
    Return action given a state
    """
    mario, field = state

    keys = {k:False for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]}

    n_key = rd.randint(0, len(keys))
    actions = rd.choices(list(keys.keys()), k=n_key)

    for a in actions:
        keys[a] = True
    return keys


game(key_function)
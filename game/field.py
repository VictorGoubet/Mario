from __future__ import annotations

import typing
import pygame
import random as rd

from globals import *
from ennemy import Ennemy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mario import Mario

class Field():
    """
    Class defining the field
    """

    def __init__(self, h_floor:int, x_off:int, speed:int, win:pygame.Surface) -> None:
        """Initialise the field object

        :param int h_floor: The height of the floor
        :param int x_off: The minimal distance to mario to start sliding the field
        :param int speed: The speed of the sliding
        :param pygame.Surface win: The windows where to display the field
        """
        self.win = win
        self.s_coin = 25 # number or coins per chunk
        self.speed = speed
        self.x_off = x_off
        self.h_floor = h_floor

        # load textures
        self.sky_txtr = pygame.image.load(f'{PATH}/textures/sky.png')
        self.coin_txtr = pygame.image.load(f'{PATH}/textures/coin.png')
        self.coin_txtr = pygame.transform.scale(self.coin_txtr, (self.s_coin, self.s_coin))
        self.floor_txtr = pygame.image.load(f'{PATH}/textures/floor.png')
        self.clock_txtr = pygame.image.load(f'{PATH}/textures/clock.png')
        self.flag_txtr = pygame.image.load(f'{PATH}/textures/flag.png')
        self.flag_txtr = pygame.transform.scale(self.flag_txtr, (110, 250))

        # prepare the current floor and the next one (next chunk)
        self.nx_floor = self.create_floor()
        self.floor = self.create_floor(next=False)

        # prepare the current coins and the next one
        self.nx_coins = self.generate_coins()
        self.coins = self.generate_coins(next=False)

        # prepare the current ennemies and the next one
        self.nx_ennemies = self.generate_ennemies()
        self.ennemies = self.generate_ennemies(next=False)

        self.n_block = 1
        self.x_flag = None # coordinates of the flag

    def create_floor(self, next:bool=True) -> typing.List[typing.Tuple[int, int]]:
        """Generate an array or coordinates. Each coordinates represent the position of
           a block in the current floor

        :param bool next: If true, the generated floor is the floor which will
                          be displayed at the next complete sliding, defaults to True
        :return typing.List[typing.Tuple[int, int]]: The list of x and y coordinates
        """
        floor = []
        for k in range(WIDTH//self.h_floor):
            x = k * self.h_floor
            x += WIDTH if next else 0
            # generate random holes
            y = HEIGHT if len(floor) > 0 and floor[-1][1] != HEIGHT and rd.randint(0, 1) else HEIGHT - self.h_floor
            floor.append([x, y])
        return floor

    def generate_ennemies(self, next:bool=True) -> typing.List[Ennemy]:
        """Generate some ennemies

        :param bool next: If True, the generated ennemies will belong
                          to the next floor, defaults to True
        :return typing.List[Ennemy]: The list of ennemies
        """
        ennemies = []
        width, height = 30, 30
        y0 = HEIGHT - H_FLOOR - height
        floor = self.nx_floor if next else self.floor

        # detect the first plateform until first hole
        frst_plateform = []
        for i, (x, y) in enumerate(self.floor):
            if y == HEIGHT:
                break
            frst_plateform.append(i)

        for i, (x, y) in enumerate(floor):
            # do not put ennemy on the first plateform and in holes
            if rd.randrange(0, 2) == 1 and not (floor == self.floor and i in frst_plateform) and y != HEIGHT:
                e = Ennemy(x, y0, width, height, 'goomba', self.win)
                ennemies.append(e)
        return ennemies

    def generate_coins(self, next:bool=True) -> typing.List[typing.Tuple[int, int]]:
        """Generate the random coordinates of coins

        :param bool next: If True, the generated coins will belong
                          to the next floor, defaults to True
        :return typing.List[typing.Tuple[int, int]]: The list of coins
        """
        coins = []
        y0 = HEIGHT - H_FLOOR - H_MARIO
        for _ in range(rd.randint(1, 4)):
            n = rd.randint(1, 5)
            x = rd.randint(0, WIDTH - (n + 1) * self.s_coin)
            x += WIDTH if next else 0
            y = rd.choice([y0 - H_JUMP + 10, y0 - 10])
            coins += [[x + k * self.s_coin, y] for k in range(n)]
        return coins


    def show(self, mario:Mario) -> None:
        """Show all the field and all the belonging entities

        :param Mario mario: Mario player evolving on the current field
        """

        self.move_field(mario)

        self.win.blit(self.sky_txtr, (0, 0))
        self.win.blit(self.clock_txtr, (WIDTH - 60, 8))
        self.win.blit(self.coin_txtr, (WIDTH - 160, 2))

        for e in self.ennemies + self.nx_ennemies:
            e.show()

        self.show_entities(self.coins, self.nx_coins, self.coin_txtr)
        self.show_entities(self.floor, self.nx_floor, self.floor_txtr)

        if self.n_block + 1 >= N_END:
            floor = self.nx_floor if self.n_block + 1 == N_END else self.floor
            self.x_flag = [x for x, y in floor if y != HEIGHT][-1]
            self. win.blit(self.flag_txtr, (self.x_flag, HEIGHT - H_FLOOR - 245))


    def show_entities(self, ent:typing.List[typing.Tuple[int, int]], 
                            nx_ent:typing.List[typing.Tuple[int, int]], 
                            txtr:pygame.Surface) -> None:
        """Show all the entities with the given texture

        :param typing.List[typing.Tuple[int, int]] ent: The coordinates of all the entities to display
        :param typing.List[typing.Tuple[int, int]] nx_ent: The coordinates of all the entities for the next floor
        :param pygame.Surface txtr: The texture to use for these entities
        """
        for x, y in ent:
            self.win.blit(txtr, (x, y))
        for x_n, y_n in nx_ent:
            self.win.blit(txtr, (x_n, y_n))


    def move_ennemies(self, freeze:bool) -> None:
        """Move all (crt and next) the ennemies (random moves)

        :param bool freeze: If True, all the ennemies will stop moving
        """
        for e in self.ennemies + self.nx_ennemies:
            e.random_move(self, freeze)


    def move_field(self, mario:Mario) -> None:
        """Slide the field and the coins when mario moves

        :param Mario mario: The mario player
        """

        # move the field
        if mario.x > self.x_off:
            self.floor = [[x-self.speed, y] for x, y in self.floor]
            self.nx_floor = [[x-self.speed, y] for x, y in self.nx_floor]

            self.coins = [[x-self.speed, y] for x, y in self.coins]
            self.nx_coins = [[x-self.speed, y] for x, y in self.nx_coins]

            for e in self.ennemies + self.nx_ennemies:
                e.x -= self.speed

            mario.x -= self.speed

        # if we reached the end of current floor:
        # set current floor as next floor and generate a new next floor
        if self.nx_floor[0][0] == 0:
            self.floor = self.nx_floor
            self.coins = self.nx_coins
            self.ennemies = self.nx_ennemies

            self.nx_floor = self.create_floor()
            self.nx_coins = self.generate_coins()
            self.nx_ennemies = self.generate_ennemies()

            self.n_block += 1

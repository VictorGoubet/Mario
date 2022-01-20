import pygame
import random as rd
from globals import *

class Field():

    def __init__(self, h_floor, x_off, speed):
        self.h_floor = h_floor
        self.x_off = x_off
        self.speed = speed
        self.s_coin = 25

        self.floor = self.create_floor(False)
        self.nx_floor = self.create_floor()

        self.coins = self.generate_coins(False)
        self.nx_coins = self.generate_coins()
        self.n_block = 1

        self.x_flag = None
        

        # texture
        self.sky_txtr = pygame.image.load(r'./texture/sky.png')
        self.coin_txtr = pygame.image.load(r'./texture/coin.png')
        self.coin_txtr = pygame.transform.scale(self.coin_txtr, (self.s_coin, self.s_coin))
        self.floor_txtr = pygame.image.load(r'./texture/floor.png')
        self.clock_txtr = pygame.image.load(r'./texture/clock.png')
        self.flag_txtr = pygame.image.load(r'./texture/flag.png')
        self.flag_txtr = pygame.transform.scale(self.flag_txtr, (110, 250))
    
    def create_floor(self, next=True):
        floor = []
        for k in range(WIDTH//self.h_floor):
            x = k * self.h_floor
            x += WIDTH if next else 0
            if len(floor) > 0 and floor[-1][1] != HEIGHT and rd.randint(0, 1):
                y = HEIGHT 
            else:
                y = HEIGHT - self.h_floor
            floor.append([x, y])
        return floor


    
    def generate_coins(self, next=True):
        coins = []
        y0 = HEIGHT-H_FLOOR-H_MARIO
        for _ in range(rd.randint(1, 4)):
            n = rd.randint(1, 5)
            x = rd.randint(0, WIDTH-(n+1)*self.s_coin)
            x += WIDTH if next else 0
            y = rd.choice([y0-H_JUMP+10, y0-10])
            coins += [[x+k*self.s_coin, y] for k in range(n)]
        return coins


    
    def show(self, mario):
        
        self.move_field(mario)

        win.blit(self.sky_txtr, (0, 0))
        win.blit(self.clock_txtr, (WIDTH-60, 8))
        win.blit(self.coin_txtr, (WIDTH-160, 2))
        self.show_entities(self.coins, self.nx_coins, self.coin_txtr)
        self.show_entities(self.floor, self.nx_floor, self.floor_txtr)

        if self.n_block+1>= N_END:
            floor = self.nx_floor if self.n_block+1==N_END else self.floor
            self.x_flag = [x for x, y in floor if y != HEIGHT][-1]
            win.blit(self.flag_txtr, (self.x_flag, HEIGHT-H_FLOOR-245))



    def show_entities(self, ent, nx_ent, txtr):
        for x, y in ent:
            win.blit(txtr, (x, y))
        for x_n, y_n in nx_ent:
            win.blit(txtr, (x_n, y_n))


    
    def move_field(self, mario):

        if mario.x > self.x_off:
            self.floor = [[x-self.speed, y] for x, y in self.floor]
            self.nx_floor = [[x-self.speed, y] for x, y in self.nx_floor]

            self.coins = [[x-self.speed, y] for x, y in self.coins]
            self.nx_coins = [[x-self.speed, y] for x, y in self.nx_coins]

            mario.x -= self.speed
        
        if self.nx_floor[0][0] == 0:
            self.floor = self.nx_floor
            self.coins = self.nx_coins
            
            self.nx_coins = self.generate_coins()
            self.nx_floor = self.create_floor()

            self.n_block += 1
            
        
    

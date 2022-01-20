import time
import pygame

from globals import *


class Mario():

    def __init__(self, height, width, x, y, h_jump):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.orientation = 'R'
        self.txtr = [self.import_txtr('mario1'),
                     self.import_txtr('mario2')]
        self.k_anim = 0
        self.score = 0
        self.h_jump = h_jump
        self.y0 = HEIGHT-H_FLOOR-self.height
        self.finish = False
        self.freeze = False
    
    def show(self):
        try:
            win.blit(self.txtr[self.k_anim], (self.x, self.y))
        except:
            pass

    def import_txtr(self, name):
        txtr = pygame.image.load(f'./texture/{name}.png')
        txtr = pygame.transform.scale(txtr, (self.width, self.height))
        return txtr

    def update_orientation(self, dir):
        if self.orientation != dir:
            self.orientation = dir
            self.txtr = [pygame.transform.flip(x, True, False) for x in self.txtr]

    
    def launch_jump(self):
        decrease = False
        while self.y-1 < self.y0:
            if self.y > self.y0 - self.h_jump and not decrease:
                self.y -= 1
            else:
                self.y += 1
                decrease = True
            v = self.y0 - self.y 
            time.sleep((v+1)/(20*1000))
        self.y = self.y0
    
    def fall(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('./song/gameover.mp3'))
        self.freeze = True
        while self.y < HEIGHT:
            self.y += 1
            time.sleep(1/1000)
        time.sleep(3)
        self.finish = True
    
    def move(self, keys, field):
        if not self.freeze:
            if keys[pygame.K_LEFT]:
                self.x -= 10 if self.x>=10 else 0
                self.update_orientation('L')
                self.k_anim = 0 if self.k_anim == 1 else 1

            elif keys[pygame.K_RIGHT]:
                self.x += 10
                self.update_orientation('R')
                self.k_anim = 0 if self.k_anim == 1 else 1
            else:
                self.k_anim = 0

            if keys[pygame.K_UP] and self.y == self.y0:
                self.launch_jump()   
            
            self.check_holes(field)
            self.check_coins(field)
            self.check_flag(field)
        time.sleep(1)

    def check_flag(self, field):
        if field.x_flag and self.x - 10 > field.x_flag:
            self.freeze = True
            self.x = field.x_flag
            self.y = HEIGHT-H_FLOOR-240
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('./song/success.mp3'))
            time.sleep(3)
            self.finish = True

    def check_holes(self, field):
        for x, y in field.floor + field.nx_floor:
            pos_x = x < self.x and (self.x + self.width) < x + field.h_floor
            if pos_x and y == HEIGHT and self.y == self.y0:
                self.fall()
    
    def check_collision(self, pos, size):
        x, y = pos
        h, w = size
        cdt_y1 = y <= self.y <= y + h
        cdt_y2 = y <= self.y + self.height <= y + h
        cdt_y3 = self.y <= y and self.y + self.height >= y + h

        cdt_x1 = x <= self.x <= x + w
        cdt_x2 = x <= self.x + self.width <= x + w
        cdt_x3 = self.x <= x and self.x + self.width >= x + w

        if (cdt_y1 or cdt_y2 or cdt_y3) and (cdt_x1 or cdt_x2 or cdt_x3):
            return True
    
    def play_sound(self, name, vol):
        global crt_chnl
        sound = pygame.mixer.Sound(f'./song/{name}.mp3')
        sound.set_volume(vol)
        pygame.mixer.Channel(crt_chnl).play(sound)
        
        crt_chnl = 1 if crt_chnl==19 else crt_chnl + 1
    
    def check_coins(self, field):
        try:
            for x, y in field.coins + field.nx_coins:
                if self.check_collision((x , y), (field.s_coin, field.s_coin)):
                    a, b = [x, y] in field.coins, [x, y] in field.nx_coins
                    if a or b:
                        if a:
                            field.coins.remove([x, y])
                        else:
                            field.nx_coins.remove([x, y])
                        self.score += 1
                        self.play_sound('coin_sound', 0.02)            
        except:
            pass
                

        
        
        



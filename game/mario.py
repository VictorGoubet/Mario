import time
import pygame
from game.globals import *


class Mario():
    """
    Class of the player
    """

    def __init__(self, height, width, x, y, h_jump, win):

        # mario size
        self.height = height
        self.width = width

        self.win = win

        # mario position
        self.x = x
        self.y = y
        self.orientation = 'R'

        self.speed = 10

        # load textures
        self.txtr = [self.import_txtr('mario1'),
                     self.import_txtr('mario2')]

        self.k_anim = 0
        self.score = 0
        self.h_jump = h_jump
        self.y0 = HEIGHT - H_FLOOR - self.height
        self.finish = False
        self.freeze = False

    def show(self):
        """
        Display mario texture at its coordinates
        """
        try:
            self.win.blit(self.txtr[self.k_anim], (self.x, self.y))
        except:
            pass

    def import_txtr(self, name):
        """
        Import texture
        """
        txtr = pygame.image.load(f'{PATH}/textures/{name}.png')
        txtr = pygame.transform.scale(txtr, (self.width, self.height))
        return txtr

    def update_orientation(self, dir):
        """
        Return the texture corresponding to mario's orientation
        """
        if self.orientation != dir:
            self.orientation = dir
            self.txtr = [pygame.transform.flip(
                x, True, False) for x in self.txtr]

    def launch_jump(self, h_jump):
        """
        Launch the jump movement following approximative 
        physics laws (really approximative)
        """
        reach = False
        y_jump = self.y - h_jump
        self.y = self.y - 1
        while self.y < self.y0:

            if self.y == y_jump:
                reach = True

            if reach:
                self.y += 1
            else:
                self.y -= 1

            v = self.y0 - self.y
            time.sleep((v+1)/(20*1000))

    def fall(self):
        """
        Launch the huge fall when mario is in a hole
        """
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound(f'{PATH}/songs/gameover.mp3'))
        self.freeze = True
        while self.y < HEIGHT:
            self.y += 1
            time.sleep(1/1000)
        time.sleep(3)
        self.finish = True

    def move(self, keys, field):
        """
        Map each keyboard key to a mario's movement
        """
        if not self.freeze:
            if keys[pygame.K_LEFT]:
                self.x -= self.speed if self.x >= self.speed else 0
                self.update_orientation('L')
                self.k_anim = 0 if self.k_anim == 1 else 1

            elif keys[pygame.K_RIGHT]:
                self.x += self.speed
                self.update_orientation('R')
                self.k_anim = 0 if self.k_anim == 1 else 1
            else:
                self.k_anim = 0

            if keys[pygame.K_UP] and self.y == self.y0:
                self.launch_jump(self.h_jump)

            # after moving, check the situation
            self.check_all(field)

        time.sleep(1)

    def check_all(self, field):
        """
        Check mario situation
        """
        self.check_holes(field)
        self.check_ennemies(field)
        self.check_coins(field)
        self.check_flag(field)

    def check_flag(self, field):
        """
        Check if mario is on the flag
        """
        if field.x_flag and self.x - 10 > field.x_flag:
            self.freeze = True
            self.x = field.x_flag
            self.y = HEIGHT - H_FLOOR - 240
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound(f'{PATH}/songs/success.mp3'))
            time.sleep(3)
            self.finish = True

    def check_ennemies(self, field):
        """
        Check if mario is colliding with an ennemy
        """
        if self.freeze == False:
            for e in field.ennemies + field.nx_ennemies:
                if self.colision_x(e.x, e.width, self.x, self.width) or \
                self.colision_x(self.x, self.width, e.x, e.width):
                    if e.y + 10 >= (self.y + self.height) >= e.y - 5:
                        try:
                            field.ennemies.remove(e)
                        except:
                            field.nx_ennemies.remove(e)
                        self.score += 10
                        self.play_sound('crush', 0.2)

                    elif (self.y + self.height) > e.y and not self.freeze:
                        pygame.mixer.Channel(0).play(
                            pygame.mixer.Sound(f'{PATH}/songs/gameover.mp3'))
                        self.freeze = True
                        time.sleep(3)
                        self.finish = True

    def check_holes(self, field):
        """
        Check if mario is in a hole
        """
        for x, y in field.floor + field.nx_floor:
            pos_x = x < self.x and (self.x + self.width) < x + field.h_floor
            if pos_x and y == HEIGHT and self.y == self.y0:
                self.fall()

    def colision_x(self, x1, w1, x2, w2):
        """
        check colision on x axis
        """
        cdt_x1 = x2 <= x1 <= x2 + w2
        cdt_x2 = x2 <= x1 + w1 <= x2 + w2
        cdt_x3 = x1 <= x2 and x1 + w1 >= x2 + w2
        cdt_x3 = x1 >= x2 and x1 + w1 <= x2 + w2
        return (cdt_x1 or cdt_x2 or cdt_x3)

    def colision_y(self, y1, h1, y2, h2):
        """
        check colision on y axis
        """
        cdt_y1 = y2 <= y1 <= y2 + h2
        cdt_y2 = y2 <= y1 + h1 <= y2 + h2
        cdt_y3 = y1 <= y2 and y1 + h1 >= y2 + h2
        cdt_y3 = y1 >= y2 and y1 + h1 <= y2 + h2
        return (cdt_y1 or cdt_y2 or cdt_y3)

    def check_collision(self, pos, size):
        """
        Check if mario is colliding with the field (in the hole for example)
        """
        x, y = pos
        h, w = size

        cd1_x = self.colision_x(self.x, self.width, x, w)
        cd1_y = self.colision_y(self.y, self.height, y, h)

        cd2_x = self.colision_x(x, w, self.x, self.width)
        cd2_y = self.colision_y(y, h, self.y, self.height)
        if (cd1_x or cd2_x) and (cd1_y or cd2_y):
            return True

    def check_coins(self, field):
        """
        Check if Mario is on a coin
        """
        try:
            for x, y in field.coins + field.nx_coins:
                if self.check_collision((x, y), (field.s_coin, field.s_coin)):
                    try:
                        field.coins.remove([x, y])
                    except:
                        field.nx_coins.remove([x, y])
                    self.score += 1
                    self.play_sound('coin_sound', 0.02)
        except:
            pass

    def play_sound(self, name, vol):
        """
        Launch a provided sound
        """
        global CRT_CHNL
        sound = pygame.mixer.Sound(f'{PATH}/songs/{name}.mp3')
        sound.set_volume(vol)
        pygame.mixer.Channel(CRT_CHNL).play(sound)

        CRT_CHNL = 1 if CRT_CHNL == 19 else CRT_CHNL + 1

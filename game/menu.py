import time
import pygame

from game.globals import *


class Menu():
    """
    Class of the menu panel
    """

    def __init__(self, win):

        self.win = win
        # load textures
        self.menu_txtr = pygame.image.load(f'{PATH}/textures/menu.jpg')
        self.play_txtr = pygame.image.load(f'{PATH}/textures/btn_play.jpg')
        self.quit_txtr = pygame.image.load(f'{PATH}/textures/btn_quit.jpg')

        # define the position of the buttons
        self.btn_w = 200
        self.btn_h = 66
        self.pos_btn_play = (WIDTH//2-50 - self.btn_w, HEIGHT-15 - self.btn_h)
        self.pos_btn_quit = (WIDTH//2+50, HEIGHT-15-self.btn_h)

        self.display = True
        self.run = True
        self.click = False
        self.msc = False

    def show(self):
        """
        show the different buttons of the menu
        """
        self.win.blit(self.menu_txtr, (0, 0))
        self.win.blit(self.play_txtr, self.pos_btn_play)
        self.win.blit(self.quit_txtr, self.pos_btn_quit)

    def update(self):
        """
        Mapp the differents button click to there actions
        """
        if not self.msc:
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound(f'{PATH}/songs/menu_song.mp3'))
            self.msc = True

        if self.is_focus(self.pos_btn_play, (self.btn_w, self.btn_h)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.click:
                self.display = False
                self.click = False
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound(f'{PATH}/songs/main_theme.mp3'))
                self.msc = False

        elif self.is_focus(self.pos_btn_quit, (self.btn_w, self.btn_h)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.click:
                self.run = False
                self.click = False
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return time.time()

    def is_focus(self, pos, size):
        """
        Handle the mouse focus on the buttons
        """
        x, y = pos
        w, h = size
        x_m, y_m = pygame.mouse.get_pos()
        if x < x_m < x + w and y < y_m < y+h:
            return True

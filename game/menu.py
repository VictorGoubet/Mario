import time
import typing
import pygame

from globals import *


class Menu():
    """
    Class of the menu panel
    """

    def __init__(self, win:pygame.Surface) -> None:
        """Initialise the menu

        :param pygame.Surface win: The winodws of the game
        """

        self.win = win

        # load textures
        self.menu_txtr = pygame.image.load(f'{PATH}/textures/menu.jpg')
        self.play_txtr = pygame.image.load(f'{PATH}/textures/btn_play.jpg')
        self.quit_txtr = pygame.image.load(f'{PATH}/textures/btn_quit.jpg')

        # define the position of the buttons
        self.btn_h = 66
        self.btn_w = 200
        self.pos_btn_play = (WIDTH // 2 - 50 - self.btn_w, HEIGHT - 15 - self.btn_h)
        self.pos_btn_quit = (WIDTH // 2 + 50, HEIGHT - 15 - self.btn_h)

        self.run = True
        self.msc = False
        self.click = False
        self.display = True


    def show(self) -> None:
        """
        Show the different buttons of the menu
        """
        self.win.blit(self.menu_txtr, (0, 0))
        self.win.blit(self.play_txtr, self.pos_btn_play)
        self.win.blit(self.quit_txtr, self.pos_btn_quit)


    def update(self) -> float:
        """
        Map the different button click to there actions
        :return float: The current time
        """

        if not self.msc:
            # Restart the music when finished
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(f'{PATH}/songs/menu_song.mp3'))
            self.msc = True

        # Handle click on the Play button
        if self.is_focus(self.pos_btn_play, (self.btn_w, self.btn_h)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.click:
                self.display = False
                self.click = False
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(f'{PATH}/songs/main_theme.mp3'))
                self.msc = False

        # Handle click of Quit button
        elif self.is_focus(self.pos_btn_quit, (self.btn_w, self.btn_h)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.click:
                self.run = False
                self.click = False
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return time.time()


    def is_focus(self, pos:typing.Tuple[int, int], size:typing.Tuple[int, int]) -> bool:
        """Check if the mouse is on a given button

        :param typing.Tuple[int, int] pos: The x and y position of the button
        :param typing.Tuple[int, int] size: The h and w size of the button
        :return bool: True if the mouse is on the button, else False
        """
        (x, y), (w, h) = pos, size
        x_m, y_m = pygame.mouse.get_pos()
        return x < x_m < x + w and y < y_m < y+h
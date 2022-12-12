import time
import pygame

from game.globals import *
from game.menu import Menu
from game.mario import Mario
from game.field import Field
from game.thread import myThread


class Game():

    def __init__(self, key_function=None):

        # Init pygame
        pygame.init()

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 13)
        self.mode = 'train' if self.key_function else 'game'
        self.key_function = key_function

        pygame.mixer.init()
        pygame.mixer.set_num_channels(20)
        pygame.display.set_caption('Mario')

        # Init entities
        self.menu = Menu(self.win)
        self.mario = Mario(H_MARIO, WIDTH_MARIO, 0, HEIGHT -
                           H_FLOOR - H_MARIO, H_JUMP, self.win)
        self.field = Field(H_FLOOR, WIDTH - 400, 10, self.win)

    def launch(self):
        """
        Launch the game
        """
        self.mainloop(self.key_function)
        pygame.quit()

    def get_pixel_screen(self):
        """
        Return the screen as a pixel array
        """
        return pygame.Surface.get_buffer(self.win).raw

    
    def training_box(self):
        """
        Special mode for training
        """

    def mainloop(self):
        """
        main loop of the game
        """
        while self.menu.run:
            self.clock.tick(FPS)

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.menu.run = False
                if e.type == pygame.MOUSEBUTTONUP:
                    self.menu.click = True

            if self.menu.display:
                self.menu.show()
                t0 = self.menu.update()
            else:
                # manage physics
                keys = pygame.key.get_pressed()
                moves_thread = myThread(
                    "moves", lambda: self.mario.move(keys, self.field))
                moves_thread.start()
                self.field.move_ennemies(self.mario.freeze)

                # display the field and mario
                self.field.show(self.mario)
                self.mario.show()

                if self.mario.finish:
                    self.menu.display = True

                # compute score
                score = self.font.render(
                    f'{self.mario.score}', True, (255, 255, 255))
                t1 = time.time() - t0
                t = self.font.render(f'{int(t1)}', True, (255, 255, 255))
                score_by_t = self.font.render(
                    f'Coins/sc: {round(self.mario.score/t1, 2)}sc', True, (255, 255, 255))

                # show score
                self.win.blit(score, (WIDTH - 130, 10))
                self.win.blit(t, (WIDTH - 40, 10))
                self.win.blit(score_by_t, (10, 10))

            pygame.display.update()


if __name__ == '__main__':
    mario_game = Game()
    mario_game.launch()

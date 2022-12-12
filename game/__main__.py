import time
import pygame

from game.globals import *
from game.menu import Menu
from game.mario import Mario
from game.field import Field
from game.thread import myThread
from model.DeepQ import DeepQ



class Game():

    def __init__(self, animate = True):

        self.animate = animate
        # Init pygame
        pygame.init()

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 13)
        self.mode = 'train' if self.key_function else 'game'
        pygame.mixer.init()
        pygame.mixer.set_num_channels(20)
        pygame.display.set_caption('Mario')

        # Init entities
        self.menu = Menu(self.win)
        self.mario = Mario(H_MARIO, WIDTH_MARIO, 0, HEIGHT -
                           H_FLOOR - H_MARIO, H_JUMP, self.win, animate = animate)
        self.field = Field(H_FLOOR, WIDTH - 400, 10, self.win)

        self.mapped_moves = {
            0 : [pygame.K_LEFT],
            1 : [pygame.K_RIGHT],
            2 : [pygame.K_UP],
            3 : [pygame.K_LEFT, pygame.K_UP],
            4 : [pygame.K_RIGHT, pygame.K_UP],
            5 : []
        }

    def launch(self):
        """
        Launch the game
        """
        self.mainloop()
        pygame.quit()


    def step(self, action):
        self.clock.tick(FPS)
        _ = pygame.event.get()
        score0 = self.mario.score

        action = self.mapped_moves[action]
        action = {k: True if k in action else False for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]}

        moves_thread = myThread(
                    "moves", lambda: self.mario.move(action, self.field))
               
        moves_thread.start()

        self.show_env()
        
        screen = pygame.surfarray.array3d(self.win) / 255

        reward = self.mario.score - score0

        pygame.display.update()


        return screen, reward, self.mario.finish

    def show_env(self):
        self.field.move_ennemies(self.mario.freeze)
        # display the field and mario
        self.field.show(self.mario)
        self.mario.show()

    def reset(self):

        self.mario = Mario(H_MARIO, WIDTH_MARIO, 0, HEIGHT -
                           H_FLOOR - H_MARIO, H_JUMP, self.win,  animate = self.animate)
        self.field = Field(H_FLOOR, WIDTH - 400, 10, self.win)

        
        self.show_env()
        pygame.display.update()



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
    env = Game(animate = False)
    model = DeepQ( 1, 0.4, env, 32)
    model.train(10)
    '''#mario_game.launch()
    n = 0
    while not mario_game.mario.finish:
        mario_game.step(1)
        if mario_game.mario.finish and n < 3:
            mario_game.reset()
            n+=1'''



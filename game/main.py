import time
import pygame

from globals import *
from menu import Menu
from thread import myThread


def game():
    """
    Launch the entire game
    """
    menu = Menu()
    
    while menu.run:
        clock.tick(FPS)
        
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                menu.run = False
            if e.type == pygame.MOUSEBUTTONUP:
                menu.click = True

        if menu.display:
            menu.show()
            mario, field, t0 = menu.update()
        else:
            # manage physics
            keys = pygame.key.get_pressed() 
            moves_thread = myThread("moves", lambda:mario.move(keys, field))
            moves_thread.start()
            
            # display the field and mario
            field.show(mario)
            mario.show()

            if mario.finish:
                menu.display = True

            # compute score
            score = font.render(f'{mario.score}', True, (255, 255, 255))
            t1 = time.time()-t0
            t = font.render(f'{int(t1)}', True, (255, 255, 255))
            score_by_t = font.render(f'Coins/sc: {round(mario.score/t1, 2)}sc', True, (255, 255, 255))

            # show score
            win.blit(score, (WIDTH-130, 10))
            win.blit(t, (WIDTH-40, 10))
            win.blit(score_by_t, (10, 10))
        
        pygame.display.update()
    


    


if __name__ == '__main__':
    game()
    pygame.quit()




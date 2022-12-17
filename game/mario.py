import time
import typing
import pygame
from globals import *
from field import Field


class Mario():
    """
    Class of the player
    """

    def __init__(self, height:int, width:int, x:int, y:int, h_jump:int, win:pygame.Surface) -> None:
        """Initialise the characther

        :param int height: The height of mario
        :param int width: The width of mario
        :param int x: The x position of mario
        :param int y: The y position of mario
        :param int h_jump: The height of the mario's jump
        :param pygame.Surface win: The windows where to display mario
        """
        
        self.win = win
        

        # mario's characteristics
        self.speed = 10
        self.width = width
        self.height = height
        self.h_jump = h_jump
        self.x, self.y = x, y
        self.x_start, self.y_start = x, y 

        self.reset()

        # global characteristics
        self.y0 = HEIGHT - H_FLOOR - self.height # ground level
        
        # load textures
        self.txtr = [self.import_txtr('mario1'),
                     self.import_txtr('mario2')]


    def reset(self) -> None:
        """Reset mario for a new game
        """
        self.score = 0
        self.k_anim = 0
        self.finish = False
        self.freeze = False
        self.orientation = 'R'
        self.x, self.y = self.x_start, self.y_start


    def show(self) -> None:
        """
        Display mario texture at its coordinates
        """
        try:
            self.win.blit(self.txtr[self.k_anim], (self.x, self.y))
        except:
            pass


    def import_txtr(self, name:str) -> pygame.Surface:
        """Import a texture

        :param str name: The name of the texture to import
        :return pygame.Surface: The loaded texture
        """
        txtr = pygame.image.load(f'{PATH}/textures/{name}.png')
        txtr = pygame.transform.scale(txtr, (self.width, self.height))
        return txtr


    def update_orientation(self, dir:str) -> None:
        """Set the mario's orientation to the given one

        :param str dir: The new orientation: `['R' |'L']`
        """
        if self.orientation != dir:
            self.orientation = dir
            self.txtr = [pygame.transform.flip(x, True, False) for x in self.txtr]

    def launch_jump(self) -> None:
        """
        Launch the jump movement following approximative 
        physics laws (really approximative)
        * Note: This function is executed in a thread inorder
                to be able to continue to change orientation in the air
        """

        reach = False
        y_jump = self.y - self.h_jump
        self.y = self.y - 1
        while self.y < self.y0:
            if self.y == y_jump:
                reach = True
            if reach:
                self.y += 1
            else:
                self.y -= 1
            v = self.y0 - self.y
            time.sleep((v + 1) / (20 * 1000))

    def fall(self) -> None:
        """
        Launch the huge fall when mario is in a hole and
        set the game as finished
        """
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(f'{PATH}/songs/gameover.mp3'))
        self.freeze = True
        while self.y < HEIGHT:
            self.y += 1
            time.sleep(1 / 1000)
        time.sleep(3.5)
        self.finish = True


    def move(self, keys:typing.List[bool], field:Field) -> None:
        """Map each keyboard keys to mario's actions

        :param typing.List[bool] keys: The pressed status of each arrow key
        :param Field field: The field object on which mario evolves
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
                self.launch_jump()

            # after moving, check the situation
            self.check_all(field)

        time.sleep(1)


    def check_all(self, field:Field) -> None:
        """Check all stuff which could lead to
           the end of the game

        :param Field field: The field on which mario evolves
        """
        # Check loose
        self.check_holes(field)
        self.check_ennemies(field)
        self.check_coins(field)

        # Check win
        self.check_flag(field)



    def check_flag(self, field:Field) -> None:
        """Check if mario is on the flag

        :param Field field: The field on which mario evolves
        """
        if field.x_flag and self.x - 10 > field.x_flag:
            self.freeze = True
            self.x = field.x_flag
            self.y = HEIGHT - H_FLOOR - 240
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(f'{PATH}/songs/success.mp3'))
            time.sleep(3.5)
            self.finish = True

    def check_ennemies(self, field:Field) -> None:
        """Check if mario hit ennemies

        :param Field field: The field on which mario evolves
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
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(f'{PATH}/songs/gameover.mp3'))
                        self.freeze = True
                        time.sleep(3.5)
                        self.finish = True

    def check_holes(self, field:Field) -> None:
        """Check if mario fall in a hole

        :param Field field: The field on which mario evolves
        """
        for x, y in field.floor + field.nx_floor:
            pos_x = x < self.x and (self.x + self.width) < x + field.h_floor
            if pos_x and y == HEIGHT and self.y == self.y0:
                self.fall()

    def colision_x(self, x1:int, w1:int, x2:int, w2:int) -> bool:
        """Check if an object 1 overllap an object 2 on the x axis

        :param int x1: The x coordinate of the object 1
        :param int w1: The width of the object 1
        :param int x2: The x coordinate of the object 2
        :param int w2: The width of the object 2
        :return bool: True if there is a collision, else False
        """
        cdt_x1 = x2 <= x1 <= x2 + w2
        cdt_x2 = x2 <= x1 + w1 <= x2 + w2
        cdt_x3 = x1 <= x2 and x1 + w1 >= x2 + w2
        cdt_x3 = x1 >= x2 and x1 + w1 <= x2 + w2
        return (cdt_x1 or cdt_x2 or cdt_x3)


    def colision_y(self, y1:int, h1:int, y2:int, h2:int) -> bool:
        """Check if an object 1 overllap an object 2 on the y axis

        :param int y1: The y coordinate of the object 1
        :param int h1: The height of the object 1
        :param int y2: The y coordinate of the object 2
        :param int h2: The height of the object 2
        :return bool: True if there is a collision, else False
        """
        cdt_y1 = y2 <= y1 <= y2 + h2
        cdt_y2 = y2 <= y1 + h1 <= y2 + h2
        cdt_y3 = y1 <= y2 and y1 + h1 >= y2 + h2
        cdt_y3 = y1 >= y2 and y1 + h1 <= y2 + h2
        return (cdt_y1 or cdt_y2 or cdt_y3)


    def check_collision(self, pos:typing.Tuple[int, int], size:typing.Tuple[int, int]) -> bool:
        """Check if mario is colliding with the field (in the hole for example)

        :param typing.Tuple[int, int] pos: The x and y position of an object
        :param typing.Tuple[int, int] size: The width and height of an object
        :return bool: True if there is collision, else False
        """
        (x, y), (h, w) = pos, size

        cd1_x = self.colision_x(self.x, self.width, x, w)
        cd1_y = self.colision_y(self.y, self.height, y, h)

        cd2_x = self.colision_x(x, w, self.x, self.width)
        cd2_y = self.colision_y(y, h, self.y, self.height)
        return (cd1_x or cd2_x) and (cd1_y or cd2_y)


    def check_coins(self, field:Field) -> None:
        """Check if Mario is on a coin

        :param Field field: The field on which mario evolves
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

    def play_sound(self, name:str, vol:int) -> None:
        """Play a given sound

        :param str name: The name of the sound to play
        :param int vol: The volume of the sound
        """
        global CRT_CHNL
        sound = pygame.mixer.Sound(f'{PATH}/songs/{name}.mp3')
        sound.set_volume(vol)
        pygame.mixer.Channel(CRT_CHNL).play(sound)

        CRT_CHNL = 1 if CRT_CHNL == 19 else CRT_CHNL + 1

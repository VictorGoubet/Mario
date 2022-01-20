import pygame

HEIGHT, WIDTH = 400, 700
H_FLOOR = 100
H_MARIO, WIDTH_MARIO = 50, 40
FPS = 25
H_JUMP = 100
crt_chnl = 1
N_END = 5

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 13)
pygame.mixer.init()
pygame.mixer.set_num_channels(20)
pygame.display.set_caption('Mario')


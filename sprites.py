import pygame
from objects import*
from config import*

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# # Menu Sprites

START_IMG = pygame.image.load("sprites\\buttons\Start1.png").convert_alpha()
START_CLICK = pygame.image.load("sprites\\buttons\Start5.png").convert_alpha()

START = Button((WIN_WIDTH/2) - 340, WIN_HEIGHT/2, START_IMG, START_CLICK, 5)


MULTI_IMG = pygame.image.load("sprites\\buttons\Multiplayer1.png").convert_alpha()
MULTI_CLICK = pygame.image.load("sprites\\buttons\Multiplayer5.png").convert_alpha()


MULTI = Button((WIN_WIDTH/2) + 10, WIN_HEIGHT/2 , MULTI_IMG, MULTI_CLICK, 5)

# # Background Sprites
BG_IMG = pygame.image.load("sprites\\background\Background.png").convert_alpha()
BG = pygame.transform.scale(BG_IMG, (WIN_WIDTH, WIN_HEIGHT))

# # Character Sprites
FIGHTER1_SHEET = pygame.image.load("sprites\players\\fighter_1.png").convert_alpha()
FIGHTER2_SHEET = pygame.image.load("sprites\players\\fighter_2.png").convert_alpha()

# # Fighter Config
FIGHTER_SIZE = (80, 120)
FIGHTER_SCALE = 3
FIGHTER_OFFSET = [[41, 40], [52, 40]]
FIGHTER1_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, FIGHTER_OFFSET]


FIGHTER2_DATA = [FIGHTER_SIZE, FIGHTER_SCALE, FIGHTER_OFFSET]

# # Animation images per row 
FIGHTER_ANIMS = [4,6,2,10,1,10,16,12,10]

fighter_1 = Fighter(200, 401, False, FIGHTER1_DATA, FIGHTER1_SHEET, FIGHTER_ANIMS, 1)
fighter_2 = Fighter(1000, 401, True, FIGHTER2_DATA, FIGHTER2_SHEET, FIGHTER_ANIMS, 2)

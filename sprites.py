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
fighter_1 = Fighter(200, 401)
fighter_2 = Fighter(1000, 401)
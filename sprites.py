import pygame
from pygame import mixer
from objects import*
from config import*

mixer.init()
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# # Music
MENU_MUSIC = pygame.mixer.Sound("music\menu.wav")
MENU_MUSIC.set_volume(0.15)

BATTLE_MUSIC = pygame.mixer.Sound("music\\battle.wav")
BATTLE_MUSIC.set_volume(0.50)

SLASH = pygame.mixer.Sound("music\slash.mp3")
SLASH.set_volume(0.5)
PARRY = pygame.mixer.Sound("music\parry.mp3")
PARRY.set_volume(1)
DEATH = pygame.mixer.Sound("music\die.mp3")
DEATH.set_volume(0.15)
ROLL = pygame.mixer.Sound("music\\roll.wav")
ROLL.set_volume(1)
JUMP = pygame.mixer.Sound("music\\jump.wav")
JUMP.set_volume(0.5)

SFX = [SLASH, PARRY, DEATH, ROLL, JUMP]

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
FIGHTER_ANIMS = [4,6,2,10,1,10,8,12,10]




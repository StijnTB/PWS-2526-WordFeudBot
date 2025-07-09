import pygame
from pygame import Color
from utils import *
pygame.init()

class Globals:
    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 600
    TILE_SIZE: int = floor(SCREEN_HEIGHT/15) #tile size should be divisible by 2 and 10
    tile_size: int = 40
    TEXT_SIZE_TILE: int = 20
    TILE_COLOR_DICT: dict = {
        "TW":Color(122,57,57),
        "TL":Color(72,91,145),
        "DW":Color(191,120,32),
        "DL":Color(113,157,101),
        "Base":Color(44,47,54),
        "Letter":Color(209,210,205)
    }
screen = pygame.display.set_mode((Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT))
pygame.display.set_caption("WordFeud")

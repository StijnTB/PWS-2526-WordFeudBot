import pygame
from pygame import Color
from utils import *


pygame.init()


class Globals:
    TILE_SIZE: int = 30  # tile size should be divisible by 2 and 10
    BUTTON_SIZE: tuple[int, int] = (148, TILE_SIZE)
    _border_between_tiles_width: int = 2
    _offset_between_screen_categories: int = 10
    amount_of_passes: int = (
        0  # every time the player or the bot passes, increase by 1. after 3, stop game
    )
    random_seed: int = 11 #the seed to use for every random generator to improve bugfixing
    SCREEN_WIDTH = (
        TILE_SIZE * 15
        + 14 * _border_between_tiles_width
        + _offset_between_screen_categories
        + BUTTON_SIZE[0]
    )
    SCREEN_HEIGHT = (
        TILE_SIZE * 15
        + 15 * _border_between_tiles_width
        + _offset_between_screen_categories
        + BUTTON_SIZE[1]
    )
    TEXT_SIZE_TILE: int = int(TILE_SIZE / 2)  # is 20
    # board_letter_empty and tilerow_letter_empty zijn zelfde / board_letter_set en tilerow_letter_base zijn zelfde / board_letter_try en tilerow_letter_selected zijn zelfde
    TILE_COLOR_DICT: dict = {
        "TW": Color(122, 57, 57),
        "TL": Color(72, 91, 145),
        "DW": Color(191, 120, 32),
        "DL": Color(113, 157, 101),
        "MI": Color(97, 72, 99),
        "Empty_tile": Color(44, 47, 54),  # grey
        "Played_tilerow_letter": Color(44, 47, 54),  # grey, same as empty_tile
        "Set_board/Base_tilerow": Color(209, 210, 205),  # greyish white
        "Try_board/Selected_tilerow": Color(255, 255, 255),  # white
    }
    global_should_recompute: bool = True

    BOARD_LAYOUT_LIST: list[list] = [
        [
            "TL",
            None,
            None,
            None,
            "TW",
            None,
            None,
            "DL",
            None,
            None,
            "TW",
            None,
            None,
            None,
            "TL",
        ],
        [
            None,
            "DL",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "DL",
            None,
        ],
        [
            None,
            None,
            "DW",
            None,
            None,
            None,
            "DL",
            None,
            "DL",
            None,
            None,
            None,
            "DW",
            None,
            None,
        ],
        [
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "DW",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
        ],
        [
            "TW",
            None,
            None,
            None,
            "DW",
            None,
            "DL",
            None,
            "DL",
            None,
            "DW",
            None,
            None,
            None,
            "TW",
        ],
        [
            None,
            "TL",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "TL",
            None,
        ],
        [
            None,
            None,
            "DL",
            None,
            "DL",
            None,
            None,
            None,
            None,
            None,
            "DL",
            None,
            "DL",
            None,
            None,
        ],
        [
            "DL",
            None,
            None,
            "DW",
            None,
            None,
            None,
            "MI",
            None,
            None,
            None,
            "DW",
            None,
            None,
            "DL",
        ],
        [
            None,
            None,
            "DL",
            None,
            "DL",
            None,
            None,
            None,
            None,
            None,
            "DL",
            None,
            "DL",
            None,
            None,
        ],
        [
            None,
            "TL",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "TL",
            None,
        ],
        [
            "TW",
            None,
            None,
            None,
            "DW",
            None,
            "DL",
            None,
            "DL",
            None,
            "DW",
            None,
            None,
            None,
            "TW",
        ],
        [
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "DW",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
        ],
        [
            None,
            None,
            "DW",
            None,
            None,
            None,
            "DL",
            None,
            "DL",
            None,
            None,
            None,
            "DW",
            None,
            None,
        ],
        [
            None,
            "DL",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "TL",
            None,
            None,
            None,
            "DL",
            None,
        ],
        [
            "TL",
            None,
            None,
            None,
            "TW",
            None,
            None,
            "DL",
            None,
            None,
            "TW",
            None,
            None,
            None,
            "TL",
        ],
    ]

    TILE_LETTER_DICT: dict = {
        "A": {"amount": 7, "value": 1},
        "B": {"amount": 2, "value": 4},
        "C": {"amount": 2, "value": 5},
        "D": {"amount": 5, "value": 2},
        "E": {"amount": 18, "value": 1},
        "F": {"amount": 2, "value": 4},
        "G": {"amount": 3, "value": 3},
        "H": {"amount": 2, "value": 4},
        "I": {"amount": 4, "value": 2},
        "J": {"amount": 2, "value": 4},
        "K": {"amount": 3, "value": 3},
        "L": {"amount": 3, "value": 3},
        "M": {"amount": 3, "value": 3},
        "N": {"amount": 11, "value": 1},
        "O": {"amount": 6, "value": 1},
        "P": {"amount": 2, "value": 4},
        "Q": {"amount": 1, "value": 10},
        "R": {"amount": 5, "value": 2},
        "S": {"amount": 5, "value": 2},
        "T": {"amount": 5, "value": 2},
        "U": {"amount": 3, "value": 2},
        "V": {"amount": 2, "value": 4},
        "W": {"amount": 2, "value": 5},
        "X": {"amount": 1, "value": 8},
        "Y": {"amount": 1, "value": 8},
        "Z": {"amount": 2, "value": 5},
        " ": {"amount": 2, "value": 0},
    }
    SCREEN_TILES_STARTING_HEIGHT: int = _offset_between_screen_categories * 0
    ROW_TILES_SCREEN_HEIGHT: int = (
        SCREEN_TILES_STARTING_HEIGHT
        + TILE_SIZE * 15
        + 15 * _border_between_tiles_width
        + int(TILE_SIZE / 2)
        + _offset_between_screen_categories
    )  # the center y-coordinate on the screen of the players row of tiles


game_display = pygame.display
screen = pygame.display.set_mode((Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT))
pygame.display.set_caption("WordFeud")

import pygame
from pygame import Color
from typing import Literal

pygame.init()
class Globals:
    TILE_SIZE: int = 40  # tile size should be divisible by 2 and 10
    BUTTON_SIZE: tuple[int, int] = (
        148,
        TILE_SIZE,
    )  # the size of a button, width is standard due to text size
    EMPTY_TILE: set[None | str] = {None, "DW","DL","TW","TL","","MI"}
    BORDER_BETWEEN_TILES_WIDTH: int = 2  # the amount of pixels between 2 tiles
    OFFSET_BETWEEN_SCREEN_CATEGORIES: int = (
        10  # the amount of pixels between different areas of the screen (the board, the buttons, the tilerow etc.)
    )
    amount_of_passes: int = (
        0  # every time the player or the bot passes, increase by 1. after 3, stop game
    )
    RANDOM_SEED: int = (
        17 # the seed to use for every random generator to improve bugfixing
    )
    BINGO_BONUS_SCORE_MULTIPLIER: float = (
        0.5  # a multiplier for the bingo bonus score to vary its influence
    )
    BOARDPOSITION_FACTORS: dict[str, float] = (
        {  # a group of factors used for calculating the boardposition degradation factor
            "TW": 22.5,
            "TL": 2,
            "DW": 15,
            "DL": 1.3333,
            "Vowel": 2,
            "Consonant": 1,
            "Addition_Danger": 0.1,  # the value per available letter in bag - own letters
            "danger_word_played_alongside": 1,
            "multiplication_danger_base": 0.1
        }
    )
    BOARDPOSITION_FACTOR_DISTANCE_REDUCTOR: float = (
        0.87  # a factor used to define the reduction of influence a tile has in the degradation score
    )
    SCREEN_WIDTH: int = (
        TILE_SIZE * 15
        + 14 * BORDER_BETWEEN_TILES_WIDTH
        + OFFSET_BETWEEN_SCREEN_CATEGORIES
        + BUTTON_SIZE[0]
    )  # the screen width, dependent mainly on the tile size
    SCREEN_HEIGHT: int = (
        TILE_SIZE * 15
        + 15 * BORDER_BETWEEN_TILES_WIDTH
        + OFFSET_BETWEEN_SCREEN_CATEGORIES
        + BUTTON_SIZE[1]
    )  # the screen height, dependent mainly on the tile size
    TEXT_SIZE_TILE: int = int(TILE_SIZE / 2)  # is 20
    TILE_COLOR_DICT: dict[str, Color] = {
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
    global_should_recompute: bool = (
        True  # a variable which tells the program to do a full visual recomputation. used sparingly, only when a visual element has to fully disappear.
    )

    BOARD_LAYOUT_LIST: list[list[Literal["TL", "TW", "DL", "DW", "MI", None]]] = [
        ["TL",None,None,None,"TW",None,None,"DL",None,None,"TW",None,None,None,"TL",],
        [None,"DL",None,None,None,"TL",None,None,None,"TL",None,None,None,"DL",None,],
        [None,None,"DW",None,None,None,"DL",None,"DL",None,None,None,"DW",None,None,],
        [None,None,None,"TL",None,None,None,"DW",None,None,None,"TL",None,None,None,],
        ["TW",None,None,None,"DW",None,"DL",None,"DL",None,"DW",None,None,None,"TW",],
        [None,"TL",None,None,None,"TL",None,None,None,"TL",None,None,None,"TL",None,],
        [None,None,"DL",None,"DL",None,None,None,None,None,"DL",None,"DL",None,None,],
        ["DL",None,None,"DW",None,None,None,"MI",None,None,None,"DW",None,None,"DL",],
        [None,None,"DL",None,"DL",None,None,None,None,None,"DL",None,"DL",None,None,],
        [None,"TL",None,None,None,"TL",None,None,None,"TL",None,None,None,"TL",None,],
        ["TW",None,None,None,"DW",None,"DL",None,"DL",None,"DW",None,None,None,"TW",],
        [None,None,None,"TL",None,None,None,"DW",None,None,None,"TL",None,None,None,],
        [None,None,"DW",None,None,None,"DL",None,"DL",None,None,None,"DW",None,None,],
        [None,"DL",None,None,None,"TL",None,None,None,"TL",None,None,None,"DL",None,],
        ["TL",None,None,None,"TW",None,None,"DL",None,None,"TW",None,None,None,"TL",],
    ]

    TILE_LETTER_DICT: dict[str, dict[str, int]] = {
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
        " ": {"amount": 0, "value": 0},
    }
    SCREEN_TILES_STARTING_HEIGHT: int = OFFSET_BETWEEN_SCREEN_CATEGORIES * 0
    ROW_TILES_SCREEN_HEIGHT: int = (
        SCREEN_TILES_STARTING_HEIGHT
        + TILE_SIZE * 15
        + 15 * BORDER_BETWEEN_TILES_WIDTH
        + int(TILE_SIZE / 2)
        + OFFSET_BETWEEN_SCREEN_CATEGORIES
    )  # the center y-coordinate on the screen of the players row of tiles

    players_tilerows: dict[int, list[str]] = {1: [], 2: []}


    
game_display = pygame.display
screen = pygame.display.set_mode((Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT))
pygame.display.set_caption("WordFeud")

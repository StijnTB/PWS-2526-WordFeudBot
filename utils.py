import pygame
from globals import Globals
from tileclass import BoardTile
from typing import TypedDict, Optional

def floor(number: float) -> int:
    if round(number) - number > 0:
        return int(number - (round(number) - number))
    else:
        return round(number)


def ceil(number: float) -> int:
    if round(number) - number > 0:
        return round(number)
    else:
        return int(number - (round(number) - number))


def recalculate_letters(
    pygame_font: pygame.font.Font, text: str, central_coordinates: tuple[int, int]
) -> tuple[int,int]:
    highest_letter_height: int = 0
    text_width: int = 0
    for letter_used in text:
        letter_width, letter_height = pygame_font.size(letter_used)
        text_width += letter_width
        if letter_height > highest_letter_height:
            highest_letter_height = letter_height
    text_coordinates: tuple[int,int] = (
        central_coordinates[0] - floor(text_width / 2),
        central_coordinates[1] - floor(highest_letter_height / 2),
    )
    return text_coordinates


def calculate_text_dimensions(
    pygame_font: pygame.font.Font, text: str
) -> tuple[int, int]:
    highest_letter_height: int = 0
    text_width: int = 0
    for letter_used in text:
        letter_width, letter_height = pygame_font.size(letter_used)
        text_width += letter_width
        if letter_height > highest_letter_height:
            highest_letter_height = letter_height
    return (text_width, highest_letter_height)

class GameBoardCell(TypedDict):
    type: Optional[str]
    letter: Optional[str]
    tile_object: BoardTile

def get_expected_multiplication(current_tile: tuple[int,int], check_direction: tuple[int,int], game_board: dict[str, dict[str, GameBoardCell]]) -> float:
    expected_multiplication: float = Globals.BOARDPOSITION_FACTORS["multiplication_danger_base"]
    starting_tile: tuple[int,int] = (
        current_tile[0]
        - check_direction[0] * current_tile[0],
        current_tile[1]
        - check_direction[1] * current_tile[1]
    )
    for check_tile in [
        game_board[
            str(starting_tile[0] + index * check_direction[0])
        ][str(starting_tile[1] + index * check_direction[1])
        ]["tile_object"]
        for index in range(0,14)
    ]:
        if check_tile.letter in ("TW", "DW"):
            distance_movetile_to_checktile: int = (
                (check_tile.board_coordinates[0] - current_tile[0]) ** 2
                + (check_tile.board_coordinates[1] - current_tile[1]) ** 2
            ) ** 0.5
            expected_multiplication *= Globals.BOARDPOSITION_FACTORS[check_tile.letter] ** (Globals.BOARDPOSITION_FACTOR_DISTANCE_REDUCTOR ** distance_movetile_to_checktile)
    return expected_multiplication
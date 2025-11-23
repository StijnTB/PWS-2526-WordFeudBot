import pygame
from globals import Globals
from typing import Literal, TypedDict, Optional
from tileclass import BoardTile

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

from typing import Literal

def DictBinSearch(searchdict: dict[str, str], searchable_key: str) -> Literal[-1] | str:
    keys = sorted(searchdict.keys())   # VERPLICHT: sorteer de keys
    left, right = 0, len(keys) - 1
    
    while left <= right:
        mid = (left + right) // 2
        key = keys[mid]
        if searchable_key == key:
            return searchdict[key]     # return de waarde direct
        elif searchable_key > key:
            left = mid + 1
        else:
            right = mid - 1

    return -1


class GameBoardCell(TypedDict):
    type: Optional[str]
    letter: Optional[str]
    tile_object: BoardTile
 
def get_expected_multiplication(current_tile: tuple[int,int], check_direction: tuple[int,int], game_board: dict[str, dict[str, GameBoardCell]]) -> float:
    expected_multiplication: float = Globals.BOARDPOSITION_FACTORS["multiplication_danger_base"]
    danger_xL: float = 0
    starting_tile: tuple[int,int] = (
        current_tile[0]
        - check_direction[0] * current_tile[0],
        current_tile[1]
        - check_direction[1] * current_tile[1]
    )
    starting_tile = (
        starting_tile[0] if starting_tile[0] != -1 else 0,
        starting_tile[1] if starting_tile[1] != -1 else 0
    )
    for check_tile in [
        game_board[
            str(starting_tile[0] + index * check_direction[0])
        ][str(starting_tile[1] + index * check_direction[1])
        ]["tile_object"]
        for index in range(0,15)
    ]:
        
        if check_tile.letter in ("TW", "DW"):
            distance_movetile_to_checktile: int = (
                (check_tile.board_coordinates[0] - current_tile[0]) ** 2
                + (check_tile.board_coordinates[1] - current_tile[1]) ** 2
            ) ** 0.5
            expected_multiplication *= Globals.BOARDPOSITION_FACTORS[check_tile.letter] ** (Globals.BOARDPOSITION_FACTOR_DISTANCE_REDUCTOR ** distance_movetile_to_checktile)
        if check_tile.letter in ("DL", "TL"):
            distance_movetile_to_checktile: int = (
                (check_tile.board_coordinates[0] - current_tile[0]) ** 2
                + (check_tile.board_coordinates[1] - current_tile[1]) ** 2
            ) ** 0.5
            if distance_movetile_to_checktile == 1:
                if game_board[str(current_tile[0])][str(current_tile[1])]["tile_object"].letter in ("A", "E", "O", "I", "U"):
                    danger_xL += (3 * Globals.BOARDPOSITION_FACTORS[check_tile.letter]) ** (Globals.BOARDPOSITION_FACTOR_DISTANCE_REDUCTOR)
                elif game_board[str(current_tile[0])][str(current_tile[1])]["tile_object"].letter in ("K", "S"):
                    danger_xL += Globals.BOARDPOSITION_FACTORS[check_tile.letter] ** (Globals.BOARDPOSITION_FACTOR_DISTANCE_REDUCTOR)
                elif game_board[str(current_tile[0])][str(current_tile[1])]["tile_object"].letter not in ("Q", "Y", "V", "C"):
                    danger_xL += (0.25 * Globals.BOARDPOSITION_FACTORS[check_tile.letter]) ** (Globals.BOARDPOSITION_FACTOR_DISTANCE_REDUCTOR)
            
    expected_multiplication += danger_xL
    return expected_multiplication
 
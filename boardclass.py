import pygame
from tileclass import *
from trieclass import TRIE
from globals import Globals
from typing import TypedDict, Optional, Literal

pygame.init()


class game_board_cell(TypedDict):
    type: Optional[str]
    letter: Optional[str]
    tile_object: BoardTile


class Board:
    def __init__(
        self,
        original_board_layout: list[list[Literal["TW", "TL", "DW", "DL", "MI"] | None]],
        word_tree: TRIE,
    ) -> None:
        self._original_board_layout: list[
            list[Literal["TW", "TL", "DW", "DL", "MI"] | None]
        ] = original_board_layout
        self._word_tree: TRIE = word_tree
        self._game_board: dict[str, dict[str, game_board_cell]] = {}
        self.is_first_turn: bool = True
        self._used_rows: list[int] = [False for _ in range(0, 15)]
        self._used_columns: list[int] = [False for _ in range(0, 15)]
        for row_index in range(0, len(self._original_board_layout)):
            self._game_board[str(row_index)] = {}
            for column_index in range(0, 15):
                original_tile: str | None = self._original_board_layout[row_index][
                    column_index
                ]
                self._game_board[str(row_index)][str(column_index)] = {
                    "type": self._original_board_layout[row_index][column_index],
                    "letter": None,
                    "tile_object": BoardTile(
                        letter=(
                            ""
                            if original_tile == None or original_tile == "MI"
                            else str(original_tile)
                        ),
                        tile_type=(
                            original_tile if original_tile != None else "Empty_tile"
                        ),
                        board_coords=(row_index, column_index),
                    ),
                }

    @property
    def used_rows(self) -> list[int]:
        return self._used_rows

    @property
    def used_columns(self) -> list[int]:
        return self._used_columns

    def update(self) -> None:
        for row in self._game_board:
            for column in self._game_board[row]:
                tile_object: BoardTile = self._game_board[row][column]["tile_object"]
                tile_object.update()

    @property
    def game_board(self) -> dict[str, dict[str, game_board_cell]]:
        return self._game_board

    @property
    def word_tree(self) -> TRIE:
        return self._word_tree

    def get_row_coordinate(self, vertical_coordinate: int) -> int:
        for index in range(0, 15):
            if index < 15:
                if (
                    (
                        Globals.SCREEN_TILES_STARTING_HEIGHT
                        + (Globals.TILE_SIZE + Globals.BORDER_BETWEEN_TILES_WIDTH)
                        * index
                    )
                    <= vertical_coordinate
                    < (
                        Globals.SCREEN_TILES_STARTING_HEIGHT
                        + (Globals.TILE_SIZE + Globals.BORDER_BETWEEN_TILES_WIDTH)
                        * (index + 1)
                    )
                ):
                    return index
        return -1

    def get_column_coordinate(self, horizontal_coordinate: int) -> int:
        for index in range(0, 15):
            if index < 15:
                if (
                    (Globals.TILE_SIZE + Globals.BORDER_BETWEEN_TILES_WIDTH) * index
                    <= horizontal_coordinate
                    < (Globals.TILE_SIZE + Globals.BORDER_BETWEEN_TILES_WIDTH)
                    * (index + 1)
                ):
                    return index
        return -1

    def get_clicked_tile_coordinates(
        self, mouse_coordinates: tuple[int, int]
    ) -> tuple[int, int]:
        row_coordinate: int = self.get_row_coordinate(mouse_coordinates[1])
        column_coordinate: int = self.get_column_coordinate(mouse_coordinates[0])
        return (row_coordinate, column_coordinate)

    def set_letter_to_tile(
        self, letter: str, tile_coordinates: tuple[int, int]
    ) -> bool:
        selected_tile: BoardTile = self.game_board[str(tile_coordinates[0])][
            str(tile_coordinates[1])
        ]["tile_object"]
        if len(selected_tile.letter) != 1 and len(letter) == 1:
            selected_tile.letter = letter
            selected_tile.tile_type = "Try_board/Selected_tilerow"
            # Globals.global_should_recompute = True
            return True
        else:
            return False

    def get_tile_object(self, tile_coordinates: tuple[int, int]) -> BoardTile:
        return self._game_board[str(tile_coordinates[0])][str(tile_coordinates[1])][
            "tile_object"
        ]

    def reset_tile(self, clicked_tile_coordinates: tuple[int, int]):
        clicked_tile_y: int = clicked_tile_coordinates[0]
        clicked_tile_x: int = clicked_tile_coordinates[1]
        original_type: str | None = Globals.BOARD_LAYOUT_LIST[clicked_tile_y][
            clicked_tile_x
        ]
        if isinstance(original_type, str):
            original_tile_type = original_type
        else:
            original_tile_type = "Empty_tile"
        tile_object: BoardTile = self.get_tile_object(clicked_tile_coordinates)
        tile_object.is_attempt_blank = False
        tile_object.tile_type = original_tile_type
        if tile_object.tile_type in ["TW", "TL", "DW", "DL"]:
            tile_object.letter = tile_object.tile_type
        else:
            tile_object.letter = ""

        # Globals.global_should_recompute = True

    def reset_tiles(self, reset_coordinates_list: list[tuple[int, int]]):
        for coordinate_set in reset_coordinates_list:
            self.reset_tile(coordinate_set)

    def _direction_of_word(
        self, tile_coordinates_list: list[tuple[int, int]]
    ) -> tuple[int, int]:
        coordinate_set: tuple[int, int]
        row_set: set[int] = set()
        column_set: set[int] = set()
        for coordinate_set in tile_coordinates_list:
            row_set.add(coordinate_set[0])
            column_set.add(coordinate_set[1])
        if (
            len(row_set) == 1 and len(column_set) >= 1
        ):  # 1 row coordinate, multiple column coordinates so horizontal word / 1 row coordinate, 1 column coordinate so 1 letter word
            return (0, 1)
        elif (
            len(row_set) > 1 and len(column_set) == 1
        ):  # multiple row coordinates, 1 column coordinate so vertical word
            return (1, 0)
        else:  # bugged coordinates / multiple row coordinates and multiple column coordinates / no coordinates are given -> no tiles are set
            return (0, 0)

    def get_word_from_tile(
        self,
        known_tile_coordinate: tuple[int, int],
        direction: tuple[int, int],
        complete_tile_list: list[tuple[int, int]],
        blank_tiles: list[tuple[int, int]] | None = None,
    ) -> tuple[str, int]:
        word_formed_letters: list[str] = []
        letter_values: list[int] = []
        double_word_counter: int = 0
        triple_word_counter: int = 0
        tile_object: BoardTile = self.game_board[str(known_tile_coordinate[0])][
            str(known_tile_coordinate[1])
        ]["tile_object"]
        word_formed_letters.append(tile_object.letter)
        original_tile_type = Globals.BOARD_LAYOUT_LIST[
            tile_object.board_coordinates[0]
        ][tile_object.board_coordinates[1]]
        letter_value_multiplier: int = 1
        tile_value_zero: bool = False
        if blank_tiles:
            if known_tile_coordinate in blank_tiles:
                tile_value_zero = True
        if original_tile_type == "TL":
            letter_value_multiplier = 3
        elif original_tile_type == "DL":
            letter_value_multiplier = 2
        elif original_tile_type == "TW":
            triple_word_counter += 1
        elif original_tile_type == "DW":
            double_word_counter += 1
        if not tile_value_zero:
            letter_values.append(tile_object.tile_value * letter_value_multiplier)
        while tile_object.letter not in ["", "TW", "TL", "DW", "DL"]:
            if (
                tile_object.board_coordinates[0] - direction[0] < 0
                or tile_object.board_coordinates[1] - direction[1] < 0
            ):
                break
            tile_object = self.game_board[
                str(tile_object.board_coordinates[0] - direction[0])
            ][str(tile_object.board_coordinates[1] - direction[1])]["tile_object"]
            if len(tile_object.letter) == 1:
                word_formed_letters.insert(0, tile_object.letter)
                letter_value_multiplier = 1
                if (
                    tile_object.board_coordinates in complete_tile_list
                ):  # only get multipliers etc. when tile is laid in this turn
                    original_tile_type = Globals.BOARD_LAYOUT_LIST[
                        tile_object.board_coordinates[0]
                    ][tile_object.board_coordinates[1]]
                    if original_tile_type == "TL":
                        letter_value_multiplier = 3
                    elif original_tile_type == "DL":
                        letter_value_multiplier = 2
                    elif original_tile_type == "TW":
                        triple_word_counter += 1
                    elif original_tile_type == "DW":
                        double_word_counter += 1
                if blank_tiles:
                    if not tile_object.board_coordinates in blank_tiles:
                        letter_values.insert(
                            0, tile_object.tile_value * letter_value_multiplier
                        )
                else:
                    letter_values.insert(
                        0, tile_object.tile_value * letter_value_multiplier
                    )
        tile_object = self.game_board[str(known_tile_coordinate[0])][
            str(known_tile_coordinate[1])
        ]["tile_object"]
        while tile_object.letter not in ["", "TW", "TL", "DW", "DL"]:
            if (
                tile_object.board_coordinates[0] + direction[0] > 14
                or tile_object.board_coordinates[1] + direction[1] > 14
            ):
                break
            tile_object = self.game_board[
                str(tile_object.board_coordinates[0] + direction[0])
            ][str(tile_object.board_coordinates[1] + direction[1])]["tile_object"]
            if len(tile_object.letter) == 1:
                letter_value_multiplier = 1
                word_formed_letters.append(tile_object.letter)
                if tile_object.board_coordinates in complete_tile_list:
                    original_tile_type = Globals.BOARD_LAYOUT_LIST[
                        tile_object.board_coordinates[0]
                    ][tile_object.board_coordinates[1]]
                    if original_tile_type == "TL":
                        letter_value_multiplier = 3
                    elif original_tile_type == "DL":
                        letter_value_multiplier = 2
                    elif original_tile_type == "TW":
                        triple_word_counter += 1
                    elif original_tile_type == "DW":
                        double_word_counter += 1
                if blank_tiles:
                    if not tile_object.board_coordinates in blank_tiles:
                        letter_values.append(
                            tile_object.tile_value * letter_value_multiplier
                        )
                else:
                    letter_values.append(
                        tile_object.tile_value * letter_value_multiplier
                    )
        word_value: int = 0
        for value in letter_values:
            word_value += value
        word_value = word_value * (2**double_word_counter) * (3**triple_word_counter)
        return ("".join(word_formed_letters), word_value)

    def finalize_set_tiles(self, tile_coordinates_list: list[tuple[int, int]]):
        tile_object: BoardTile
        coordinate_set: tuple[int, int]
        for coordinate_set in tile_coordinates_list:
            if not self._used_rows[coordinate_set[0]]:
                self._used_rows[coordinate_set[0]] = True
            if not self._used_columns[coordinate_set[1]]:
                self._used_columns[coordinate_set[1]] = True
            tile_object = self.game_board[str(coordinate_set[0])][
                str(coordinate_set[1])
            ]["tile_object"]
            tile_object.tile_type = "Set_board/Base_tilerow"

    def player_try_word(
        self, tile_coordinates_list: list[tuple[int, int]]
    ) -> tuple[
        bool, int
    ]:  # returns whether try works or fails, and the score (score is 0 when fail)
        if len(tile_coordinates_list) == 0:
            print("no tiles submitted")
            return (False, 0)
        if self.is_first_turn:
            if len(tile_coordinates_list) == 1:
                print("submitted only 1 tile on first turn")
                return (False, 0)
            tile_is_on_center: bool = False
            for tile in tile_coordinates_list:
                if tile == (7, 7):
                    tile_is_on_center = True
                    break
            if not tile_is_on_center:
                print("no tile was on center in first turn")
                return (False, 0)
        word_direction = self._direction_of_word(tile_coordinates_list)
        if word_direction == (0, 0):
            print("multiple rows and columns is not allowed")
            return (False, 0)
        first_tile_in_main_coordinates: tuple[int, int] = (15, 15)
        coordinate_selector: int = 1 if word_direction == (0, 1) else 0
        for tile in tile_coordinates_list:
            if (
                tile[coordinate_selector]
                < first_tile_in_main_coordinates[coordinate_selector]
            ):
                first_tile_in_main_coordinates = tile
        # from the first tile, the main word is formed. after that, all tiles check in the non-main direction
        words_created_set: set[str] = set()
        total_value: int = 0
        main_word, main_word_value = self.get_word_from_tile(
            first_tile_in_main_coordinates, word_direction, tile_coordinates_list
        )
        print(main_word_value)
        if len(main_word) > 1:
            words_created_set.add(main_word)
            total_value += main_word_value
        alternative_word_direction: tuple[int, int] = (
            (1, 0) if word_direction == (0, 1) else (0, 1)
        )
        for tile in tile_coordinates_list:
            word_created, word_value = self.get_word_from_tile(
                tile, alternative_word_direction, tile_coordinates_list
            )
            if len(word_created) > 1:
                words_created_set.add(word_created)
                total_value += word_value
        for word_created in words_created_set:
            if not self._word_tree.search_word(
                word_created
            ):  # word was not found in word list
                print(f"submitted word '{word_created}' was not found in the word list")
                return (False, 0)
        print(tile_coordinates_list)
        if len(tile_coordinates_list) == 7:
            print("extra 40 for 7 letters played")
            total_value += 40  # 7 tiles laid on board, so add 40 points
        self.finalize_set_tiles(tile_coordinates_list)
        self.is_first_turn = False
        return (True, total_value)

    def bot_play_word(
        self,
        tile_coordinates_list: list[tuple[int, int]],
        letters_list: list[str],
        blanks_list: list[tuple[int, int]],
    ):
        if len(tile_coordinates_list) == len(letters_list):
            for index in range(len(tile_coordinates_list)):
                if not self._used_rows[tile_coordinates_list[index][0]]:
                    self._used_rows[tile_coordinates_list[index][0]] = True
                if not self._used_columns[tile_coordinates_list[index][1]]:
                    self._used_columns[tile_coordinates_list[index][1]] = True
                tile_coordinate: tuple[int, int] = tile_coordinates_list[index]
                tile_letter: str = letters_list[index]
                self.game_board[str(tile_coordinate[0])][str(tile_coordinate[1])][
                    "letter"
                ] = tile_letter
                tile_object: BoardTile = self.game_board[str(tile_coordinate[0])][
                    str(tile_coordinate[1])
                ]["tile_object"]
                if tile_object.board_coordinates in blanks_list:
                    tile_object.is_attempt_blank = True
                tile_object.letter = tile_letter
                tile_object.tile_type = "Set_board/Base_tilerow"
                if tile_object.board_coordinates in blanks_list:
                    tile_object.is_attempt_blank = True
            self.is_first_turn = False

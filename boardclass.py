import pygame
from tileclass import *
from trieclass import TRIE
from globals import Globals
from random import randint

pygame.init()


class Board:
    def __init__(self, original_board_layout: list, word_tree: TRIE) -> None:
        self._original_board_layout: list = original_board_layout
        self._word_tree: TRIE = word_tree
        self._game_board: dict = {}
        self._try_game_board: dict
        self._is_first_turn: bool = True
        for row_index in range(0, 15):
            self._game_board[str(row_index)] = {}
            for column_index in range(0, 15):
                self._game_board[str(row_index)][str(column_index)] = {
                    "type": self._original_board_layout[row_index][column_index],
                    "letter": None,
                    "tile_object": BoardTile(
                        letter=(
                            ""
                            if self._original_board_layout[row_index][column_index]
                            in [None, "MI"]
                            else self._original_board_layout[row_index][column_index]
                        ),
                        tile_type=(
                            self._original_board_layout[row_index][column_index]
                            if self._original_board_layout[row_index][column_index]
                            != None
                            else "Empty_tile"
                        ),
                        board_coords=(row_index, column_index),
                    ),
                }
        # self._try_game_board =

    def update(self) -> None:
        for row in self._game_board:
            for column in self._game_board[row]:
                tile_object: BoardTile = self._game_board[row][column]["tile_object"]
                tile_object.update()

    @property
    def game_board(self) -> dict:
        return self._game_board

    def get_row_coordinate(self, vertical_coordinate: int) -> int:
        for index in range(0, 15):
            if index < 15:
                if (
                    (
                        Globals.SCREEN_TILES_STARTING_HEIGHT
                        + (Globals.TILE_SIZE + Globals._border_between_tiles_width)
                        * index
                    )
                    <= vertical_coordinate
                    < (
                        Globals.SCREEN_TILES_STARTING_HEIGHT
                        + (Globals.TILE_SIZE + Globals._border_between_tiles_width)
                        * (index + 1)
                    )
                ):
                    return index
        return -1

    def get_column_coordinate(self, horizontal_coordinate: int) -> int:
        for index in range(0, 15):
            if index < 15:
                if (
                    (Globals.TILE_SIZE + Globals._border_between_tiles_width) * index
                    <= horizontal_coordinate
                    < (Globals.TILE_SIZE + Globals._border_between_tiles_width)
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
        if len(selected_tile.letter) != 1:
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

    def reset_tile(self, clicked_tile_coordinates):
        clicked_tile_y: int = clicked_tile_coordinates[0]
        clicked_tile_x: int = clicked_tile_coordinates[1]
        original_tile_type: str = (
            Globals.BOARD_LAYOUT_LIST[clicked_tile_y][clicked_tile_x]
            if Globals.BOARD_LAYOUT_LIST[clicked_tile_y][clicked_tile_x] != None
            else "Empty_tile"
        )
        tile_object: BoardTile = self.get_tile_object(clicked_tile_coordinates)
        tile_object._is_attempt_blank = False
        tile_object.tile_type = original_tile_type
        if tile_object.tile_type in ["TW", "TL", "DW", "DL"]:
            tile_object.letter = tile_object.tile_type
        else:
            tile_object.letter = ""

        # Globals.global_should_recompute = True

    def reset_tiles(self, reset_coordinates_list: list[tuple[int, int]]):
        coordinate_set: tuple[int, int]
        for coordinate_set in reset_coordinates_list:
            if isinstance(coordinate_set, tuple):
                self.reset_tile(coordinate_set)

    def _direction_of_word(
        self, tile_coordinates_list: list[tuple[int, int]]
    ) -> tuple[int, int]:
        coordinate_set: tuple[int, int]
        row_set: set = set()
        column_set: set = set()
        for coordinate_set in tile_coordinates_list:
            if isinstance(coordinate_set, tuple):
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
    ) -> tuple[str, int]:
        word_formed_letters: list[str] = []
        letter_values: list[int] = []
        double_word_counter: int = 0
        triple_word_counter: int = 0
<<<<<<< Updated upstream
        if isinstance(known_tile_coordinate, tuple):
            tile_object: BoardTile = self.game_board[str(known_tile_coordinate[0])][
                str(known_tile_coordinate[1])
            ]["tile_object"]
            word_formed_letters.append(tile_object.letter)
            original_tile_type = Globals.BOARD_LAYOUT_LIST[
                tile_object._board_coordinates[0]
            ][tile_object._board_coordinates[1]]
            letter_value_multiplier: int = 1
            if original_tile_type == "TL":
                letter_value_multiplier = 2
            elif original_tile_type == "DL":
                letter_value_multiplier = 3
            elif original_tile_type == "TW":
                double_word_counter += 1
            elif original_tile_type == "DW":
                triple_word_counter += 1
            letter_values.append(tile_object._tile_value * letter_value_multiplier)
            while tile_object.letter not in ["", "TW", "TL", "DW", "DL"]:
                tile_object = self.game_board[
                    str(tile_object._board_coordinates[0] - direction[0])
                ][str(tile_object._board_coordinates[1] - direction[1])]["tile_object"]
                if len(tile_object.letter) == 1:
                    word_formed_letters.insert(0, tile_object.letter)
                    letter_value_multiplier = 1
                    if (
                        tile_object._board_coordinates in complete_tile_list
                    ):  # only get multipliers etc. when tile is laid in this turn
                        original_tile_type = Globals.BOARD_LAYOUT_LIST[
                            tile_object._board_coordinates[0]
                        ][tile_object._board_coordinates[1]]
                        if original_tile_type == "TL":
                            letter_value_multiplier = 2
                        elif original_tile_type == "DL":
                            letter_value_multiplier = 3
                        elif original_tile_type == "TW":
                            double_word_counter += 1
                        elif original_tile_type == "DW":
                            triple_word_counter += 1
                    letter_values.insert(
                        0, tile_object._tile_value * letter_value_multiplier
                    )
            tile_object = self.game_board[str(known_tile_coordinate[0])][
                str(known_tile_coordinate[1])
            ]["tile_object"]
            while tile_object.letter not in ["", "TW", "TL", "DW", "DL"]:
                tile_object = self.game_board[
                    str(tile_object._board_coordinates[0] + direction[0])
                ][str(tile_object._board_coordinates[1] + direction[1])]["tile_object"]
                if len(tile_object.letter) == 1:
                    letter_value_multiplier = 1
                    word_formed_letters.append(tile_object.letter)
                    if tile_object._board_coordinates in complete_tile_list:
                        original_tile_type = Globals.BOARD_LAYOUT_LIST[
                            tile_object._board_coordinates[0]
                        ][tile_object._board_coordinates[1]]
                        if original_tile_type == "TL":
                            letter_value_multiplier = 2
                        elif original_tile_type == "DL":
                            letter_value_multiplier = 3
                        elif original_tile_type == "TW":
                            double_word_counter += 1
                        elif original_tile_type == "DW":
                            triple_word_counter += 1
                    letter_values.append(
                        tile_object._tile_value * letter_value_multiplier
                    )
            word_value: int = 0
            print(letter_values)
            for value in letter_values:
                word_value += value
            word_value = (
                word_value * (2**double_word_counter) * (3**triple_word_counter)
            )
            return ("".join(word_formed_letters), word_value)
        return ("", 0)
=======

        tile_object: BoardTile = self.game_board[str(known_tile_coordinate[0])][
            str(known_tile_coordinate[1])
        ]["tile_object"]
        word_formed_letters.append(tile_object.letter)
        original_tile_type = Globals.BOARD_LAYOUT_LIST[
            tile_object._board_coordinates[0]
        ][tile_object._board_coordinates[1]]
        letter_value_multiplier: int = 1
        if original_tile_type == "TL":
            letter_value_multiplier = 3
        elif original_tile_type == "DL":
            letter_value_multiplier = 2
        elif original_tile_type == "TW":
            double_word_counter += 1
        elif original_tile_type == "DW":
            triple_word_counter += 1
        letter_values.append(tile_object._tile_value * letter_value_multiplier)
        while tile_object.letter not in ["", "TW", "TL", "DW", "DL"]:
            if (
                tile_object._board_coordinates[0] - direction[0] < 0
                or tile_object._board_coordinates[1] - direction[1] < 0
            ):
                break
            tile_object = self.game_board[
                str(tile_object._board_coordinates[0] - direction[0])
            ][str(tile_object._board_coordinates[1] - direction[1])]["tile_object"]
            if len(tile_object.letter) == 1:
                word_formed_letters.insert(0, tile_object.letter)
                letter_value_multiplier = 1
                if (
                    tile_object._board_coordinates in complete_tile_list
                ):  # only get multipliers etc. when tile is laid in this turn
                    original_tile_type = Globals.BOARD_LAYOUT_LIST[
                        tile_object._board_coordinates[0]
                    ][tile_object._board_coordinates[1]]
                    if original_tile_type == "TL":
                        letter_value_multiplier = 3
                    elif original_tile_type == "DL":
                        letter_value_multiplier = 2
                    elif original_tile_type == "TW":
                        triple_word_counter += 1
                    elif original_tile_type == "DW":
                        double_word_counter += 1
                letter_values.insert(
                    0, tile_object._tile_value * letter_value_multiplier
                )
        tile_object = self.game_board[str(known_tile_coordinate[0])][
            str(known_tile_coordinate[1])
        ]["tile_object"]
        while tile_object.letter not in ["", "TW", "TL", "DW", "DL"]:
            if (
                tile_object._board_coordinates[0] + direction[0] > 14
                or tile_object._board_coordinates[1] + direction[1] > 14
            ):
                break
            tile_object = self.game_board[
                str(tile_object._board_coordinates[0] + direction[0])
            ][str(tile_object._board_coordinates[1] + direction[1])]["tile_object"]
            if len(tile_object.letter) == 1:
                letter_value_multiplier = 1
                word_formed_letters.append(tile_object.letter)
                if tile_object._board_coordinates in complete_tile_list:
                    original_tile_type = Globals.BOARD_LAYOUT_LIST[
                        tile_object._board_coordinates[0]
                    ][tile_object._board_coordinates[1]]
                    if original_tile_type == "TL":
                        letter_value_multiplier = 3
                    elif original_tile_type == "DL":
                        letter_value_multiplier = 2
                    elif original_tile_type == "TW":
                        triple_word_counter += 1
                    elif original_tile_type == "DW":
                        double_word_counter += 1
                letter_values.append(tile_object._tile_value * letter_value_multiplier)
        word_value: int = 0
        #print(letter_values)
        for value in letter_values:
            word_value += value
        #print(
        #    f"original word value of word {''.join(word_formed_letters)} is {word_value}, multiplied value is {word_value * (2**double_word_counter) * (3**triple_word_counter)}"
        #)
        word_value = word_value * (2**double_word_counter) * (3**triple_word_counter)
        return (''.join(word_formed_letters), word_value)
>>>>>>> Stashed changes

    def finalize_set_tiles(self, tile_coordinates_list: list[tuple[int, int]]):
        tile_object: BoardTile
        coordinate_set: tuple[int, int]
        for coordinate_set in tile_coordinates_list:
            if isinstance(coordinate_set, tuple):
                tile_object = self.game_board[str(coordinate_set[0])][
                    str(coordinate_set[1])
                ]["tile_object"]
                tile_object.tile_type = "Set_board/Base_tilerow"
        # Globals.global_should_recompute = True

    def player_try_word(
        self, tile_coordinates_list: list[tuple[int, int]]
    ) -> tuple[
        bool, int
    ]:  # returns whether try works or fails, and the score (score is 0 when fail)
        if len(tile_coordinates_list) == 0:
            print("no tiles submitted")
            return (False, 0)
        if self._is_first_turn:
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
            if isinstance(tile, tuple):
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
<<<<<<< Updated upstream
=======
        #print(tile_coordinates_list)
>>>>>>> Stashed changes
        if len(tile_coordinates_list) == 7:
            total_value += 40  # 7 tiles laid on board, so add 40 points
        self.finalize_set_tiles(tile_coordinates_list)
        self._is_first_turn = False
        return (True, total_value)

<<<<<<< Updated upstream
    # def get_word_value(self, tile_coordinate_list):
=======
    def bot_play_word(
        self, tile_coordinates_list: list[tuple[int, int]], letters_list: list[str]
    ):
        if len(tile_coordinates_list) == len(letters_list):
            for index in range(len(tile_coordinates_list)):
                tile_coordinate: tuple[int, int] = tile_coordinates_list[index]
                tile_letter: str = letters_list[index]
                #print(f"tile coordinate {tile_coordinate}; tile letter {tile_letter}")
                self.game_board[str(tile_coordinate[0])][str(tile_coordinate[1])][
                    "letter"
                ] = tile_letter
                tile_object: BoardTile = self.game_board[str(tile_coordinate[0])][
                    str(tile_coordinate[1])
                ]["tile_object"]
                tile_object.letter = tile_letter
                tile_object.tile_type = "Set_board/Base_tilerow"
                time.sleep(0.5)
>>>>>>> Stashed changes

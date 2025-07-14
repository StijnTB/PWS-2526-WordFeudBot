import pygame
from tileclass import *
from globals import Globals, screen, game_display

pygame.init()


class Board:
    def __init__(self, original_board_layout: list) -> None:
        self._original_board_layout: list = original_board_layout

        self._should_recompute = True
        self._game_board: dict = {}
        self._try_game_board: dict
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

    def reset_board(self) -> None:
        self.__init__(Globals.BOARD_LAYOUT_LIST)

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
            return True
        else:
            return False

    def get_tile_object(self, tile_coordinates: tuple[int, int]) -> BoardTile:
        return self._game_board[str(tile_coordinates[0])][str(tile_coordinates[1])][
            "tile_object"
        ]

    def reset_tile(self, clicked_tile_coordinates: tuple[int, int]):
        original_tile_type: str = (
            Globals.BOARD_LAYOUT_LIST[clicked_tile_coordinates[0]][
                clicked_tile_coordinates[1]
            ]
            if Globals.BOARD_LAYOUT_LIST[clicked_tile_coordinates[0]][
                clicked_tile_coordinates[1]
            ]
            != None
            else "Empty_tile"
        )
        tile_object: BoardTile = self.get_tile_object(clicked_tile_coordinates)
        tile_object._letter = ""
        tile_object.tile_type = original_tile_type

    @property
    def game_board(self) -> dict:
        return self._game_board

    def get_played_word(self, tiles: list) -> dict:
        starting_tile_coordinates: tuple = (15, 15)
        ending_tile_coordinates: tuple = (0, 0)
        tile: BoardTile
        for tile in tiles:
            if tile._board_coordinates <= starting_tile_coordinates:
                starting_tile_coordinates = tile._board_coordinates
            if tile._board_coordinates >= ending_tile_coordinates:
                ending_tile_coordinates = tile._board_coordinates
        direction: tuple = (0, 0)
        if starting_tile_coordinates[0] < ending_tile_coordinates[0]:
            direction = (1, 0)
        if starting_tile_coordinates[1] < ending_tile_coordinates[1]:
            direction = (0, 1) if direction == (0, 0) else (1, 1)

        if direction == (1, 1) or direction == (0, 0):
            return {
                "word": "",
                "tiles": [],
            }  # either both the y and x differ between the start and end of the word, or there has occured a glitch

        played_word: str = ""
        played_word_tile_object_list: list = []
        if direction == (0, 1):
            for tile_row in range(
                starting_tile_coordinates[0], ending_tile_coordinates[0] + 1
            ):
                played_word += self._try_game_board[tile_row][
                    starting_tile_coordinates[1]
                ]["letter"]
                played_word_tile_object_list.append(
                    self._try_game_board[tile_row][starting_tile_coordinates[1]][
                        "tile_object"
                    ]
                )
        elif direction == (1, 0):
            for tile_column in range(
                starting_tile_coordinates[1], ending_tile_coordinates[1] + 1
            ):
                played_word += self._try_game_board[starting_tile_coordinates[0]][
                    tile_column
                ]["letter"]
                played_word_tile_object_list.append(
                    self._try_game_board[starting_tile_coordinates[0]][tile_column][
                        "tile_object"
                    ]
                )
        return {"word": played_word, "tiles": played_word_tile_object_list}

    def play_word(self, tiles: list) -> None:
        word, word_tiles_list = self.get_played_word(tiles)

    def _direction_of_word(
        self, tiles: list
    ) -> tuple:  # tiles is a list of the tile objects which have a new letter
        tile: BoardTile
        row_set: set = set()
        column_set: set = set()

        for tile in tiles:
            row_set.add(tile._board_coordinates[0])
            column_set.add(tile._board_coordinates[1])

        if len(row_set) == 1 and len(column_set) >= 1:
            return (0, 1)
        elif len(row_set) >= 1 and len(column_set) == 1:
            return (1, 0)
        elif len(row_set) == 1 and len(column_set) == 1:
            return (1, 1)
        else:
            return (0, 0)

    def try_word(self, tiles: list) -> bool:
        if self._direction_of_word(tiles):
            tile: BoardTile
            for tile in tiles:
                board_coords: tuple = tile._board_coordinates
                # if self._game_board[board_coords[1]]
        dr, dc = self._direction_of_word(tiles)
        if (dr, dc) == (
            0,
            0,
        ):  # the word is either bugged (row has length 0 or column has length 0) or both sets are longer than 1
            return False
        return True

    def update(self) -> None:
        if self._should_recompute:
            screen.fill((0, 0, 0))
            for row in self._game_board:
                for column in self._game_board[row]:
                    tile_object: BoardTile = self._game_board[row][column][
                        "tile_object"
                    ]
                    tile_object.update()

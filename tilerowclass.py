from tileclass import *
from tilebagclass import TileBag
from globals import *
import random


class TileRow:
    def __init__(self, tilebag: TileBag):
        self._tile_list: list = tilebag.grab_letters(7)


class PlayerTileRow(TileRow):
    def __init__(self, tilebag: TileBag):
        super().__init__(tilebag)
        self._tile_row_objects: list[RowTile] = []
        self._tile_size = Globals.TILE_SIZE
        self._selected_tile_index: int = -1
        self._selected_letter: str = "None"
        self._test_tile_list: list = self._tile_list

        self._played_tile_list: list = (
            []
        )  # contains the rowtile data of tiles played in this turn
        self._board_set_tile_list: list = (
            []
        )  # contains the coordinates of tiles which are set in this turn
        for index, tile_letter in enumerate(self._tile_list):
            self._tile_row_objects.append(RowTile(letter=tile_letter, row_coords=index))

    def shuffle_row(self):
        random.shuffle(self._tile_list)
        tile_object: RowTile
        for index, tile_object in enumerate(self._tile_row_objects):
            tile_object.letter = self._tile_list[index]

    def check_tile_selected(self, tile_row_index: int):
        tile_object: RowTile = self._tile_row_objects[tile_row_index]
        if tile_object.tile_type == "Set_board/Base_tilerow":
            tile_object.tile_type = "Try_board/Selected_tilerow"
        elif tile_object.tile_type == "Try_board/Selected_tilerow":
            tile_object.tile_type = "Set_board/Base_tilerow"

    def get_clicked_tile_index(self, mouse_coordinates: tuple[int, int]):
        mouse_x = mouse_coordinates[0]
        selected_tile_index = 0
        for index in range(0, len(self._tile_list)):
            if index < len(self._tile_list):
                if (
                    (self._tile_size + Globals._border_between_tiles_width) * index
                    <= mouse_x
                    < (self._tile_size + Globals._border_between_tiles_width)
                    * (index + 1)
                ):
                    selected_tile_index = index
        return selected_tile_index

    def change_selected_tile(self, mouse_coordinates: tuple[int, int]):
        new_selected_tile_index = self.get_clicked_tile_index(mouse_coordinates)
        if (
            new_selected_tile_index == self._selected_tile_index
        ):  # clicked tile is selected tile, so deselect
            self.check_tile_selected(new_selected_tile_index)
            self._selected_tile_index = -1
            self.selected_letter = "None"
        elif (
            self._selected_tile_index == -1
        ):  # no tile is currently selected, select new tile
            self.check_tile_selected(new_selected_tile_index)
            self._selected_tile_index = new_selected_tile_index
            self.selected_letter = self._tile_list[self.selected_tile_index]
        else:  # there is a tile selected and you click a different one, deselect original tile and select new tile
            self.check_tile_selected(self._selected_tile_index)
            self.check_tile_selected(new_selected_tile_index)
            self._selected_tile_index = new_selected_tile_index
            self.selected_letter = self._tile_list[self.selected_tile_index]

    def hide_selected_tile(self, clicked_board_tile_coordinates: tuple[int, int]):
        selected_tile: RowTile = self._tile_row_objects[self.selected_tile_index]
        self.check_tile_selected(self.selected_tile_index)
        selected_tile.tile_type = "Played_tilerow_letter"
        self._selected_tile_index = -1
        self._played_tile_list.append(selected_tile)
        self._board_set_tile_list.append(clicked_board_tile_coordinates)

    def return_clicked_tile(self, letter: str, uncheck: bool):
        if uncheck:
            self.check_tile_selected(self.selected_tile_index)
        index: int
        tile_object: RowTile
        for index in range(0, len(self._tile_row_objects)):
            tile_object = self._tile_row_objects[index]
            if (
                tile_object.letter == letter
                and tile_object.tile_type == "Played_tilerow_letter"
            ):
                tile_object.tile_type = "Try_board/Selected_tilerow"
                self.selected_tile_index = index
                break

    @property
    def selected_tile_index(self) -> int:
        return self._selected_tile_index

    @selected_tile_index.setter
    def selected_tile_index(self, new_tile_index: int):
        self._selected_tile_index = new_tile_index

    @property
    def selected_letter(self) -> str:
        return self._selected_letter

    @selected_letter.setter
    def selected_letter(self, new_letter: str):
        self._selected_letter = new_letter


class BotTileRow(TileRow):
    def __init__(self, tilebag: TileBag):
        super().__init__(tilebag)

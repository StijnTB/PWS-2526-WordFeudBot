from tileclass import *
from tilebagclass import TileBag
from globals import *
import random
random.seed(Globals.random_seed)

class TileRow:
    def __init__(self, tilebag: TileBag):
        self._tilebag: TileBag = tilebag
        self._tile_list: list[str] = tilebag.grab_letters(7)

    def get_remaining_points(self) -> int:
        remaining_points: int = 0
        for letter in self._tile_list:
            if letter != "":
                remaining_points += Globals.TILE_LETTER_DICT[letter]["value"]
        return remaining_points


class PlayerTileRow(TileRow):
    def __init__(self, tilebag: TileBag):
        super().__init__(tilebag)
        self._tile_row_objects: list[RowTile] = []
        self._tile_size: int = Globals.TILE_SIZE
        self._selected_tile_index: int = -1
        self._selected_letter: str = "None"
        self._played_tile_list: list[RowTile] = (
            []
        )  # contains the rowtile data of tiles played in this turn
        self._board_set_tile_list: list[tuple[int, int]] = (
            []
        )  # contains the coordinates of tiles which are set in this turn
        for index, tile_letter in enumerate(self._tile_list):
            self._tile_row_objects.append(RowTile(letter=tile_letter, row_coords=index))
        Globals.global_should_recompute = True
        self.update()

    def swap_letters(self, list_of_swapped_indexes: list[int]):
        letters_to_return: list[str] = []
        for index in list_of_swapped_indexes:
            letter = self._tile_list[index]
            letters_to_return.append(letter)
        for letter in letters_to_return:
            self._tile_list.remove(letter)
        if len(letters_to_return) > 0:
            new_letters = self._tilebag.swap_letters(letters_to_return)
            self._tile_list.extend(new_letters)
            self.reload_tiles()

    def reload_tiles(self) -> None:
        for index in range(len(self._tile_list)):
            tile_object: RowTile = self._tile_row_objects[index]
            tile_object.letter = self._tile_list[index]

    def shuffle_row(self):
        shuffleable_row_list: list = self._tile_list.copy()
        tile_object: RowTile
        unshufflable_index_list: list = []
        for tile_object in self._played_tile_list:
            shuffleable_row_list.remove(tile_object.letter)
            unshufflable_index_list.append(tile_object._row_coordinate)
        random.shuffle(shuffleable_row_list)
        current_index_shuffled_list: int = 0
        for index in range(len(self._tile_list)):
            if index not in unshufflable_index_list:
                self._tile_list[index] = shuffleable_row_list[
                    current_index_shuffled_list
                ]
                current_index_shuffled_list += 1
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
        self.selected_letter = "None"
        self._played_tile_list.append(selected_tile)
        self._board_set_tile_list.append(clicked_board_tile_coordinates)

    def return_full_tilerow(self):
        for tile_object in self._played_tile_list:
            tile_object.tile_type = "Set_board/Base_tilerow"
        self._played_tile_list.clear()

    def return_clicked_tile(
        self,
        letter: str,
        uncheck: bool,
        board_tile_coordinates: tuple[int, int],
        tile_is_blank: bool,
    ):
        if uncheck:
            self.check_tile_selected(self.selected_tile_index)
        index: int
        tile_object: RowTile
        for index in range(0, len(self._tile_row_objects)):
            tile_object = self._tile_row_objects[index]
            if tile_is_blank:
                letter = " "
            if (
                tile_object.letter == letter
                and tile_object.tile_type == "Played_tilerow_letter"
            ):
                tile_object.tile_type = "Set_board/Base_tilerow"
                self.selected_tile_index = -1
                self.selected_letter = "None"
                self._played_tile_list.remove(tile_object)
                self._board_set_tile_list.remove(board_tile_coordinates)
                break

    def get_new_letters(self):
        if len(self._played_tile_list) <= len(self._tilebag._bag_list):
            for tile in self._played_tile_list:
                tile.letter = self._tilebag.grab_letters(1)[0]
                tile.tile_type = "Set_board/Base_tilerow"
                self._tile_list[tile._row_coordinate] = tile.letter
        else:  # less than the played amount of tiles are in the bag
            for tile in self._played_tile_list:
                if len(self._tilebag._bag_list) >= 1:
                    tile.letter = self._tilebag.grab_letters(1)[0]
                    tile.tile_type = "Set_board/Base_tilerow"
                    self._tile_list[tile._row_coordinate] = tile.letter
                elif len(self._tilebag._bag_list) == 0:
                    tile.tile_type = "Empty_tile"
                    tile.letter = ""
                    self._tile_list[tile._row_coordinate] = tile.letter
        self._board_set_tile_list.clear()
        self._played_tile_list.clear()

    def update(self) -> None:
        for tile in self._tile_row_objects:
            tile.update()

    @property
    def selected_tile_index(self) -> int:
        return self._selected_tile_index

    @selected_tile_index.setter
    def selected_tile_index(self, new_tile_index: int):
        self._selected_tile_index = new_tile_index
        # Globals.global_should_recompute = True

    @property
    def selected_letter(self) -> str:
        return self._selected_letter

    @selected_letter.setter
    def selected_letter(self, new_letter: str):
        self._selected_letter = new_letter
        # Globals.global_should_recompute = True


class BotTileRow(TileRow):
    def __init__(self, tilebag: TileBag):
        super().__init__(tilebag)
        self._max_grabbable_amount_from_tilebag: int = 7

    def get_new_letters(self, letters_to_replace: list[str]) -> None:
        old_tile_list = self._tile_list.copy()
        try:
            for letter in letters_to_replace:
                print(f"letter: {letter}; tile list: {self._tile_list}")
                if letter in self._tile_list:
                    self._tile_list.remove(letter)
                else:
                    if " " in self._tile_list:
                        self._tile_list.remove(" ")
                    else:
                        raise ValueError()
            if len(self._tilebag._bag_list) == 0:
                pass
            elif len(self._tilebag._bag_list) >= len(letters_to_replace):
                self._tile_list.extend(
                    self._tilebag.grab_letters(len(letters_to_replace))
                )
            elif len(self._tilebag._bag_list) < len(letters_to_replace):
                self._tile_list.extend(
                    self._tilebag.grab_letters(len(self._tilebag._bag_list))
                )
        except Exception as e:
            print(e)
            print(
                f"letters to replace {letters_to_replace}; tile list {old_tile_list}; changed tile list {self._tile_list}"
            )

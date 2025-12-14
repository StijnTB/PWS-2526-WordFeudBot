from pygame import mouse, event, display, quit, QUIT, MOUSEBUTTONDOWN

from boardclass import Board
from globals import Globals, screen
from sidebar import SideBar, BaseButton
from tilebagclass import TileBag
from tileclass import BoardTile
from tilerowclass import PlayerTileRow


class Player:
    def __init__(
        self,
        tilebag: TileBag,
        board: Board,
    ):
        self._game_board: Board = board
        self._tilebag: TileBag = tilebag
        self._sidebar: SideBar = SideBar()
        self._tilerow: PlayerTileRow = PlayerTileRow(self._tilebag)
        self._is_turn: bool = True
        self._turn_state: str = "Base"  # "Base" is placing tiles board, "Swap" is
        self._exit: bool = (
            False  # when True, player wants to exit, which sends message to main loop in basegame to stop loop
        )
        self.update()

    def play(self):
        print("player turn")
        self._is_turn: bool = True
        self._screen_should_recompute: bool = False
        while self._is_turn:
            if self._exit:
                break
            self.update()
            mouse_coordinates = mouse.get_pos()
            self._sidebar.recalculate_button_highlights(mouse_coordinates)
            for _event in event.get():
                if _event.type == QUIT:
                    quit()
                    self._exit = True
                    break
                else:
                    if _event.type == MOUSEBUTTONDOWN:
                        if self._turn_state == "Base":
                            if (
                                Globals.ROW_TILES_SCREEN_HEIGHT - Globals.TILE_SIZE / 2
                            ) <= mouse_coordinates[1] <= (
                                Globals.ROW_TILES_SCREEN_HEIGHT + Globals.TILE_SIZE / 2
                            ) and (
                                0
                                <= mouse_coordinates[0]
                                <= (
                                    Globals.TILE_SIZE * len(self._tilerow.tile_list)
                                    + (len(self._tilerow.tile_list) - 1)
                                    * Globals.BORDER_BETWEEN_TILES_WIDTH
                                )
                            ):  # mouse is in area of TileRow
                                self._tilerow.change_selected_tile(mouse_coordinates)
                            elif (
                                Globals.SCREEN_TILES_STARTING_HEIGHT
                                <= mouse_coordinates[1]
                                <= (
                                    Globals.SCREEN_TILES_STARTING_HEIGHT
                                    + Globals.TILE_SIZE * 15
                                    + Globals.BORDER_BETWEEN_TILES_WIDTH * 14
                                )
                                and 0
                                <= mouse_coordinates[0]
                                <= (
                                    Globals.TILE_SIZE * 15
                                    + Globals.BORDER_BETWEEN_TILES_WIDTH * 14
                                )
                            ):  # mouse is in area of Board
                                clicked_tile_coordinates: tuple[int, int] = (
                                    self._game_board.get_clicked_tile_coordinates(
                                        mouse_coordinates
                                    )
                                )
                                if self._tilerow.selected_tile_index != -1:
                                    assignment_worked: bool = (
                                        self._game_board.set_letter_to_tile(
                                            self._tilerow.selected_letter,
                                            clicked_tile_coordinates,
                                        )
                                    )
                                    if assignment_worked:
                                        self._tilerow.hide_selected_tile(
                                            clicked_tile_coordinates
                                        )
                                    else:
                                        clicked_board_tile: BoardTile = (
                                            self._game_board.get_tile_object(
                                                clicked_tile_coordinates
                                            )
                                        )
                                        if (
                                            clicked_board_tile.tile_type
                                            == "Try_board/Selected_tilerow"
                                        ):  # selected tile has a letter but is still in try type
                                            is_attempted_blank: bool = False
                                            if clicked_board_tile.is_attempt_blank:
                                                is_attempted_blank = True
                                            self._tilerow.return_clicked_tile(
                                                clicked_board_tile.letter,
                                                True,
                                                clicked_tile_coordinates,
                                                is_attempted_blank,
                                            )
                                            self._game_board.reset_tile(
                                                clicked_tile_coordinates
                                            )
                                elif self._tilerow.selected_tile_index == -1:
                                    clicked_board_tile: BoardTile = (
                                        self._game_board.get_tile_object(
                                            clicked_tile_coordinates
                                        )
                                    )
                                    if (
                                        clicked_board_tile.tile_type
                                        == "Try_board/Selected_tilerow"
                                    ):  # selected tile has a letter but is still in try type
                                        is_attempted_blank: bool = False
                                        if clicked_board_tile.is_attempt_blank:
                                            is_attempted_blank = True
                                        self._tilerow.return_clicked_tile(
                                            clicked_board_tile.letter,
                                            False,
                                            clicked_tile_coordinates,
                                            is_attempted_blank,
                                        )
                                        self._game_board.reset_tile(
                                            clicked_tile_coordinates
                                        )
                            elif (
                                self._sidebar.horizontal_range[0]
                                <= mouse_coordinates[0]
                                <= self._sidebar.horizontal_range[1]
                                and self._sidebar.vertical_range[0]
                                <= mouse_coordinates[1]
                                <= self._sidebar.vertical_range[1]
                            ):  # mouse is in area of button menu
                                clicked_button = self._sidebar.button_clicked(
                                    mouse_coordinates
                                )
                                if isinstance(clicked_button, BaseButton):
                                    match clicked_button.text:
                                        case "PLAY WORD":
                                            attempt_information = (
                                                self._game_board.player_try_word(
                                                    self._tilerow.board_set_tile_list
                                                )
                                            )
                                            attempt_success = attempt_information[0]
                                            if attempt_success:
                                                print("success")
                                                print(attempt_information[1])
                                                self._tilerow.get_new_letters()
                                                self._sidebar.score_object.player_score += attempt_information[
                                                    1
                                                ]
                                                self._is_turn = False
                                            else:
                                                print("failure")
                                        case "SHUFFLE":
                                            self._tilerow.shuffle_row()
                                        case "RETURN TILES":
                                            self._tilerow.return_full_tilerow()
                                            self._game_board.reset_tiles(
                                                self._tilerow.board_set_tile_list
                                            )
                                            self._tilerow.board_set_tile_list.clear()
                                        case "PASS TURN":
                                            self._tilerow.return_full_tilerow()
                                            self._game_board.reset_tiles(
                                                self._tilerow.board_set_tile_list
                                            )
                                            self._tilerow.board_set_tile_list.clear()
                                            self._is_turn = False
                                        case "SWAP LETTERS":
                                            if (
                                                self._tilebag.get_amount_of_letters_remaining()
                                                >= 7
                                            ):
                                                self._sidebar.switch_number_button_visibility()
                                                self._tilerow.return_full_tilerow()
                                                self._game_board.reset_tiles(
                                                    self._tilerow.board_set_tile_list
                                                )
                                                self._tilerow.board_set_tile_list.clear()
                                                self._turn_state = "Swap"
                                                self._is_turn = False
                                        case _:
                                            pass
                                else:
                                    pass
                        elif self._turn_state == "Swap":
                            return_value = self._sidebar.swap_state_button_clicked(
                                mouse_coordinates
                            )
                            if return_value == "Swap_letters":
                                print("swap letters")
                                swappable_indexes = (
                                    self._sidebar.button_set.get_swappable_indexes()
                                )
                                print(swappable_indexes)
                                self._turn_state = "Base"
                                self._tilerow.swap_letters(swappable_indexes)
                                self._sidebar.switch_number_button_visibility()
                                Globals.global_should_recompute = True
                                self._is_turn = False

                                # run function to swap letters on tilerow
                            elif return_value == "Swap_state_back":
                                print("go back")
                                self._sidebar.switch_number_button_visibility()
                                Globals.global_should_recompute = True
                                self._turn_state = "Base"

                    display.flip()  # Update display

    def update(self) -> None:
        if (
            Globals.global_should_recompute
        ):  # only use Globals.global_should_recompute when full recomputation, otherwise use recompute on individual items for better performance
            print("call update")
            screen.fill("Black")
            self._game_board.update()
            self._sidebar.update()
            self._tilerow.update()
            Globals.global_should_recompute = False

    @property
    def tilerow(self) -> PlayerTileRow:
        return self._tilerow

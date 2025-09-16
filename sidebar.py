import pygame
from globals import Globals, screen
from utils import *
from pygame import Rect

pygame.init()


class BaseButton:
    def __init__(
        self,
        screen_coordinates: tuple[int, int],
        text: str,
        dimensions: tuple[int, int],
        hidden: bool = False,
    ):
        self._coordinates: tuple[int, int] = screen_coordinates
        self._text: str = text
        self._dimensions: tuple[int, int] = dimensions

        self._button_horizontal_range: tuple[int, int] = (
            int(self._coordinates[0] - self._dimensions[0] / 2),
            int(self._coordinates[0] + self._dimensions[0] / 2),
        )
        self._button_vertical_range: tuple[int, int] = (
            int(self._coordinates[1] - self._dimensions[1] / 2),
            int(self._coordinates[1] + self._dimensions[1] / 2),
        )
        self._highlighted: bool = False  # true when you hover over a button
        self._base_tile_shape: Rect = Rect(
            int(self._coordinates[0] - self._dimensions[0] / 2),
            int(self._coordinates[1] - self._dimensions[1] / 2),
            self._dimensions[0],
            self._dimensions[1],
        )
        self._hidden: bool = hidden
        self._tile_indexes_selected_list: list[int] = []
        self._pygame_font = pygame.font.Font(
            "GothamBlack.ttf", int(Globals.TEXT_SIZE_TILE * 3 / 4)
        )
        self._letter_image = self._pygame_font.render(self.text, True, "Black")
        self._highest_letter_height: int = 0
        self._text_width: int = 0
        for letter_used in self._text:
            letter_width, letter_height = self._pygame_font.size(letter_used)
            self._text_width += letter_width
            if letter_height > self._highest_letter_height:
                self._highest_letter_height = letter_height
        self._text_coordinates: tuple = (
            self._coordinates[0] - floor(self._text_width / 2),
            self._coordinates[1] - floor(self._highest_letter_height / 2),
        )
        Globals.global_should_recompute = True
        self.update()

    def update(self) -> None:
        if not self.hidden:
            self._background_rect: Rect = pygame.draw.rect(
                pygame.display.get_surface(),
                (
                    Globals.TILE_COLOR_DICT["Set_board/Base_tilerow"]
                    if not self.highlighted
                    else Globals.TILE_COLOR_DICT["Try_board/Selected_tilerow"]
                ),
                self._base_tile_shape,
                0,
                int(self._dimensions[1] / 4),
            )
            screen.blit(self._letter_image, self._text_coordinates)

    @property
    def vertical_range(self) -> tuple[int, int]:
        return self._button_vertical_range

    @property
    def horizontal_range(self) -> tuple[int, int]:
        return self._button_horizontal_range

    @property
    def highlighted(self) -> bool:
        return self._highlighted

    @highlighted.setter
    def highlighted(self, new_highlight: bool) -> None:
        self._highlighted = new_highlight
        # Globals.global_should_recompute = True
        self.update()

    @property
    def hidden(self) -> bool:
        return self._hidden

    @hidden.setter
    def hidden(self, new_hidden_state: bool) -> None:
        self._hidden = new_hidden_state
        # Globals.global_should_recompute = True
        self.update()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        self._text = new_text
        # Globals.global_should_recompute = True
        self.update()


class NumberButton(BaseButton):
    def __init__(self, number: int, top_left_coordinate: tuple[int, int]):
        left_x_coordinate: int = top_left_coordinate[0]
        top_y_coordinate: int = top_left_coordinate[1]
        super().__init__(
            (
                left_x_coordinate
                + int((Globals.BUTTON_SIZE[0] - 8) / 10)
                + int(
                    (Globals.BUTTON_SIZE[0] - 8)
                    * (number - 1 if number - 1 in [0, 1, 2, 3, 4] else number - 6)
                    / 5
                )
                + Globals._border_between_tiles_width
                * (number - 1 if number - 1 in [0, 1, 2, 3, 4] else number - 6),
                top_y_coordinate
                + int((Globals.BUTTON_SIZE[0] - 8) / 10)
                * (1 if number - 1 in [0, 1, 2, 3, 4] else 3)
                + Globals._border_between_tiles_width
                * (1 if number - 1 in [0, 1, 2, 3, 4] else 2),
                # + Globals._border_between_tiles_width * (number - 1 if number - 1 in []),
            ),
            str(number),
            (
                int((Globals.BUTTON_SIZE[0] - 8) / 5),
                int((Globals.BUTTON_SIZE[0] - 8) / 5),
            ),
            hidden=True,
        )


class Scores:
    def __init__(self):
        self._x: int = (
            Globals.TILE_SIZE * 15
            + Globals._border_between_tiles_width * 14
            + Globals._offset_between_screen_categories
            + int(Globals.BUTTON_SIZE[0] / 2)
        )
        self._text_starting_x: int = int(self._x - Globals.BUTTON_SIZE[0] / 2) + int(
            Globals.BUTTON_SIZE[1] / 4
        )
        self._player_score: int = 0
        self._bot_score: int = 0
        self._background_height: int = int(Globals.BUTTON_SIZE[1] * 1.5)
        self._base_tile_shape: Rect = Rect(
            int(self._x - Globals.BUTTON_SIZE[0] / 2),
            0,
            Globals.BUTTON_SIZE[0],
            self._background_height,
        )
        self._background_rect: Rect = pygame.draw.rect(
            pygame.display.get_surface(),  # surface
            Globals.TILE_COLOR_DICT["Try_board/Selected_tilerow"],  # color
            self._base_tile_shape,  # base rect
            0,  # line width
            int(Globals.BUTTON_SIZE[1] / 4),  # corner radius
        )
        self._pygame_font: pygame.font.Font = pygame.font.Font(
            "GothamBlack.ttf", int(Globals.TEXT_SIZE_TILE * 3 / 4)
        )
        self._player_image = self._pygame_font.render("PLAYER", True, "Black")
        self._bot_image = self._pygame_font.render("BOT", True, "Black")
        self._player_image_coordinates: tuple[int, int] = (
            self._text_starting_x,
            int(Globals.BUTTON_SIZE[1] / 4),
        )
        self._bot_image_coordinates: tuple[int, int] = (
            self._text_starting_x,
            int(
                self._background_height
                - Globals.BUTTON_SIZE[1] / 4
                - calculate_text_dimensions(self._pygame_font, "BOT")[1]
            ),
        )
        self.update()

    def update(self):

        self._background_rect: Rect = pygame.draw.rect(
            pygame.display.get_surface(),  # surface
            Globals.TILE_COLOR_DICT["Try_board/Selected_tilerow"],  # color
            self._base_tile_shape,  # base rect
            0,  # line width
            int(Globals.BUTTON_SIZE[1] / 4),  # corner radius
        )
        self._player_score_image = self._pygame_font.render(
            str(self.player_score), True, "Black"
        )
        self._bot_score_image = self._pygame_font.render(
            str(self.bot_score), True, "Black"
        )
        self._player_score_image_coordinates: tuple[int, int] = (
            Globals.SCREEN_WIDTH
            - int(Globals.BUTTON_SIZE[1] / 4)
            - calculate_text_dimensions(self._pygame_font, str(self.player_score))[0],
            int(Globals.BUTTON_SIZE[1] / 4),
        )
        self._bot_score_image_coordinates: tuple[int, int] = (
            Globals.SCREEN_WIDTH
            - int(Globals.BUTTON_SIZE[1] / 4)
            - calculate_text_dimensions(self._pygame_font, str(self.bot_score))[0],
            int(
                self._background_height
                - Globals.BUTTON_SIZE[1] / 4
                - calculate_text_dimensions(self._pygame_font, "BOT")[1]
            ),
        )
        screen.blit(self._player_image, self._player_image_coordinates)
        screen.blit(self._bot_image, self._bot_image_coordinates)
        screen.blit(self._player_score_image, self._player_score_image_coordinates)
        screen.blit(self._bot_score_image, self._bot_score_image_coordinates)

    @property
    def player_score(self) -> int:
        return self._player_score

    @player_score.setter
    def player_score(self, new_score: int) -> None:
        if new_score > 0:
            self._player_score = new_score
        elif new_score <= 0:
            self._player_score = 0
        self.update()

    @property
    def bot_score(self) -> int:
        return self._bot_score

    @bot_score.setter
    def bot_score(self, new_score: int) -> None:
        if new_score > 0:
            self._bot_score = new_score
        elif new_score <= 0:
            self._bot_score = 0
        self.update()


class SideBar:
    def __init__(self):
        self._score_object: Scores = Scores()
        self._button_set: ButtonSet = ButtonSet()
        max_vertical_coordinate: int = self._score_object._background_height
        button: BaseButton
        for button in self._button_set._button_list:
            max_vertical_coordinate += button._dimensions[1]
        max_vertical_coordinate += 4 * Globals._border_between_tiles_width
        self._horizontal_range: tuple[int, int] = (
            Globals.SCREEN_WIDTH - Globals.BUTTON_SIZE[0],
            Globals.SCREEN_WIDTH,
        )
        self._vertical_range: tuple[int, int] = (
            self._score_object._background_height,
            max_vertical_coordinate,
        )
        Globals.global_should_recompute = True
        self.update()

    def recalculate_button_highlights(self, mouse_coordinates: tuple[int, int]) -> None:
        self._button_set.calculate_button_highlights(mouse_coordinates)

    def switch_number_button_visibility(self):
        self._button_set.switch_visibility_number_buttons()

    def button_clicked(self, mouse_coordinates: tuple[int, int]) -> BaseButton | None:
        button: BaseButton
        for button in self._button_set._button_list:
            if (
                button.horizontal_range[0]
                <= mouse_coordinates[0]
                <= button.horizontal_range[1]
                and button.vertical_range[0]
                <= mouse_coordinates[1]
                <= button.vertical_range[1]
            ):  # mouse is in range, so button is selected
                print(button.text)
                return button
        return None

    def swap_state_button_clicked(self, mouse_coordinates: tuple[int, int]):
        return_button: BaseButton = self._button_set._pass_turn_swap_button
        if (
            return_button.horizontal_range[0]
            <= mouse_coordinates[0]
            <= return_button.horizontal_range[1]
            and return_button.vertical_range[0]
            <= mouse_coordinates[1]
            <= return_button.vertical_range[1]
        ):
            self.switch_number_button_visibility()
            print("swap visibility")
            Globals.global_should_recompute = True
            return "Swap_state_back"
        else:
            for button in self._button_set._number_buttons_dict.values():
                if (
                    button.horizontal_range[0]
                    <= mouse_coordinates[0]
                    <= button.horizontal_range[1]
                    and button.vertical_range[0]
                    <= mouse_coordinates[1]
                    <= button.vertical_range[1]
                ):
                    button.highlighted = True if not button.highlighted else False
                    if button.text == "SWAP":
                        Globals.global_should_recompute = True
                        return "Swap_letters"

    def number_button_clicked(self, mouse_coordinates: tuple[int, int]):
        for button in self._button_set._number_buttons_dict.values():
            if (
                button.horizontal_range[0]
                <= mouse_coordinates[0]
                <= button.horizontal_range[1]
                and button.vertical_range[0]
                <= mouse_coordinates[1]
                <= button.vertical_range[1]
            ):
                button.highlighted = True if not button.highlighted else False

    def update(self) -> None:
        self._score_object.update()
        self._button_set.update()


class ButtonSet:
    def __init__(self):
        left_x_coordinate: int = Globals.SCREEN_WIDTH - Globals.BUTTON_SIZE[0]
        # buttons: play word, shuffle board, return all letters to row pass turn, pass turn with letter swap
        self._play_word_button: BaseButton = BaseButton(
            (
                left_x_coordinate + int(Globals.BUTTON_SIZE[0] / 2),
                int(Globals.BUTTON_SIZE[1] * 1.5 + Globals.BUTTON_SIZE[1] / 2)
                + Globals._border_between_tiles_width,
            ),
            "PLAY WORD",
            Globals.BUTTON_SIZE,
        )
        self._shuffle_board_button: BaseButton = BaseButton(
            (
                left_x_coordinate + int(Globals.BUTTON_SIZE[0] / 2),
                self._play_word_button._coordinates[1]
                + Globals.BUTTON_SIZE[1]
                + Globals._border_between_tiles_width,
            ),
            "SHUFFLE",
            Globals.BUTTON_SIZE,
        )
        self._return_tiles_to_row_button: BaseButton = BaseButton(
            (
                left_x_coordinate + int(Globals.BUTTON_SIZE[0] / 2),
                self._shuffle_board_button._coordinates[1]
                + Globals.BUTTON_SIZE[1]
                + Globals._border_between_tiles_width,
            ),
            "RETURN TILES",
            Globals.BUTTON_SIZE,
        )
        self._pass_turn_button: BaseButton = BaseButton(
            (
                left_x_coordinate + int(Globals.BUTTON_SIZE[0] / 2),
                self._return_tiles_to_row_button._coordinates[1]
                + Globals.BUTTON_SIZE[1]
                + Globals._border_between_tiles_width,
            ),
            "PASS TURN",
            Globals.BUTTON_SIZE,
        )
        self._pass_turn_swap_button: BaseButton = BaseButton(
            (
                left_x_coordinate + int(Globals.BUTTON_SIZE[0] / 2),
                self._pass_turn_button._coordinates[1]
                + Globals.BUTTON_SIZE[1]
                + Globals._border_between_tiles_width,
            ),
            "SWAP LETTERS",
            Globals.BUTTON_SIZE,
        )
        self._number_buttons_dict: dict[str, NumberButton] = {}
        for number in range(0, 7):
            number_button: NumberButton = NumberButton(
                number + 1,
                (
                    left_x_coordinate,
                    self._pass_turn_swap_button._coordinates[1]
                    + int(Globals.BUTTON_SIZE[1] / 2),
                ),
            )
            self._number_buttons_dict[str(number)] = number_button
        self._run_swap_letters_button: BaseButton = BaseButton(
            (
                left_x_coordinate
                + int((Globals.BUTTON_SIZE[0] - 8) / 5) * 2
                + Globals._border_between_tiles_width * 2
                + int(
                    (
                        Globals.BUTTON_SIZE[0]
                        - int((Globals.BUTTON_SIZE[0] - 8) / 5) * 2
                        - Globals._border_between_tiles_width * 2
                    )
                    / 2
                ),
                self._number_buttons_dict["6"]._coordinates[1],
            ),
            "SWAP",
            (
                (
                    Globals.BUTTON_SIZE[0]
                    - int((Globals.BUTTON_SIZE[0] - 8) / 5) * 2
                    - Globals._border_between_tiles_width * 2
                ),
                int((Globals.BUTTON_SIZE[0] - 8) / 5),
            ),
            hidden=True,
        )

        print(
            self._run_swap_letters_button._dimensions,
            self._run_swap_letters_button._coordinates[0] - left_x_coordinate,
        )
        self._number_buttons_dict["SWAP"] = self._run_swap_letters_button
        self._button_list: list[BaseButton] = [
            self._play_word_button,
            self._shuffle_board_button,
            self._return_tiles_to_row_button,
            self._pass_turn_button,
            self._pass_turn_swap_button,
        ]
        self.update()

    def switch_visibility_number_buttons(self):
        new_state: bool = (
            True if self._number_buttons_dict["0"].hidden == False else False
        )
        for number_button in self._number_buttons_dict.values():
            number_button.highlighted = False
            number_button.hidden = new_state
        # self._run_swap_letters_button.hidden = new_state

    def get_swappable_indexes(self) -> list[int]:
        swappable_indexes_list: list[int] = []
        for button in self._number_buttons_dict:
            if button != "SWAP":
                if self._number_buttons_dict[button].highlighted:
                    swappable_indexes_list.append(int(button))
        return swappable_indexes_list

    def calculate_button_highlights(
        self, mouse_coordinates: tuple[int, int]
    ) -> (
        None
    ):  # checks whether a button should be highlighted due to the mouse hovering over it
        for button in self._button_list:
            if (
                button.horizontal_range[0]
                <= mouse_coordinates[0]
                <= button.horizontal_range[1]
                and button.vertical_range[0]
                <= mouse_coordinates[1]
                <= button.vertical_range[1]
            ):  # mouse is in range, so button is highlighted
                if not button.highlighted:
                    button.highlighted = True
            else:
                if button.highlighted:
                    button.highlighted = False

    def update(self) -> None:
        for button in self._button_list:
            button.update()
        for button in self._number_buttons_dict.values():
            button.update()

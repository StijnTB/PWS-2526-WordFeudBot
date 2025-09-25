import pygame
from pygame import Rect, Color
from globals import Globals, screen
from utils import *

pygame.init()


class BaseTile:
    def __init__(
        self,
        tile_size: int = Globals.TILE_SIZE,
        letter: str = "",
        tile_type: str = "Empty_board_tilerow",
        x: int = 0,
        y: int = 0,
    ) -> None:
        self._tile_size: int = tile_size
        self._letter: str = letter
        self._tile_value: int = 0
        self._tile_type = tile_type
        self._x: int = x
        self._y: int = y
        self._tile_color: Color = Globals.TILE_COLOR_DICT[self._tile_type]
        self._base_tile_shape: Rect = Rect(
            int(self._x - self._tile_size / 2),
            int(self._y - self._tile_size / 2),
            self._tile_size,
            self._tile_size,
        )
        self._background_rect: Rect = pygame.draw.rect(
            pygame.display.get_surface(),
            self._tile_color,
            self._base_tile_shape,
            0,
            int(self._tile_size / 4),
        )
        self._is_attempt_blank: bool = False
        # Globals.global_should_recompute = True
        self.update()

    def update(self) -> None:
        self.decide_tile_color()
        self._background_rect = pygame.draw.rect(
            pygame.display.get_surface(),
            self._tile_color,
            self._base_tile_shape,
            0,
            int(self._tile_size / 4),
        )
        self.recalculate_letters()
        screen.blit(self._letter_image, self._text_coordinates)
        self._pygame_font = pygame.font.Font("PWS-2526-WordFeudBot-testing-required-by-Joram\GothamBlack.ttf", Globals.TEXT_SIZE_TILE)
        self._letter_image = self._pygame_font.render(self.letter, True, "Black")
        screen.blit(self._letter_image, self._text_coordinates)
        if self.tile_type in (
            "Try_board/Selected_tilerow",
            "Set_board/Base_tilerow",
            "Played_tilerow_letter",
        ):
            self._letter_value_pygame_font = pygame.font.Font(
                "PWS-2526-WordFeudBot-testing-required-by-Joram\GothamBlack.ttf", ceil(Globals.TEXT_SIZE_TILE / 2)
            )
            if not self._is_attempt_blank:
                self._tile_value = Globals.TILE_LETTER_DICT[self._letter]["value"]
                self._tile_value_image = self._letter_value_pygame_font.render(
                    str(Globals.TILE_LETTER_DICT[self._letter]["value"]), True, "Black"
                )
            else:
                self._tile_value = 0
                self._tile_value_image = self._letter_value_pygame_font.render(
                    "0", True, "Black"
                )
            screen.blit(self._tile_value_image, (self._x + 7, self._y + 7))

    def recalculate_letters(self):
        self._pygame_font: pygame.font.Font = pygame.font.Font(
            "PWS-2526-WordFeudBot-testing-required-by-Joram\GothamBlack.ttf", Globals.TEXT_SIZE_TILE
        )
        self._letter_image: pygame.surface.Surface = self._pygame_font.render(
            self._letter, True, "Black"
        )
        self._highest_letter_height: int = 0
        self._text_width: int = 0
        for letter_used in self._letter:
            letter_width, letter_height = self._pygame_font.size(letter_used)
            self._text_width += letter_width
            if letter_height > self._highest_letter_height:
                self._highest_letter_height = letter_height
        self._text_coordinates: tuple = (
            self._x - floor(self._text_width / 2),
            self._y - floor(self._highest_letter_height / 2),
        )

    def decide_tile_color(self) -> None:
        self._tile_color = Color(Globals.TILE_COLOR_DICT[self._tile_type])

    @property
    def letter(self) -> str:
        return self._letter

    @letter.setter
    def letter(self, new_letter: str) -> None:
        if new_letter == " ":
            while new_letter not in alphabet_list:
                supposed_letter = input("input a single letter you want the tile to be")
                new_letter = supposed_letter.upper()
                self._is_attempt_blank = True
        self._letter = new_letter
        # Globals.global_should_recompute = True
        self.update()

    @property
    def tile_type(self) -> str:
        return self._tile_type

    @tile_type.setter
    def tile_type(self, new_tile_type: str) -> None:
        self._tile_type = new_tile_type
        # Globals.global_should_recompute = True
        self.update()


class RowTile(BaseTile):
    def __init__(
        self,
        tile_size: int = Globals.TILE_SIZE,
        letter: str = "",
        row_coords: int = 0,  # the location on the row, 0 is left and 6 is right
    ) -> None:
        self._tile_type: str = "Set_board/Base_tilerow"
        self._tile_size: int = tile_size
        self._letter: str = letter
        self._row_coordinate: int = row_coords
        self._x: int = (
            self._row_coordinate * Globals.TILE_SIZE
            + int(Globals.TILE_SIZE / 2)
            + self._row_coordinate * Globals._border_between_tiles_width
        )
        self._y: int = Globals.ROW_TILES_SCREEN_HEIGHT
        super().__init__(
            self._tile_size, self._letter, self._tile_type, self._x, self._y
        )
        # Globals.global_should_recompute = True
        self.update()

    def update(self) -> None:
        super().update()

    @property
    def letter(self) -> str:
        return self._letter

    @letter.setter
    def letter(self, new_letter: str):
        self._letter = new_letter
        # Globals.global_should_recompute = True
        self.update()


class BoardTile(BaseTile):
    def __init__(
        self,
        tile_size: int = Globals.TILE_SIZE,
        letter: str = "",
        tile_type: str = "Empty_tile",
        board_coords: tuple = (0, 0),
    ) -> None:
        self._used: bool = False
        self._tile_size: int = int(tile_size)
        self._letter: str = letter
        self._tile_type: str = tile_type
        self._board_coordinates: tuple = board_coords
        self._is_attempt_blank: bool = (
            False  # if true, the board tile is a try and contains a letter which is not su
        )
        self._x: int = int(
            self._board_coordinates[1] * self._tile_size
            + self._tile_size / 2
            + self._board_coordinates[1] * Globals._border_between_tiles_width
        )
        self._y: int = int(
            Globals.SCREEN_TILES_STARTING_HEIGHT
            + self._board_coordinates[0] * self._tile_size
            + self._tile_size / 2
            + self._board_coordinates[0] * Globals._border_between_tiles_width
        )
        super().__init__(
            self._tile_size, self._letter, self._tile_type, self._x, self._y
        )

        self.update()

    def update(self) -> None:
        super().update()

    @property
    def used(self) -> bool:
        return self._used

    @used.setter
    def used(self, new_used_state: bool) -> None:
        self._used = new_used_state
        self.update()

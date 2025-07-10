import pygame
from pygame import Rect, Color
from globals import Globals, screen
from utils import *
pygame.init()

class BaseTile():
    def __init__(
            self,
            tile_size: int = Globals.TILE_SIZE,
            letter: str = "",
            tile_type: str = "Base",
            x: int = 0,
            y: int = 0
    ):
        self._tile_size: int = tile_size
        self._letter: str = letter
        self._tile_type = tile_type
        self._x: int = x
        self._y: int = y
        self._tile_color: Color = Globals.TILE_COLOR_DICT[self._tile_type]
        self._base_tile_shape: Rect = Rect(
            int(self._x-self._tile_size/2), 
            int(self._y-self._tile_size/2), 
            self._tile_size, 
            self._tile_size
        )
        self._background_rect: Rect = pygame.draw.rect(
            pygame.display.get_surface(), 
            self._tile_color, 
            self._base_tile_shape,
            0,
            int(self._tile_size/4)
        )
        self._pygame_font: pygame.font.Font = pygame.font.Font("GothamBlack.ttf",Globals.TEXT_SIZE_TILE)
        self._letter_image: pygame.surface.Surface = self._pygame_font.render(self._letter, True, "Black")
        highest_letter_height: int = 0
        text_width: int = 0
        for letter_used in self._letter:
            letter_width, letter_height = self._pygame_font.size(letter_used)
            text_width += letter_width
            if letter_height > highest_letter_height: highest_letter_height = letter_height
        self._text_dimensions: tuple = (text_width, highest_letter_height)
        self._text_coordinates: tuple = (
            self._x-floor(text_width/2),
            self._y-floor(highest_letter_height/2)
        )
        screen.blit(self._letter_image, self._text_coordinates)
        self._should_recompute: bool = True
        self.update()

    def update(self):
        if self._should_recompute:
            self.decide_tile_color()
            self._background_rect = pygame.draw.rect(
                pygame.display.get_surface(),
                self._tile_color,
                self._base_tile_shape,
                0,
                int(self._tile_size/4)
            )
            self._pygame_font = pygame.font.Font("GothamBlack.ttf",Globals.TEXT_SIZE_TILE)
            self._letter_image = self._pygame_font.render(self.letter, True, "Black")
            screen.blit(self._letter_image, self._text_coordinates)
    @property
    def letter(self):
        return self._letter
    
    @letter.setter
    def letter(self, new_letter: str):
        self._letter = new_letter
        self._should_recompute = True

    def decide_tile_color(self):
        self._tile_color = Color(Globals.TILE_COLOR_DICT[self._tile_type])

class BoardTile(BaseTile):
    def __init__(
            self,
            tile_size: int = Globals.TILE_SIZE,
            letter: str = "",
            tile_type: str = "Base",
            board_coords: tuple = (0,0)
    ):
        self._tile_size: int = int(tile_size)
        self._letter: str = letter
        self._tile_type: str = tile_type
        self._board_coordinates: tuple = board_coords
        self._x: int = int(self._board_coordinates[1] * self._tile_size + self._tile_size/2)
        self._y: int = int(self._board_coordinates[0] * self._tile_size + self._tile_size/2)
        super().__init__(
            self._tile_size,self._letter,self._tile_type,self._x,self._y
            )
        self._pygame_font = pygame.font.Font("GothamBlack.ttf",Globals.TEXT_SIZE_TILE)
        self._letter_image = self._pygame_font.render(self._letter, True, "black")
        
        self._should_recompute: bool = True
        self.update()
    def update(self):
        if self._should_recompute:
            self.decide_tile_color()
            self._background_rect = pygame.draw.rect(
                pygame.display.get_surface(),
                self._tile_color,
                self._base_tile_shape,
                0,
                int(self._tile_size/4)
            )
            self._pygame_font = pygame.font.Font("GothamBlack.ttf",Globals.TEXT_SIZE_TILE)
            self._letter_image = self._pygame_font.render(self._letter, True, "Black")
            super().update()
    @property
    def letter(self):
        """Get the letter assigned to the tile"""
        return self._letter

    @letter.setter
    def letter(self,new_letter: str):
        """Set the letter of the tile"""
        if len(new_letter) == 1: 
            self._letter = new_letter
            self._should_recompute = True
    
    @property
    def tile_type(self):
        """Get the tile type assigned to the tile"""
        return self._tile_type
    
    @tile_type.setter
    def tile_type(self,new_tile_type):
        self._tile_type = new_tile_type
        self._should_recompute = True

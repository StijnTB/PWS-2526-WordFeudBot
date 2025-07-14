import pygame
from globals import Globals, screen
from tileclass import *
from boardclass import Board
from tilebagclass import TileBag
from tilerowclass import PlayerTileRow, BotTileRow

# screen setup: top: puntenaantallen / midden: bord 15x15 tiles [tile size afhankelijk van letter size] / bodem: balk met tiles, buttons voor (speel, shuffle, tiles terug naar balk, pas), #tiles nog in de pot
pygame.init()


game_board = Board(Globals.BOARD_LAYOUT_LIST)
tilebag = TileBag()
player_tilerow = PlayerTileRow(tilebag)
bot_tilerow = BotTileRow(tilebag)
letter_selected: bool = False

mouse = pygame.mouse
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_coordinates = mouse.get_pos()
            if (
                Globals.ROW_TILES_SCREEN_HEIGHT - Globals.TILE_SIZE / 2
            ) <= click_coordinates[1] <= (
                Globals.ROW_TILES_SCREEN_HEIGHT + Globals.TILE_SIZE / 2
            ) and (
                0
                <= click_coordinates[0]
                <= (
                    Globals.TILE_SIZE * len(player_tilerow._tile_list)
                    + (len(player_tilerow._tile_list) - 1)
                    * Globals._border_between_tiles_width
                )
            ):  # mouse is in area of TileRow
                player_tilerow.change_selected_tile(click_coordinates)
            elif (
                Globals.SCREEN_TILES_STARTING_HEIGHT
                <= click_coordinates[1]
                <= (
                    Globals.SCREEN_TILES_STARTING_HEIGHT
                    + Globals.TILE_SIZE * 15
                    + Globals._border_between_tiles_width * 14
                )
            ):  # mouse is in area of Board
                clicked_tile_coordinates: tuple[int, int] = (
                    game_board.get_clicked_tile_coordinates(click_coordinates)
                )
                if player_tilerow.selected_tile_index != -1:
                    assignment_worked: bool = game_board.set_letter_to_tile(
                        player_tilerow.selected_letter, clicked_tile_coordinates
                    )
                    if assignment_worked:
                        player_tilerow.hide_selected_tile(clicked_tile_coordinates)
                    else:
                        clicked_board_tile: BoardTile = game_board.get_tile_object(
                            clicked_tile_coordinates
                        )
                        if (
                            clicked_board_tile.tile_type == "Try_board/Selected_tilerow"
                        ):  # selected tile has a letter but is still in try type
                            print("try to return")
                            player_tilerow.return_clicked_tile(
                                clicked_board_tile.letter, True
                            )
                            game_board.reset_tile(clicked_tile_coordinates)
                elif player_tilerow.selected_tile_index == -1:
                    clicked_board_tile: BoardTile = game_board.get_tile_object(
                        clicked_tile_coordinates
                    )
                    if (
                        clicked_board_tile.tile_type == "Try_board/Selected_tilerow"
                    ):  # selected tile has a letter but is still in try type
                        player_tilerow.return_clicked_tile(
                            clicked_board_tile.letter, False
                        )
                        game_board.reset_tile(clicked_tile_coordinates)


    pygame.display.flip()  # Update display

pygame.quit()

import pygame
from globals import Globals, screen
from tileclass import BoardTile
# screen setup: top: puntenaantallen / midden: bord 15x15 tiles [tile size afhankelijk van letter size] / bodem: balk met tiles, buttons voor (speel, shuffle, tiles terug naar balk, pas), #tiles nog in de pot
pygame.init()

# lijst van lijsten is overzichtelijker om te visualiseren, voor game data wordt dictionary gebruikt
board_types = [
    ["TL",None,None,None,"TW",None,None,"DL",None,None,"TW",None,None,None,"TL"],
    [None,"DL",None,None,None,"TL",None,None,None,"TL",None,None,None,"DL",None],
    [None,None,"DW",None,None,None,"DL",None,"DL",None,None,None,"DW",None,None],
    [None,None,None,"TL",None,None,None,"DW",None,None,None,"TL",None,None,None],
    ["TW",None,None,None,"DW",None,"DL",None,"DL",None,"DW",None,None,None,"TW"],
    [None,"TL",None,None,None,"TL",None,None,None,"TL",None,None,None,"TL",None],
    [None,None,"DL",None,"DL",None,None,None,None,None,"DL",None,"DL",None,None],
    ["DL",None,None,"DW",None,None,None,None,None,None,None,"DW",None,None,"DL"],
    [None,None,"DL",None,"DL",None,None,None,None,None,"DL",None,"DL",None,None],
    [None,"TL",None,None,None,"TL",None,None,None,"TL",None,None,None,"TL",None],
    ["TW",None,None,None,"DW",None,"DL",None,"DL",None,"DW",None,None,None,"TW"],
    [None,None,None,"TL",None,None,None,"DW",None,None,None,"TL",None,None,None],
    [None,None,"DW",None,None,None,"DL",None,"DL",None,None,None,"DW",None,None],
    [None,"DL",None,None,None,"TL",None,None,None,"TL",None,None,None,"DL",None],
    ["TL",None,None,None,"TW",None,None,"DL",None,None,"TW",None,None,None,"TL"],
]
game_board = {}
screen.fill((0, 0, 0))
for row_index in range(0, 15):
    game_board[str(row_index)] = {}
    for column_index in range(0, 15):
        game_board[str(row_index)][str(column_index)] = {
            "type": board_types[row_index][column_index],
            "letter": None,
            "tile_object": BoardTile(
                letter= board_types[row_index][column_index] if board_types[row_index][column_index] != None else "", 
                tile_type = board_types[row_index][column_index] if board_types[row_index][column_index] != None else "Base",
                board_coords = (row_index, column_index)
                )
        }



def create_standard_conditions():
    for row in game_board:
        for tile in game_board[row]:
            pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()  # Update display

pygame.quit()

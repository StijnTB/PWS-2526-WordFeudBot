import pygame

from tileclass import *
from boardclass import Board
from tilebagclass import TileBag
from trieclass import TRIE
from player import Player
from bot import Bot
from globals import Globals, screen
import random
from nltk.corpus import alpino

word_trie: TRIE = TRIE()

line: str
longest_word_length = 0
longest_word = ""
for line in alpino.words():  # type: ignore
    word = line.upper()
    word_trie.insert(word)

pygame.init()

screen.fill("Black")

game_board = Board(Globals.BOARD_LAYOUT_LIST, word_trie)
tilebag = TileBag()
player = Player(tilebag, game_board)
bot = Bot(tilebag, game_board)
Globals.global_should_recompute = True
starting_turn: int = random.randint(
    0, 1
)  # if starting_turn = 0, player starts, elif starting_turn = 1, bot starts
starting_turn = 0
players_turn: bool = True
running = True
while running:
    if starting_turn == 0:
        player.play()
        if player._exit:
            running = False
            break
        # bot.play()
    elif starting_turn == 1:
        bot.play()
        player.play()
        if player._exit:
            running = False
            break

pygame.quit()

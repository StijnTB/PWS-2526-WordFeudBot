import pygame
from utils import alphabet_list
from tileclass import *
from boardclass import Board
from tilebagclass import TileBag
from trieclass import TRIE
from player import Player
from competition_bot import CompetitionBot
from sidebar import SideBar
from globals import Globals, screen
import random

word_trie: TRIE = TRIE()
wordlist: list[str] = []
file = open("wordlist.txt")
for line in file:
    word = line.strip()
    word_trie.insert(word)
    wordlist.append(word)


pygame.init()

screen.fill("Black")

game_board = Board(Globals.BOARD_LAYOUT_LIST, word_trie)
tilebag = TileBag()
sidebar = SideBar()
player = Player(tilebag, game_board, sidebar)
bot = CompetitionBot(tilebag, game_board, sidebar, wordlist)

Globals.global_should_recompute = True

turn: int = random.randint(0, 1)
turn = 0
players_turn: bool = True
running = True
exit_phase: bool = True
while running:
    if turn == 0:
        player.play()
        if player._exit:
            running = False
            exit_phase = False  # skip exit phase
            break
        turn = 1
    elif turn == 1:
        bot.competition_bot_play()
        turn = 0
    print(f"player tilerow: {player._tilerow._tile_list}")
    print(f"bot tilerow: {bot._tilerow._tile_list}")

    if set(player._tilerow._tile_list) == {""}:
        sidebar._score_object.player_score += bot._tilerow.get_remaining_points()
        sidebar._score_object.bot_score -= bot._tilerow.get_remaining_points()
        pygame.display.flip()
        break
    elif set(bot._tilerow._tile_list) == {""} or bot._tilerow._tile_list == []:
        sidebar._score_object.bot_score += player._tilerow.get_remaining_points()
        sidebar._score_object.player_score -= player._tilerow.get_remaining_points()
        pygame.display.flip()
        break

print("entering exit phase")
while exit_phase:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_phase = False
            break
pygame.quit()

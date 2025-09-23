import time

start_time = time.time()
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
random.seed(Globals.random_seed)
word_trie: TRIE = TRIE()
wordlist: list[str] = []

with open("wordlist.txt", "r", encoding="utf-8") as wordlist_file:
    wordlist: list[str] = wordlist_file.read().splitlines()
    for index in range(len(wordlist)):
        wordlist[index] = wordlist[index].upper()
        word_trie.insert(wordlist[index].upper())
pygame.init()

screen.fill("Black")

game_board = Board(Globals.BOARD_LAYOUT_LIST, word_trie)
tilebag = TileBag()
sidebar = SideBar()
player = CompetitionBot(tilebag, game_board, sidebar, wordlist, 2)
bot = CompetitionBot(tilebag, game_board, sidebar, wordlist, 1)

Globals.global_should_recompute = True

turn: int = random.randint(0, 1)
turn = 1
running = True
exit_phase: bool = True
end_time = time.time()
time_spent: float = end_time - start_time
amount_of_turns: int = 0
print(time_spent)
while running:
    if turn == 0:
        player.competition_bot_play()
        turn = 1
    elif turn == 1:
        bot.competition_bot_play()
        turn = 0
    amount_of_turns += 1
    print(amount_of_turns)
    print(f"player tilerow: {player._tilerow._tile_list}")
    print(f"bot tilerow: {bot._tilerow._tile_list}")
    if Globals.amount_of_passes == 3:
        sidebar._score_object.player_score -= player._tilerow.get_remaining_points()
        sidebar._score_object.bot_score -= bot._tilerow.get_remaining_points()
        pygame.display.flip()
        break
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

print("entering exit phase")
while exit_phase:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_phase = False
            break
pygame.quit()

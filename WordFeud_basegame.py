from itertools import combinations
from json import load
from pygame import init, quit, event, display, QUIT
from random import seed, randint

from boardclass import Board
from competition_bot import CompetitionBot
from globals import Globals, screen
from player import Player  # pyright: ignore[reportUnusedImport]
from sidebar import SideBar
from tilebagclass import TileBag
from trieclass import TRIE


init()
seed(Globals.RANDOM_SEED)
word_trie: TRIE = TRIE()
wordlist: list[str] = []
bots_greedy_or_board_position: bool = False
seven_letter_words: list[str] = []
word_dict: dict[int, dict[str, list[str]]] = {}
with open("wordlist.txt", "r", encoding="utf-8") as wordlist_file:
    wordlist: list[str] = wordlist_file.read().splitlines()
    for index in range(len(wordlist)):
        word: str = wordlist[index].upper()
        if len(word) == 7 and not bots_greedy_or_board_position:
            seven_letter_words.append(word)
        wordlist[index] = word
        word_trie.insert(word)

with open("achtervoegselwoorden.json", "r") as f:
    achtervoegsels = load(f)
with open("voorvoegselwoorden.json", "r") as f:
    voorvoegsels = load(f)


if not bots_greedy_or_board_position:
    word_dict: dict[int, dict[str, list[str]]] = {7: {}, 6: {}, 5: {}}

    combinations_6: list[tuple[int, ...]] = list(combinations(range(7), 6))
    combinations_5: list[tuple[int, ...]] = list(combinations(range(7), 5))
    for word in seven_letter_words:
        key7: str = "".join(sorted(word))
        if key7 not in word_dict[7]:
            word_dict[7][key7] = [word]
        else:
            word_dict[7][key7].append(word)
        for combination in combinations_6:
            kept = "".join(sorted(word[i] for i in combination))
            if kept not in word_dict[6]:
                word_dict[6][kept] = [word]
            else:
                word_dict[6][kept].append(word)
        for combination in combinations_5:
            kept = "".join(sorted(word[i] for i in combination))
            if kept not in word_dict[5]:
                word_dict[5][kept] = [word]
            else:
                word_dict[5][kept].append(word)


screen.fill("Black")

game_board = Board(Globals.BOARD_LAYOUT_LIST, word_trie)
tilebag = TileBag()
sidebar = SideBar()
player = CompetitionBot(
    tilebag,
    game_board,
    sidebar,
    wordlist,
    2,
    "greedy",
    word_dict,
    voorvoegsels,
    achtervoegsels,
)
bot = CompetitionBot(
    tilebag,
    game_board,
    sidebar,
    wordlist,
    1,
    "combi",
    word_dict,
    voorvoegsels,
    achtervoegsels,
)

Globals.global_should_recompute = True
starting_turn: int = randint(
    0, 1
)  # if starting_turn = 0, player starts, elif starting_turn = 1, bot starts
starting_turn = 0
players_turn: bool = True
turn = starting_turn
amount_of_turns: int = 0
running = True
while running:
    for _event in event.get():
        if _event.type == QUIT:
            running = False
    print(f"player tilerow: {player.tilerow.tile_list}")
    print(f"bot tilerow: {bot.tilerow.tile_list}")
    Globals.players_tilerows[1] = player.tilerow.tile_list
    Globals.players_tilerows[2] = bot.tilerow.tile_list
    if turn == 0:
        player.competition_bot_play()
        turn = 1
    elif turn == 1:
        bot.competition_bot_play()
        turn = 0
    amount_of_turns += 1
    print(amount_of_turns)
    if Globals.amount_of_passes >= 3:
        sidebar.score_object.player_score -= player.tilerow.get_remaining_points()
        sidebar.score_object.bot_score -= bot.tilerow.get_remaining_points()
        display.flip()
        break
    if set(player.tilerow.tile_list) == {""}:
        sidebar.score_object.player_score += bot.tilerow.get_remaining_points()
        sidebar.score_object.bot_score -= bot.tilerow.get_remaining_points()
        display.flip()
        break
    elif set(bot.tilerow.tile_list) == {""} or bot.tilerow.tile_list == []:
        sidebar.score_object.bot_score += player.tilerow.get_remaining_points()
        sidebar.score_object.player_score -= player.tilerow.get_remaining_points()
        display.flip()
        break

quit()

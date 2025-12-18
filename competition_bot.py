from itertools import combinations, product
from math import comb, e
from pygame import display
from random import choices, seed 
from time import sleep
from typing import Literal

from bot import Bot
from boardclass import Board
from botmove import BotMoveObject
from globals import Globals
from sidebar import SideBar
from tilebagclass import TileBag
from tileclass import BoardTile
from utils import get_expected_multiplication

seed(Globals.RANDOM_SEED)

empty_tile: set[None | str] = {None, "DW", "DL", "TW", "TL", ""}


class CompetitionBot(Bot):
    def __init__(
        self,
        tilebag: TileBag,
        board: Board,
        sidebar: SideBar,
        wordlist: list[str],
        player_id: Literal[1, 2],
        modus: Literal["greedy", "kansberekening", "bordpositie", "combi"],
        word_dict: dict[int, dict[str, list[str]]],
        voorvoegsels: dict[str, str],
        achtervoegsels: dict[str, str],
    ):
        self._tilebag: TileBag = tilebag
        self._board: Board = board
        self._sidebar: SideBar = sidebar
        self._wordlist: list[str] = wordlist
        self._player_id: int = player_id
        self._modus: Literal["greedy", "kansberekening", "bordpositie", "combi"] = (
            modus  # "greedy", "kansberekening", "bordpositie", "combi" voor initializatie specifieke functies
        )
        self._letterFreqs: dict[str, list[int]] = {}
        self._checkList: dict[str, list[int]] = {}
        self._letterTypes: list[int] = [0 for _ in range(len(self._wordlist))]
        self._word_dict: dict[int, dict[str, list[str]]] = word_dict
        self._voorvoegsels: dict[str, str] = voorvoegsels
        self._achtervoegsels: dict[str, str] = achtervoegsels
        self._amount_of_turns: int = 0
        i: int = 0
        for word in self._wordlist:
            self._letterFreqs[str(i)] = self.countFrequencyOfEachLetterType(word)
            self._checkList[str(i)] = [
                index for index in range(0, 26) if self._letterFreqs[str(i)][index] > 0
            ]
            self._letterTypes[i] = self.letterTypesInWord(word)
            i += 1

        super().__init__(self._tilebag, self._board)

    def getGreedyMove(self) -> BotMoveObject:

        possible_moves_list: list[BotMoveObject] = []
        best_move_greedy: BotMoveObject = BotMoveObject([], [], [], (1, 1), 0)
        bingo_dict: dict[str, float] = {}
        if self._modus in ("kansberekening", "combi"):
            if self._tilebag.get_amount_of_letters_remaining() > 0:
                bingo_dict = self.get_bingo_dict()
                print(bingo_dict)
            if self._tilebag.get_amount_of_letters_remaining() >= 7:
                max_pair: tuple[str, float] = ("", 0.0)
                for bingo_set in bingo_dict.items():
                    if bingo_set[1] > max_pair[1]:
                        max_pair = bingo_set
                best_move_greedy: BotMoveObject = BotMoveObject(
                    [letter for letter in max_pair[0]],
                    [],
                    [],
                    (1, 1),
                    0,
                    max_pair[1] * Globals.BINGO_BONUS_SCORE_MULTIPLIER,
                )

        for row in range(0, 15):
            if not self.skip_array("row", row):
                tiles_in_row: str = self.get_letters_in_array("row", row)
                if 1 != 1:
                    for tile in self._board.game_board[str(row)].values():
                        tiles_in_row += (
                            tile["tile_object"].letter
                            if tile["tile_object"].letter not in empty_tile
                            else ""
                        )
                best_move_horizontal, possible_moves_horizontal = (
                    self.get_attempt_objects_in_array(
                        "row", row, tiles_in_row, bingo_dict
                    )
                )
                possible_moves_list.extend(possible_moves_horizontal)
                if round(
                    (
                        best_move_greedy.score
                        + best_move_greedy.bingo_bonus_score
                        - best_move_greedy.position_degradation_score
                    )
                ) < round(
                    best_move_horizontal.score
                    + best_move_horizontal.bingo_bonus_score
                    - best_move_horizontal.position_degradation_score
                ):
                    best_move_greedy = best_move_horizontal

        for column_index in range(0, 15):
            if not self.skip_array("column", column_index):
                tiles_in_column: str = self.get_letters_in_array("column", column_index)
                if 1 != 1:
                    for row in self._board.game_board.values():
                        current_tile = row[str(column_index)]["letter"]
                        if current_tile not in empty_tile and isinstance(
                            current_tile, str
                        ):
                            tiles_in_column += current_tile
                        else:
                            tiles_in_column += ""
                best_move_vertical, possible_moves_vertical = (
                    self.get_attempt_objects_in_array(
                        "column", column_index, tiles_in_column, bingo_dict
                    )
                )
                possible_moves_list.extend(possible_moves_vertical)
                if round(
                    (
                        best_move_greedy.score
                        + best_move_greedy.bingo_bonus_score
                        - best_move_greedy.position_degradation_score
                    )
                ) < round(
                    (
                        best_move_vertical.score
                        + best_move_vertical.bingo_bonus_score
                        - best_move_vertical.position_degradation_score
                    )
                ):
                    best_move_greedy = best_move_vertical
        if self._amount_of_turns >= 100:
            print(
                "moves: ", [move.move_attempted_words for move in possible_moves_list]
            )
        return best_move_greedy

    def competition_bot_play(self) -> None:
        display.flip()
        if self._board.is_first_turn:
            self._amount_of_turns = 1
        else:
            self._amount_of_turns += 2
        print("move is", self._amount_of_turns)
        best_move = self.getGreedyMove()
        print(f"best move\n {best_move.properties}")
        played_tiles: list[str] = best_move.move_attempted_letters
        move_failed: bool = False
        letters_to_coordinates: list[tuple[str, tuple[int, int]]] = []
        if len(best_move.move_coordinates) > 0:
            for index in range(len(played_tiles)):
                letters_to_coordinates.append(
                    (played_tiles[index], best_move.move_coordinates[index])
                )
        else:
            move_failed = True
        cross_off_tilerow: list[str] = self._tilerow.tile_list.copy()
        blanks_coordinates: list[tuple[int, int]] = []
        for tile in letters_to_coordinates:
            if tile[0] in cross_off_tilerow:
                cross_off_tilerow.remove(tile[0])
            elif not tile[0] in cross_off_tilerow:
                if " " in cross_off_tilerow:
                    cross_off_tilerow.remove(" ")
                    blanks_coordinates.append(tile[1])
                else:
                    print(
                        f"move failed: more blanks used than possible with tilerow, failed on tile '{tile[0]}"
                    )
                    move_failed = True
        if not move_failed and (best_move.score > 0):
            self._board.bot_play_word(
                best_move.move_coordinates,
                best_move.move_attempted_letters,
                blanks_coordinates,
            )
            self._tilerow.get_new_letters(best_move.move_attempted_letters)
            if self._player_id == 1:
                self._sidebar.score_object.bot_score += best_move.score
            elif self._player_id == 2:
                self._sidebar.score_object.player_score += best_move.score
            Globals.amount_of_passes = 0
        elif move_failed and best_move.bingo_bonus_score > 0:
            self.tilerow.swap_letters(best_move.move_attempted_letters)
            print(f"swapped {best_move.move_attempted_letters}")
        else:
            print("no move found, bot passes")
            Globals.amount_of_passes += 1
        display.flip()
        sleep(1)

    def get_letters_in_array(
        self, row_or_column: Literal["row", "column"], array_index: int
    ) -> str:
        tiles_in_array: str = ""
        for variable_index in range(0, 15):
            board_coordinates: tuple[int, int] = (
                (variable_index if row_or_column == "column" else array_index),
                (array_index if row_or_column == "column" else variable_index),
            )
            tiles_in_array += (
                self._board.game_board[str(board_coordinates[0])][
                    str(board_coordinates[1])
                ]["tile_object"].letter
                if self._board.game_board[str(board_coordinates[0])][
                    str(board_coordinates[1])
                ]["tile_object"].letter
                not in empty_tile
                else ""
            )
        return tiles_in_array

    def get_attempt_objects_in_array(
        self,
        row_or_column: Literal["row", "column"],
        array_index: int,
        tiles_in_array: str,
        bingo_dict: dict[str, float],
    ) -> tuple[BotMoveObject, list[BotMoveObject]]:
        attempt_called: int = 0
        possible_moves_list: list[BotMoveObject] = []
        best_move_greedy: BotMoveObject = BotMoveObject([], [], [], (1, 1), 0)
        filtered_wordlist: list[str] = self.filter(tiles_in_array)
        for word in filtered_wordlist:
            for tile in (
                [
                    self._board.game_board[str(array_index)][str(column_index)][
                        "tile_object"
                    ]
                    for column_index in range(0, 15)
                ]
                if row_or_column == "row"
                else [
                    self._board.game_board[str(row_index)][str(array_index)][
                        "tile_object"
                    ]
                    for row_index in range(0, 15)
                ]
            ):
                attempt_called += 1
                attempt = self.try_word_on_tile(
                    word,
                    tile,
                    (0, 1) if row_or_column == "row" else (1, 0),
                    tiles_in_array,
                )
                if attempt:
                    attempt_object = BotMoveObject(
                        attempt[3],
                        attempt[1],
                        attempt[2],
                        (0, 1) if row_or_column == "row" else (1, 0),
                        attempt[0],
                        0,
                        attempt[4],
                    )
                    if attempt_object.move_coordinates != []:
                        possible_moves_list.append(attempt_object)
                        if self._modus in ("kansberekening", "combi"):
                            self.update_bingo_bonus_score(attempt_object, bingo_dict)
                        # if self._modus in ("bordpositie", "combi"):
                        #    self.update_boardposition_score(attempt_object)
                        

                        if round(
                            (
                                attempt_object.score
                                + attempt_object.bingo_bonus_score
                                - attempt_object.position_degradation_score
                            )
                        ) > round(
                            (
                                best_move_greedy.score
                                + best_move_greedy.bingo_bonus_score
                                - best_move_greedy.position_degradation_score
                            )
                        ):
                            best_move_greedy = attempt_object

        return (best_move_greedy, possible_moves_list)

    def try_word_on_tile(
        self,
        word: str,
        tile: BoardTile,
        direction: tuple[int, int],
        tiles_in_array: str,
    ) -> (
        Literal[False] | tuple[int, list[str], list[tuple[int, int]], list[str], float]
    ):
        if self.ends_out_of_bounds(tile, direction, word):
            
            return False

        opposite_direction: tuple[int, int] = (1, 0) if direction == (0, 1) else (0, 1)

        if self.touches_no_tiles(tile, direction, opposite_direction, word):
            return False

        if self.word_has_letters_before_or_after(tile, direction, word):
            return False

        rearrange_tiles_results: bool | tuple[list[tuple[int, int]], list[str]] = (
            self.rearranges_tiles(tile, direction, word, tiles_in_array)
        )
        if isinstance(rearrange_tiles_results, bool):
            return False
        word_attempt_tiles, word_attempt_letters = rearrange_tiles_results

        points_results = self.get_points_and_attempted_words(
            tile,
            direction,
            opposite_direction,
            word,
            word_attempt_letters,
            word_attempt_tiles,
        )
        if not points_results:
            return False
        total_points, attempted_words, boardposition_score = points_results
        if total_points == 0:
            return False
        return (
            total_points,
            attempted_words,
            word_attempt_tiles,
            word_attempt_letters,
            boardposition_score,
        )

    def ends_out_of_bounds(
        self, tile: BoardTile, direction: tuple[int, int], word: str
    ) -> bool:
        if direction == (0,1):
            
            if tile.board_coordinates[1] + len(word) - 1 > 14:
                return True
        if direction == (1,0):
            
            if tile.board_coordinates[0] + len(word) - 1 > 14:
                #tile.board_coordinates[1] is 10; len(word) is 5; 
                return True
        return False

    def word_has_letters_before_or_after(
        self, tile: BoardTile, direction: tuple[int, int], word: str
    ) -> bool:
        if (
            tile.board_coordinates[0] - direction[0] != -1
            and tile.board_coordinates[1] - direction[1] != -1
        ):
            if (
                self._board.game_board[str(tile.board_coordinates[0] - direction[0])][
                    str(tile.board_coordinates[1] - direction[1])
                ]["tile_object"].tile_type
                == "Set_board/Base_tilerow"
            ):
                return True  # the attempted word has a letter before it

        if (
            tile.board_coordinates[0] + direction[0] * (len(word) + 0) != 15
            and tile.board_coordinates[1] + direction[1] * (len(word) + 0) != 15
        ):
            if (
                self._board.game_board[
                    str(tile.board_coordinates[0] + direction[0] * (len(word) + 0))
                ][str(tile.board_coordinates[1] + direction[1] * (len(word) + 0))][
                    "tile_object"
                ].tile_type
                == "Set_board/Base_tilerow"
            ):
                return True  # the attempted word has a letter behind it
        return False

    def rearranges_tiles(
        self,
        tile: BoardTile,
        direction: tuple[int, int],
        word: str,
        tiles_in_array: str,
    ) -> bool | tuple[list[tuple[int, int]], list[str]]:
        current_board_state: str = (
            ""  # the word currently formed by the entire row or column the word is placed in, with blank tiles represented as "_"
        )
        starting_coordinates: tuple[int, int] = (
            tile.board_coordinates[0] * (1 - direction[0]),
            tile.board_coordinates[1] * (1 - direction[1]),
        )
        word_attempt_tiles: list[tuple[int, int]] = (
            []
        )  # a list of the tile coordinates of the tiles the bot lays
        word_attempt_letters: list[str] = []
        for index in range(0, 15):
            current_tile_letter = self._board.game_board[
                str(starting_coordinates[0] + direction[0] * index)
            ][str(starting_coordinates[1] + direction[1] * index)]["tile_object"].letter
            if current_tile_letter in empty_tile:
                current_tile_letter = "_"
            current_board_state += current_tile_letter
        attempted_word_as_state: str = ""
        tiles_before_word: int = 0
        for index in range(
            0,
            int(
                (
                    tile.board_coordinates[0] ** 2 * direction[0]
                    + tile.board_coordinates[1] ** 2 * direction[1]
                )
                ** 0.5
            ),
        ):
            attempted_word_as_state += "_"
            tiles_before_word += 1
        attempted_word_as_state += word
        for index in range(0, 15 - tiles_before_word - len(word)):
            attempted_word_as_state += "_"
        letters_required_with_word_placement: list[str] = []
        for index in range(tiles_before_word, tiles_before_word + len(word)):
            if current_board_state[index] == "_":
                if (
                    attempted_word_as_state[index] != "_"
                ):  # empty tile is replaced by letter
                    tile_coordinate: tuple[int, int] = (
                        starting_coordinates[0] + index * direction[0],
                        starting_coordinates[1] + index * direction[1],
                    )
                    word_attempt_tiles.append(tile_coordinate)
                    word_attempt_letters.append(attempted_word_as_state[index])
                # filling up previously empty tiles is allowed
            else:
                if current_board_state[index] != attempted_word_as_state[index]:
                    return True  # replacing previously filled tiles with either other letters or empty is not allowed

        for index in range(0, tiles_before_word):
            letter = self._board.game_board[
                str(starting_coordinates[0] + index * direction[0])
            ][str(starting_coordinates[1] + index * direction[1])]["tile_object"].letter
            if letter not in empty_tile:
                letters_required_with_word_placement += letter
        for letter in word:
            letters_required_with_word_placement += letter
        for index in range(tiles_before_word + len(word), 15):
            letter = self._board.game_board[
                str(starting_coordinates[0] + index * direction[0])
            ][str(starting_coordinates[1] + index * direction[1])]["tile_object"].letter
            if letter not in empty_tile:
                letters_required_with_word_placement += letter
        # letters_available: list[str] = [char for char in tiles_in_array].extend(self._tilerow.tile_list)
        letters_available = [char for char in tiles_in_array]
        for letter in self._tilerow.tile_list:
            letters_available.append(letter)
        letters_required: str = "".join(letters_required_with_word_placement)
        for letter in letters_required:
            if letter in letters_available:
                letters_available.remove(
                    letter
                )  # cross off letters to prevent double use
            elif not letter in letters_available:
                if " " in letters_available:
                    letters_available.remove(" ")
                else:
                    return True  # letters have been allocated from outside of the word range to inside, creating doubles
        return (word_attempt_tiles, word_attempt_letters)

    def touches_no_tiles(
        self,
        tile: BoardTile,
        direction: tuple[int, int],
        opposite_direction: tuple[int, int],
        word: str,
    ) -> bool:
        index = 0
        lies_on_no_letters: bool = True
        has_no_adjacent_letters: bool = True
        while index < len(word):
            check_tile_coordinate: tuple[int, int] = (
                tile.board_coordinates[0] + direction[0] * index,
                tile.board_coordinates[1] + direction[1] * index,
            )
            if check_tile_coordinate == (7, 7):
                lies_on_no_letters = False
            if (
                self._board.game_board[str(check_tile_coordinate[0])][
                    str(check_tile_coordinate[1])
                ]["tile_object"].tile_type
                == "Set_board/Base_tilerow"
            ):
                lies_on_no_letters = False
            if (
                check_tile_coordinate[0] - opposite_direction[0] != -1
                and check_tile_coordinate[1] - opposite_direction[1] != -1
            ):
                if (
                    self._board.game_board[
                        str(check_tile_coordinate[0] - opposite_direction[0])
                    ][str(check_tile_coordinate[1] - opposite_direction[1])][
                        "tile_object"
                    ].tile_type
                    == "Set_board/Base_tilerow"
                ):
                    has_no_adjacent_letters = False
            if (
                check_tile_coordinate[0] + opposite_direction[0] != 15
                and check_tile_coordinate[1] + opposite_direction[1] != 15
            ):
                if (
                    self._board.game_board[
                        str(check_tile_coordinate[0] + opposite_direction[0])
                    ][str(check_tile_coordinate[1] + opposite_direction[1])][
                        "tile_object"
                    ].tile_type
                    == "Set_board/Base_tilerow"
                ):
                    has_no_adjacent_letters = False
            index += 1
        if has_no_adjacent_letters and lies_on_no_letters:
            return True  # the attempted word has no adjacent tiles and does not lie on any already used tile
        return False

    def get_points_and_attempted_words(
        self,
        tile: BoardTile,
        direction: tuple[int, int],
        opposite_direction: tuple[int, int],
        word: str,
        word_attempt_letters: list[str],
        word_attempt_tiles: list[tuple[int, int]],
    ) -> Literal[False] | tuple[int, list[str], float]:
        total_points: int = 0
        attempted_words: list[str] = []
        attempted_words.append(word)
        first_tile_coordinates: tuple[int, int] = (14, 14)
        for index in range(0, len(word)):
            tile_object = self._board.game_board[
                str(tile.board_coordinates[0] + direction[0] * index)
            ][str(tile.board_coordinates[1] + direction[1] * index)]["tile_object"]
            if tile_object.tile_type != "Set_board/Base_tilerow":
                tile_object.letter = word[index]
                tile_object.tile_type = "Try_board/Selected_tilerow"
        set_tiles_list: list[tuple[int, int]] = [
            (
                tile.board_coordinates[0] + index * direction[0],
                tile.board_coordinates[1] + index * direction[1],
            )
            for index in range(len(word))
            if self._board.game_board[
                str(tile.board_coordinates[0] + index * direction[0])
            ][str(tile.board_coordinates[1] + index * direction[1])][
                "tile_object"
            ].tile_type
            == "Try_board/Selected_tilerow"
        ]
        for tile_coordinates in set_tiles_list:
            if (
                tile_coordinates[0] <= first_tile_coordinates[1]
                and tile_coordinates[1] <= first_tile_coordinates[1]
            ):
                first_tile_coordinates = tile_coordinates
        cross_off_tilerow = self.tilerow.tile_list.copy()
        blank_coordinate_indexes: list[int] = []
        for index, letter in enumerate(word_attempt_letters):
            if letter in cross_off_tilerow:
                cross_off_tilerow.remove(letter)
            else:
                if " " in cross_off_tilerow:
                    cross_off_tilerow.remove(" ")
                    blank_coordinate_indexes.append(index)
        blank_coordinates: list[tuple[int, int]] = [
            word_attempt_tiles[index] for index in blank_coordinate_indexes
        ]
        main_word, main_word_value = self._board.get_word_from_tile(
            first_tile_coordinates, direction, set_tiles_list, blank_coordinates
        )

        if len(main_word) > 1:
            if not self._board.word_tree.search_word(main_word):
                self._board.reset_tiles(set_tiles_list)
                return False
            attempted_words.append(main_word)
            total_points += main_word_value
        for tile_coordinates in set_tiles_list:
            word_created, word_value = self._board.get_word_from_tile(
                tile_coordinates, opposite_direction, set_tiles_list, blank_coordinates
            )
            if len(word_created) > 1:
                if not self._board.word_tree.search_word(word_created):
                    self._board.reset_tiles(set_tiles_list)
                    return False
                attempted_words.append(word_created)
                total_points += word_value
        if len(set_tiles_list) == 7:
            total_points += 40  # add 40 for all tiles set
        boardposition_score: float = 0
        if self._modus in ("bordpositie", "combi"):
            if len(word_attempt_letters) > 0:
                boardposition_score = self.update_boardposition_score(
                    word_attempt_tiles, direction, word_attempt_letters, attempted_words
                )
        self._board.reset_tiles(set_tiles_list)

        return (total_points, attempted_words, boardposition_score)

    def filter(self, letters_on_selected: str) -> list[str]:
        blanks: int = 0
        for tile in self._tilerow.tile_list:
            if tile == " ":
                blanks += 1
        tilerow2 = [tile for tile in self._tilerow.tile_list if tile != " "]
        letters: str = "".join(tilerow2) + letters_on_selected
        hasLetters = self.countFrequencyOfEachLetterType(letters)
        hasTheseLetterTypes = self.letterTypesInWord(letters)
        res: list[str] = []
        i: int = 0
        for word in self._wordlist:
            if blanks > 0 or self.hasLetterTypes(
                self._letterTypes[i], hasTheseLetterTypes
            ):
                if self.hasNeededLetters(
                    self._checkList[str(i)],
                    self._letterFreqs[str(i)],
                    hasLetters,
                    blanks,
                ):
                    res.append(word)
            i += 1
        return res

    def valid_words(self, tilerow: list[str]) -> list[str]:

        n_blank = tilerow.count(" ")
        non_blanks = sorted([letter for letter in tilerow if letter != " "])

        if n_blank == 0 and len(non_blanks) == 7:
            key7: str = "".join(non_blanks)
            return self._word_dict[7][key7] if key7 in self._word_dict[7] else []
        elif n_blank == 1 and len(non_blanks) == 6:
            key6: str = "".join(non_blanks)
            return self._word_dict[6][key6] if key6 in self._word_dict[6] else []
        elif n_blank == 2 and len(non_blanks) == 5:
            key5: str = "".join(non_blanks)
            return self._word_dict[5][key5] if key5 in self._word_dict[5] else []
        else:
            return []

    def brute_force(
        self, tilerow: list[str], tilebag: list[str], k: int
    ) -> list[tuple[str, float]]:
        information: list[tuple[str, float]] = []
        bingo_chance: float = 0.0
        for letters_to_replace in combinations(range(7), k):
            amount_of_bingo: int = 0
            amount_of_options: int = 0
            for replacements in product(tilebag, repeat=k):
                new_tilerow = tilerow.copy()
                for idx, p in enumerate(letters_to_replace):
                    new_tilerow[p] = replacements[idx]
                if self.valid_words(new_tilerow):
                    amount_of_bingo += 1
                amount_of_options += 1
            if amount_of_options > 0:
                bingo_chance = round(amount_of_bingo / amount_of_options * 100, 1)
            else:
                bingo_chance = 0.0
            information.append(
                ("".join(sorted(tilerow[i] for i in letters_to_replace)), bingo_chance)
            )
        return information

    def sampling(
        self, tilerow: list[str], tilebag: list[str], k: int, samples: int
    ) -> list[tuple[str, float]]:
        information: list[tuple[str, float]] = []
        combinations_list: list[tuple[int, ...]] = list(combinations(range(7), k))
        n_combinations = len(combinations_list)
        samples_per_combination: int = max(1, samples // n_combinations)

        for letters_to_replace in combinations_list:
            amount_of_bingo: int = 0
            for _ in range(samples_per_combination):
                new_tilerow: list[str] = tilerow.copy()
                new_letters: list[str] = choices(tilebag, k=k)
                for idx, p in enumerate(letters_to_replace):
                    new_tilerow[p] = new_letters[idx]
                if self.valid_words(new_tilerow):
                    amount_of_bingo += 1

            bingo_chance: float = round(
                amount_of_bingo / samples_per_combination * 100, 1
            )
            key: str = "".join(sorted(tilerow[letter] for letter in letters_to_replace))
            information.append((key, bingo_chance))
        return information

    def bingo_chance(
        self, tilerow: list[str], tilebag: list[str], k: int, samples: int
    ) -> list[tuple[str, float]]:
        tilebag_size = len(tilebag)
        tilebag_size += (
            len(Globals.players_tilerows[1])
            if self._player_id == 2
            else len(Globals.players_tilerows[2])
        )
        amount_of_options = comb(7, k) * (tilebag_size**k)
        tilebag_unseen = tilebag.copy()
        tilebag_unseen.extend(
            (
                Globals.players_tilerows[1]
                if self._player_id == 2
                else Globals.players_tilerows[2]
            )
        )
        if amount_of_options <= samples:
            return self.brute_force(tilerow, tilebag_unseen, k)
        else:
            return self.sampling(tilerow, tilebag_unseen, k, samples)

    def update_bingo_bonus_score(
        self, attempt_object: BotMoveObject, bingo_dict: dict[str, float]
    ) -> None:
        check_bonus_score: str = "".join(sorted(attempt_object.move_attempted_letters))
        if check_bonus_score in bingo_dict:
            if len(attempt_object.move_attempted_letters) == 7:
                attempt_object.bingo_bonus_score = bingo_dict[check_bonus_score] * 1
                print(
                    "bingo", attempt_object.move_attempted_words, attempt_object.score
                )
            else:
                attempt_object.bingo_bonus_score = bingo_dict[check_bonus_score]
        if self.countBlanks() > 0:
            for letter in attempt_object.move_attempted_letters:
                new_tilerow = attempt_object.move_attempted_letters.copy()
                index = new_tilerow.index(letter)
                new_tilerow[index] = " "
                check = "".join(sorted(new_tilerow))
                if check in bingo_dict:
                    new_bonus: float = (
                        bingo_dict[check] * 1
                        if len(attempt_object.move_attempted_letters) == 7
                        else bingo_dict[check]
                    )
                    if new_bonus > attempt_object.bingo_bonus_score:
                        attempt_object.bingo_bonus_score = new_bonus
        attempt_object.bingo_bonus_score *= Globals.BINGO_BONUS_SCORE_MULTIPLIER

    def get_bingo_dict(self) -> dict[str, float]:
        result: list[list[tuple[str, float]]] = []
        for k in range(1, 8):
            result.append(
                self.bingo_chance(
                    self._tilerow.tile_list, self._tilebag.bag_list, k, 400000
                )
            )
        return {
            letters: chance
            for letters, chance in [item for sublist in result for item in sublist]
        }

    def update_boardposition_score(
        self,
        move_coordinates: list[tuple[int, int]],
        move_direction: tuple[int, int],
        move_letters: list[str],
        move_words: list[str],
    ) -> float:
        # the degradation factor which will be applied to get the final score of the move
        degradation_value: float = 0
        degradation_value_list: list[float] = []
        # the danger factors created by different tiles: if multiple tiles create similar danger factors, they start to count less
        combinations_created: dict[int, float] = {}
        # the amount of decimals used for comparing danger factors
        for tile in move_coordinates:
            expected_multiplication: float = get_expected_multiplication(
                tile, (move_direction[1], move_direction[0]), self._board.game_board
            )
            current_tile_attempt_letter: str = move_letters[
                move_coordinates.index(
                    self._board.game_board[str(tile[0])][str(tile[1])][
                        "tile_object"
                    ].board_coordinates
                )
            ]
            # if the letter of the current move tile is a vowel, the danger is greater than if it is a consonant

            worth_letter = self._tilebag.tile_bag_dict[current_tile_attempt_letter][
                "value"
            ]

            degradation_value_list.append(
                expected_multiplication * (1.5 * e ** (-0.178337 * (worth_letter - 1)))
            )
            degradation_value += expected_multiplication * (
                1.5 * e ** (-0.178337 * (worth_letter - 1))
            )
            # print(current_tile_attempt_letter, expected_multiplication * (1.5 * math.e ** (-0.178337 * (worth_letter - 1))))
            combinations_created[move_coordinates.index(tile)] = expected_multiplication

        # print('gevaar woord zelf:', degradation_value)
        addition_danger: float = 0
        if len(move_words) > 1:
            main_word: str = move_words[1]
        else:
            main_word: str = move_words[0]

        found_suffixes: Literal[-1] | str = self._achtervoegsels.get(main_word, -1)
        if found_suffixes != -1:
            additions: list[str] = [char for char in found_suffixes]
            tilerow_opponent: list[str] = Globals.players_tilerows[
                1 if self._player_id == 1 else 2
            ]
            amount_in_bag = 0
            amount_on_own_rack = 0
            for addition_letter in additions:
                amount_on_own_rack += self.tilerow.amount_of_letter_on_rack(
                    self.tilerow.tile_list, addition_letter
                )
                amount_in_bag += self._tilebag.get_amount_of_letter(
                    addition_letter
                ) + self.tilerow.amount_of_letter_on_rack(
                    tilerow_opponent, addition_letter
                )
            if amount_in_bag != 0:
                amount_in_bag -= (
                    (3 - self.get_score_difference() / 75)
                    * amount_on_own_rack
                    / amount_in_bag
                )
            else:
                amount_in_bag -= (
                    3 - self.get_score_difference() / 75
                ) * amount_on_own_rack
            if self._tilebag.get_amount_of_letters_remaining() > 0:
                amount_in_bag *= 1 / (
                    self._tilebag.get_amount_of_letters_remaining() + 7
                )
            addition_danger += (
                Globals.BOARDPOSITION_FACTORS["Addition_Danger"] * amount_in_bag
            )
            multiplication_danger_on_next_tile: float = get_expected_multiplication(
                (
                    move_coordinates[-1][0] + move_direction[0],
                    move_coordinates[-1][1] + move_direction[1],
                ),
                (move_direction[1], move_direction[0]),
                self._board.game_board,
            )
            addition_danger += (
                multiplication_danger_on_next_tile
                * Globals.BOARDPOSITION_FACTORS["Addition_Danger"]
                * amount_in_bag
            )
            degradation_value_list.append(
                multiplication_danger_on_next_tile
                * Globals.BOARDPOSITION_FACTORS["Addition_Danger"]
                * amount_in_bag
            )
            # print('achtervoegsels', multiplication_danger_on_next_tile * Globals.BOARDPOSITION_FACTORS["Addition_Danger"] * amount_in_bag)
        found_prefixes: Literal[-1] | str = self._voorvoegsels.get(main_word, -1)
        if found_prefixes != -1:
            additions = [char for char in found_prefixes]

            tilerow_opp = (
                Globals.players_tilerows[1]
                if self._player_id == 1
                else Globals.players_tilerows[2]
            )
            amount_on_own_rack = 0
            amount_in_bag = 0
            for addition_letter in additions:
                amount_on_own_rack += self.tilerow.amount_of_letter_on_rack(
                    self.tilerow.tile_list, addition_letter
                )
                amount_in_bag += self._tilebag.get_amount_of_letter(
                    addition_letter
                ) + self.tilerow.amount_of_letter_on_rack(tilerow_opp, addition_letter)
            if amount_in_bag != 0:
                amount_in_bag -= (
                    (3 - self.get_score_difference() / 75)
                    * amount_on_own_rack
                    / amount_in_bag
                )
            else:
                amount_in_bag -= (
                    3 - self.get_score_difference() / 75
                ) * amount_on_own_rack
            if self._tilebag.get_amount_of_letters_remaining() > 0:
                amount_in_bag *= 1 / (
                    self._tilebag.get_amount_of_letters_remaining() + 7
                )

            if (
                move_coordinates[0][0] - move_direction[0] >= 0
                and move_coordinates[0][1] - move_direction[1] >= 0
            ):
                multiplication_danger_on_preceding_tile: float = (
                    get_expected_multiplication(
                        (
                            move_coordinates[0][0] - move_direction[0],
                            move_coordinates[0][1] - move_direction[1],
                        ),
                        (move_direction[1], move_direction[0]),
                        self._board.game_board,
                    )
                )

                addition_danger += (
                    multiplication_danger_on_preceding_tile
                    * Globals.BOARDPOSITION_FACTORS["Addition_Danger"]
                    * amount_in_bag
                )
                # print('Voorvoegsels', multiplication_danger_on_preceding_tile * Globals.BOARDPOSITION_FACTORS["Addition_Danger"] * amount_in_bag)
                degradation_value_list.append(
                    multiplication_danger_on_preceding_tile
                    * Globals.BOARDPOSITION_FACTORS["Addition_Danger"]
                    * amount_in_bag
                )
        degradation_value += addition_danger
        danger_word_played_alongside: float = 0

        # the first letter of the main word
        first_tile: tuple[int, int] = move_coordinates[0]
        first_tile_set: tuple[int, int] = move_coordinates[0]
        for _ in range(
            first_tile_set[0] if move_direction == (1, 0) else first_tile_set[1], 0, -1
        ):
            if (
                first_tile[0] - move_direction[0] < 0
                or first_tile[1] - move_direction[1] < 0
            ):
                break
            elif (
                self._board.game_board[str(first_tile[0] - move_direction[0])][
                    str(first_tile[1] - move_direction[1])
                ]["tile_object"].letter
                in Globals.EMPTY_TILE
            ):
                break
            elif (
                self._board.game_board[str(first_tile[0] - move_direction[0])][
                    str(first_tile[1] - move_direction[1])
                ]["tile_object"].letter
                not in Globals.EMPTY_TILE
            ):
                first_tile = (
                    first_tile[0] - move_direction[0],
                    first_tile[1] - move_direction[1],
                )

        first_letter = self._board.game_board[str(first_tile[0])][str(first_tile[1])][
            "tile_object"
        ].letter
        # print(move_coordinates)
        # calculate danger of adding a word below the main word touching the first tile in the same direction
        danger_word_played_alongside = self.get_danger_word_played_alongside(
            self._achtervoegsels,
            first_letter,
            move_direction,
            (
                first_tile[0] + 1 if move_direction == (0, 1) else first_tile[0],
                first_tile[1] if move_direction == (0, 1) else first_tile[1] + 1,
            ),
        )
        degradation_value_list.append(danger_word_played_alongside)

        # calculate the danger of adding a word above the main word touching the first tile in the same direction
        danger_word_played_alongside = self.get_danger_word_played_alongside(
            self._voorvoegsels,
            first_letter,
            move_direction,
            (
                first_tile[0] - 1 if move_direction == (0, 1) else first_tile[0],
                first_tile[1] if move_direction == (0, 1) else first_tile[1] - 1,
            ),
        )
        degradation_value_list.append(danger_word_played_alongside)

        # determine the last letter of the main word
        last_tile_set: tuple[int, int] = move_coordinates[-1]
        last_tile: tuple[int, int] = last_tile_set
        for _ in range(
            last_tile_set[0] if move_direction == (1, 0) else last_tile_set[1], 0, 1
        ):
            if (
                last_tile[0] + move_direction[0] > 14
                or last_tile[1] + move_direction[1] > 14
            ):
                break
            elif (
                self._board.game_board[str(last_tile[0] + move_direction[0])][
                    str(last_tile[1] + move_direction[1])
                ]["tile_object"].letter
                in Globals.EMPTY_TILE
            ):
                break
            elif (
                self._board.game_board[str(last_tile[0] + move_direction[0])][
                    str(last_tile[1] + move_direction[1])
                ]["tile_object"].letter
                not in Globals.EMPTY_TILE
            ):
                last_tile = (
                    last_tile[0] + move_direction[0],
                    last_tile[1] + move_direction[1],
                )

        last_letter = self._board.game_board[str(last_tile[0])][str(last_tile[1])][
            "tile_object"
        ].letter

        # calculate the danger of adding a word below the main word touching the last tile in the same direction
        danger_word_played_alongside = self.get_danger_word_played_alongside(
            self._achtervoegsels,
            last_letter,
            move_direction,
            (
                last_tile[0] + 1 if move_direction == (0, 1) else last_tile[0],
                last_tile[1] if move_direction == (0, 1) else last_tile[1] + 1,
            ),
        )
        degradation_value_list.append(danger_word_played_alongside)

        # calculate the danger of adding a word above the main word touching the last tile in the same direction
        danger_word_played_alongside = self.get_danger_word_played_alongside(
            self._voorvoegsels,
            last_letter,
            move_direction,
            (
                last_tile[0] - 1 if move_direction == (0, 1) else last_tile[0],
                last_tile[1] if move_direction == (0, 1) else last_tile[1] - 1,
            ),
        )
        degradation_value_list.append(danger_word_played_alongside)
        # print('danger alongside:', danger_word_played_alongside)
        degradation_value += danger_word_played_alongside
        # print('totaal:', degradation_value)
        degradation_value = 0
        degradation_value_list.sort(reverse=True)
        # if main_word == "QUORN":
        #    print(degradation_value_list)
        for i in range(len(degradation_value_list)):
            if i % 2 == 0:
                degradation_value += degradation_value_list[i] * 0.8**i
            else:
                degradation_value -= degradation_value_list[i] * 0.8**i

        return degradation_value

    def get_danger_word_played_alongside(
        self,
        fixdict: dict[str, str],
        letter: str,
        check_direction: tuple[int, int],
        tile_coordinates: tuple[int, int],
    ) -> float:
        danger_word_played_alongside: float = 0
        found_fixes: Literal[-1] | str = fixdict.get(letter, -1)

        if found_fixes != -1:
            additions: list[str] = [char for char in found_fixes]

            tilerow_opponent: list[str] = (
                Globals.players_tilerows[1]
                if self._player_id == 1
                else Globals.players_tilerows[2]
            )
            amount_on_own_rack = 0
            amount_in_bag = 0
            for addition_letter in additions:
                amount_on_own_rack += self.tilerow.amount_of_letter_on_rack(
                    self.tilerow.tile_list, addition_letter
                )
                amount_in_bag += self._tilebag.get_amount_of_letter(
                    addition_letter
                ) + self.tilerow.amount_of_letter_on_rack(
                    tilerow_opponent, addition_letter
                )
            if amount_in_bag != 0:
                amount_in_bag -= (
                    (3 - self.get_score_difference() / 75)
                    * amount_on_own_rack
                    / amount_in_bag
                )
            else:
                amount_in_bag -= (
                    3 - self.get_score_difference() / 75
                ) * amount_on_own_rack
            if self._tilebag.get_amount_of_letters_remaining() > 0:
                amount_in_bag *= 1 / (
                    self._tilebag.get_amount_of_letters_remaining() + 7
                )

            multiplication_danger_last_tile_above: float = get_expected_multiplication(
                tile_coordinates, check_direction, self._board.game_board
            )

            danger_word_played_alongside += (
                multiplication_danger_last_tile_above
                * Globals.BOARDPOSITION_FACTORS["danger_word_played_alongside"]
                * amount_in_bag
            )

        return danger_word_played_alongside

    def get_score_difference(self) -> int:
        own_score: int = (
            self._sidebar.score_object.bot_score
            if self._player_id == 1
            else self._sidebar.score_object.player_score
        )
        opponent_score: int = (
            self._sidebar.score_object.player_score
            if self._player_id == 1
            else self._sidebar.score_object.bot_score
        )
        difference: int = own_score - opponent_score
        return difference

    def skip_array(
        self, row_or_column: Literal["row", "column"], array_index: int
    ) -> bool:
        used_arrays = (
            self._board.used_rows
            if row_or_column == "row"
            else self._board.used_columns
        )
        if used_arrays[array_index]:
            return False
        if array_index - 1 >= 0:
            if used_arrays[array_index - 1]:
                return False
        if array_index + 1 <= 14:
            if used_arrays[array_index + 1]:
                return False
        if array_index == 7:
            return False
        return True

    def countFrequencyOfEachLetterType(self, string: str) -> list[int]:
        freq: list[int] = [0 for _ in range(0, 26)]
        for letter in string:
            letterIndex = ord(letter) - ord("A")
            freq[letterIndex] += 1
        return freq

    def letterTypesInWord(self, string: str) -> int:
        res: int = 0
        for letter in string:
            letterIndex: int = ord(letter) - ord("A")
            res = res | (1 << letterIndex)
        return res  # returns an integer which, when converted to binary, tells for each letter indexed 0-26 whether they are in the string

    def hasLetterTypes(self, neededLetterTypes: int, hasTheseLetterTypes: int) -> bool:
        return (neededLetterTypes & hasTheseLetterTypes) == neededLetterTypes

    def hasNeededLetters(
        self, checklist: list[int], needFreq: list[int], hasFreq: list[int], blanks: int
    ) -> bool:
        for i in checklist:
            i = int(i)
            if needFreq[i] > hasFreq[i]:
                need = needFreq[i] - hasFreq[i]
                blanks -= need
                if blanks < 0:
                    return False
        return True

    def countBlanks(self) -> int:
        blanks: int = 0
        for tile in self.tilerow.tile_list:
            if tile == " ":
                blanks += 1
        return blanks

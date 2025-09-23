import pygame
from bot import Bot
from globals import Globals
from tilebagclass import TileBag
from boardclass import Board
from sidebar import SideBar
from tileclass import BoardTile
from botmove import BotMoveObject
import time
pygame.init()
empty_tile: set = {None, "DW", "DL", "TW", "TL", ""}


class CompetitionBot(Bot):
    def __init__(
        self, tilebag: TileBag, board: Board, sidebar: SideBar, wordlist: list[str], player_id: int
    ):
        self._tilebag: TileBag = tilebag
        self._board: Board = board
        self._sidebar = sidebar
        self._wordlist = wordlist
        self._player_id: int = player_id
        self._letterFreqs: dict[str, list] = {}
        self._checkList: dict[str, list] = {}
        self._letterTypes: list[int] = [None for _ in range(len(self._wordlist))]

        i: int = 0
        for word in self._wordlist:
            self._letterFreqs[str(i)] = self.countFrequencyOfEachLetterType(word)
            self._checkList[str(i)] = [
                index for index in range(0, 26) if self._letterFreqs[str(i)][index] > 0
            ]
            self._letterTypes[i] = self.letterTypesInWord(word)
            i += 1

        super().__init__(self._tilebag, self._board, self._sidebar)

    def getGreedyMove(self) -> BotMoveObject:
        attempt_called: int = 0
        possible_moves_list: list[BotMoveObject] = []
        best_move_greedy: BotMoveObject = BotMoveObject([], [], [], (), 0)
        for row in self._board.game_board:
            skip_row: bool = True
            if self._board._used_rows[int(row)]:
                skip_row = False
            if int(row) - 1 >= 0:
                if self._board._used_rows[int(row) - 1]:
                    skip_row = False
            if int(row) + 1 <= 14:
                if self._board._used_rows[int(row) + 1]:
                    skip_row = False
            if self._board._is_first_turn and int(row) == 7:
                skip_row = False
            if not skip_row:
                tiles_in_row: str = ""
                for tile in self._board.game_board[row].values():
                    tiles_in_row += (
                        tile["tile_object"].letter
                        if tile["tile_object"].letter not in empty_tile
                        else ""
                    )
                filtered_wordlist: list[str] = self.filter(tiles_in_row)
                for word in filtered_wordlist:
                    for tile in self._board.game_board[row].values():
                        attempt_called += 1
                        attempt = self.try_word_on_tile(
                            word, tile["tile_object"], (0, 1), tiles_in_row
                        )
                        if attempt:
                            attempt_object = BotMoveObject(
                                attempt[3], attempt[1], attempt[2], (0, 1), attempt[0]
                            )
                            #print(
                            #    f"attempt success horizontal: words {attempt[1]}; letters {attempt[3]}; score {attempt[0]}; coordinates {attempt[2]}"
                            #)
                            possible_moves_list.append(attempt_object)
                            if attempt[0] > best_move_greedy.score:
                                best_move_greedy = attempt_object

        for column_index in range(0, 15):
            skip_column: bool = True
            if self._board._used_columns[column_index]:
                skip_column = False
            if column_index - 1 >= 0:
                if self._board._used_columns[column_index]:
                    skip_column = False
            if column_index + 1 <= 14:
                if self._board._used_columns[column_index]:
                    skip_column = False
            if self._board._is_first_turn and column_index == 7:
                skip_column = False
            if not skip_column:
                tiles_in_column: str = ""
                for row in self._board.game_board.values():
                    tiles_in_column += (
                        row[str(column_index)]["letter"]
                        if row[str(column_index)]["letter"]
                        not in empty_tile
                        else ""
                    )
                filtered_wordlist: list[str] = self.filter(tiles_in_column)
                column_list: list[BoardTile] = [
                    self._board.game_board[str(row_index)][str(column_index)][
                        "tile_object"
                    ]
                    for row_index in range(0, 15)
                ]
                for word in filtered_wordlist:
                    for tile in column_list:
                        attempt_called += 1
                        attempt = self.try_word_on_tile(word, tile, (1, 0), tiles_in_column)
                        if attempt:
                            attempt_object = BotMoveObject(
                                attempt[3], attempt[1], attempt[2], (1, 0), attempt[0]
                            )
                            #print(
                            #    f"attempt success vertical: words {attempt[1]}; letters {attempt[3]}; score {attempt[0]}; coordinates {attempt[2]}"
                            #)
                            possible_moves_list.append(attempt_object)
                            if attempt[0] > best_move_greedy.score:
                                best_move_greedy = attempt_object

        return best_move_greedy

    def competition_bot_play(self):
        pygame.display.flip()
        best_move = self.getGreedyMove()
        print(
            f"best move\nwords: {best_move.move_attempted_words};\nscore: {best_move.score};\nletters: {best_move.move_attempted_letters};\ncoordinates {best_move.move_coordinates}"
        )
        played_tiles: list[str] = best_move.move_attempted_letters
        letters_to_coordinates: list[tuple[str, tuple[int, int]]] = []
        for index in range(len(played_tiles)):
            letters_to_coordinates.append(
                (played_tiles[index], best_move.move_coordinates[index])
            )
        cross_off_tilerow: list[str] = self._tilerow._tile_list.copy()
        move_failed: bool = False
        blanks_coordinates: list[tuple[int, int]] = []
        print(cross_off_tilerow)
        for tile in letters_to_coordinates:
            if tile[0] in cross_off_tilerow:
                cross_off_tilerow.remove(tile[0])
            elif not tile[0] in cross_off_tilerow:
                if " " in cross_off_tilerow:
                    cross_off_tilerow.remove(" ")
                    blanks_coordinates.append(tile[1])
                else:
                    print(f"move failed: more blanks used than possible with tilerow, failed on tile '{tile[0]}")
                    move_failed = True
        if not move_failed and best_move.score > 0:
            self._board.bot_play_word(
                best_move.move_coordinates,
                best_move.move_attempted_letters,
                blanks_coordinates,
            )
            self._tilerow.get_new_letters(best_move.move_attempted_letters)
            if self._player_id == 1:
                self._sidebar._score_object.bot_score += best_move.score
            elif self._player_id == 2:
                self._sidebar._score_object.player_score += best_move.score
            Globals.amount_of_passes = 0
        else:
            print("no move found, bot passes")
            Globals.amount_of_passes += 1
            pass  # bot passes; gets more options during further development for tactical bots
        pygame.display.flip()
        time.sleep(1)
    
    def try_word_on_tile(
        self, word: str, tile: BoardTile, direction: tuple[int, int], tiles_in_array: str
    ) -> bool | tuple[int, list[str], list[tuple[int, int]], list[str]]:
        if self.ends_out_of_bounds(tile, direction, word):
            return False

        opposite_direction: tuple[int, int] = (1, 0) if direction == (0, 1) else (0, 1)
        
        if self.touches_no_tiles(tile, direction, opposite_direction, word):
            return False
        
        if self.word_has_letters_before_or_after(tile, direction, word):
            return False

        rearrange_tiles_results: bool | tuple[list[tuple[int,int]], list[str]] = self.rearranges_tiles(tile, direction, word, tiles_in_array)
        if rearrange_tiles_results == True:
            return False
        word_attempt_tiles, word_attempt_letters = rearrange_tiles_results
        
        points_results = self.get_points_and_attempted_words(tile, direction, opposite_direction, word, word_attempt_letters, word_attempt_tiles)
        if not points_results:
            return False
        total_points, attempted_words = points_results
        if total_points == 0:
            return False
        return (total_points, attempted_words, word_attempt_tiles, word_attempt_letters)

    def ends_out_of_bounds(self, tile: BoardTile, direction: tuple[int,int], word: str) -> bool:
        if (
            tile._board_coordinates[0] + direction[0] * len(word) > 14
            or tile._board_coordinates[1] + direction[1] * len(word) > 14
        ):
            #            print(f"word {word}; ends out of bounds: {(tile._board_coordinates[0] + direction[0] * len(word), tile._board_coordinates[1] + direction[1] * len(word))}; start tile {tile._board_coordinates}; direction {direction}")
            return True  # word goes out of field bounds
        return False
    
    def word_has_letters_before_or_after(self, tile: BoardTile, direction: tuple[int,int], word: str) -> bool:
        if (
            tile._board_coordinates[0] - direction[0] != -1
            and tile._board_coordinates[1] - direction[1] != -1
        ):
            if (
                self._board.game_board[str(tile._board_coordinates[0] - direction[0])][
                    str(tile._board_coordinates[1] - direction[1])
                ]["tile_object"].tile_type
                == "Set_board/Base_tilerow"
            ):
                #                print(f"word {word}; has letter before it; starting tile {tile._board_coordinates}; direction {direction}")
                return True  # the attempted word has a letter before it

        if (
            tile._board_coordinates[0] + direction[0] * (len(word) + 1) != 15
            and tile._board_coordinates[1] + direction[1] * (len(word) + 1) != 15
        ):
            if (
                self._board.game_board[
                    str(tile._board_coordinates[0] + direction[0] * (len(word) + 1))
                ][str(tile._board_coordinates[1] + direction[1] * (len(word) + 1))][
                    "tile_object"
                ].tile_type
                == "Set_board/Base_tilerow"
            ):
                #                print(f"word {word}; has letter behind it; starting tile {tile._board_coordinates}; direction {direction}")
                return True  # the attempted word has a letter behind it
        return False
    
    def rearranges_tiles(self, tile: BoardTile, direction: tuple[int,int], word: str, tiles_in_array: str) -> bool | tuple[list[tuple[int,int]], list[str]]:
        current_board_state: str = (
            ""  # the word currently formed by the entire row or column the word is placed in, with blank tiles represented as "_"
        )
        starting_coordinates: tuple[int, int] = (
            tile._board_coordinates[0] * (1 - direction[0]),
            tile._board_coordinates[1] * (1 - direction[1]),
        )
        # if horizontal: direction == (0,1) -> starting coordinates = (tile[0] * 1, tile[1] * 0) = (tile[0], 0)
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
        #        print(f"starting tile {starting_coordinates}; word {word}; direction {direction}; array: {current_board_state}")
        for index in range(
            0,
            int(
                (
                    tile._board_coordinates[0] ** 2 * direction[0]
                    + tile._board_coordinates[1] ** 2 * direction[1]
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
                    #print(f"{word} starting at {tile._board_coordinates} with direction {direction} replaces or reassigns previously occupied tiles")
                    return True  # replacing previously filled tiles with either other letters or empty is not allowed
        for index in range(0, tiles_before_word):
            letter = self._board.game_board[str(starting_coordinates[0] + index * direction[0])][str(starting_coordinates[1] + index * direction[1])]["tile_object"].letter
            if letter not in empty_tile: letters_required_with_word_placement += letter
        for letter in word:
            letters_required_with_word_placement += letter
        for index in range(tiles_before_word + len(word), 15):
            letter = self._board.game_board[str(starting_coordinates[0] + index * direction[0])][str(starting_coordinates[1] + index * direction[1])]["tile_object"].letter
            if letter not in empty_tile: letters_required_with_word_placement += letter
        #letters_available: list[str] = [char for char in tiles_in_array].extend(self._tilerow._tile_list)
        letters_available = [char for char in tiles_in_array]
        for letter in self._tilerow._tile_list:
            letters_available.append(letter)
        letters_required: str = "".join(letters_required_with_word_placement)
        for letter in letters_required:
            if letter in letters_available:
                letters_available.remove(letter) #cross off letters to prevent double use
            elif not letter in letters_available:
                if " " in letters_available:
                    letters_available.remove(" ")
                else:
                    return True #letters have been allocated from outside of the word range to inside, creating doubles
        return (word_attempt_tiles, word_attempt_letters)
    
    def touches_no_tiles(self, tile: BoardTile, direction: tuple[int,int], opposite_direction: tuple[int,int], word: str) -> bool:
        index = 0
        lies_on_no_letters: bool = True
        has_no_adjacent_letters: bool = True
        while index < len(word):
            check_tile_coordinate: tuple[int, int] = (
                tile._board_coordinates[0] + direction[0] * index,
                tile._board_coordinates[1] + direction[1] * index,
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
            #            print(f"word {word}; has no adjacent letters or touches no letters; starting tile {tile._board_coordinates}")
            return True  # the attempted word has no adjacent tiles and does not lie on any already used tile
        return False
    
    def get_points_and_attempted_words(self, tile: BoardTile, direction: tuple[int,int], opposite_direction: tuple[int,int], word: str, word_attempt_letters: list[str], word_attempt_tiles: list[tuple[int,int]]):
        total_points: int = 0
        attempted_words: list[str] = []
        attempted_words.append(word)
        first_tile_coordinates: tuple[int, int] = (14, 14)
        for index in range(0, len(word)):
            tile_object = self._board.game_board[
                str(tile._board_coordinates[0] + direction[0] * index)
            ][str(tile._board_coordinates[1] + direction[1] * index)]["tile_object"]
            if tile_object.tile_type != "Set_board/Base_tilerow":
                tile_object.letter = word[index]
                tile_object.tile_type = "Try_board/Selected_tilerow"
        set_tiles_list: list[tuple[int, int]] = [
            (
                tile._board_coordinates[0] + index * direction[0],
                tile._board_coordinates[1] + index * direction[1],
            )
            for index in range(len(word))
            if self._board.game_board[
                str(tile._board_coordinates[0] + index * direction[0])
            ][str(tile._board_coordinates[1] + index * direction[1])][
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
        cross_off_tilerow = self._tilerow._tile_list.copy()
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
            attempted_words.append(main_word)
            total_points += main_word_value
        for tile in set_tiles_list:
            word_created, word_value = self._board.get_word_from_tile(
                tile, opposite_direction, set_tiles_list, blank_coordinates
            )
            if len(word_created) > 1:
                if not self._board._word_tree.search_word(word_created):
                    self._board.reset_tiles(set_tiles_list)
                    return False
                attempted_words.append(word_created)
                total_points += word_value
        if len(set_tiles_list) == 7:
            total_points += 40  # add 40 for all tiles set
        self._board.reset_tiles(set_tiles_list)

        return (total_points, attempted_words)
    
    def filter(self, letters_on_selected: str):
        blanks: int = 0
        for tile in self._tilerow._tile_list:
            if tile == " ":
                blanks += 1
        tilerow2 = [tile for tile in self._tilerow._tile_list if tile != " "]
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
        self, checklist: list[int], needFreq, hasFreq, blanks: int
    ) -> bool:
        for i in checklist:
            i = int(i)
            if needFreq[i] > hasFreq[i]:
                need = needFreq[i] - hasFreq[i]
                blanks -= need
                if blanks < 0:
                    return False
        return True

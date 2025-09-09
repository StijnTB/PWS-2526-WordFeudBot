from bot import Bot
from tilebagclass import TileBag
from boardclass import Board
from sidebar import SideBar
from tileclass import BoardTile
from botmove import BotMoveObject

empty_tile: set = {None, "DW", "DL", "TW", "TL", ""}


class CompetitionBot(Bot):
    def __init__(
        self, tilebag: TileBag, board: Board, sidebar: SideBar, wordlist: list[str]
    ):
        self._tilebag: TileBag = tilebag
        self._board: Board = board
        self._sidebar = sidebar
        self._wordlist = wordlist

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
        possible_moves_list: list[BotMoveObject] = []
        best_move_greedy: BotMoveObject = BotMoveObject([], [], [], (), 0)
        for row in self._board.game_board.values():
            tiles_in_row: str = ""
            for tile in row.values():
                tiles_in_row += (
                    tile["tile_object"].letter
                    if tile["tile_object"].letter not in empty_tile
                    else ""
                )
            filtered_wordlist: list[str] = self.filter(tiles_in_row)
            #print(f"filtered wordlist: {filtered_wordlist}")
            for word in filtered_wordlist:
                for tile in row.values():
                    attempt = self.try_word_on_tile(word, tile["tile_object"], (0, 1))
                    if attempt:
                        #print(f"attempt {attempt[1]} horizontal is success")
                        attempt_object = BotMoveObject(
                            attempt[3], attempt[1], attempt[2], (0, 1), attempt[0]
                        )
                        possible_moves_list.append(attempt_object)
                        #print(f"Candidate: {word}, score={attempt[0]}, coords={attempt[2]}")
                        if attempt[0] > best_move_greedy.score:
                            best_move_greedy = attempt_object
        for column_index in range(0, 15):
            tiles_in_column: str = ""
            for row in self._board.game_board.values():
                tiles_in_column += (
                    row[str(column_index)]["letter"]
                    if row[str(column_index)]["letter"]
                    not in (None, "DW", "TW", "DL", "TL", "")
                    else ""
                )
            filtered_wordlist: list[str] = self.filter(tiles_in_column)
            column_list: list[BoardTile] = [
                self._board.game_board[str(row_index)][str(column_index)]["tile_object"]
                for row_index in range(0, 15)
            ]
            for word in filtered_wordlist:
                for tile in column_list:
                    attempt = self.try_word_on_tile(word, tile, (1, 0))
                    if attempt:
                        #print(f"attempt {attempt[1]} vertical is success")
                        attempt_object = BotMoveObject(
                            attempt[3], attempt[1], attempt[2], (1, 0), attempt[0]
                        )
                        possible_moves_list.append(attempt_object)
                        if attempt[0] > best_move_greedy.score:
                            best_move_greedy = attempt_object

        return best_move_greedy

    def competition_bot_play(self):
        best_move = self.getGreedyMove()
        print("Rack:", self._tilerow._tile_list)
        print("Best move:", best_move.move_attempted_words, best_move.score)
        print(f"best move words: {best_move.move_attempted_words}")
        print(best_move.move_coordinates)
        print(best_move.move_attempted_letters)
        print(best_move.score)
        if best_move.score > 0:
            self._board.bot_play_word(
                best_move.move_coordinates, best_move.move_attempted_letters
            )
            self._tilerow.get_new_letters(best_move.move_attempted_letters)
            self._sidebar._score_object.bot_score += best_move.score
        else:
            print("no move found, bot passes")
            pass  # bot passes; gets more options during further development for tactical bots

    def try_word_on_tile(
        self, word: str, tile: BoardTile, direction: tuple[int, int]
    ) -> bool | tuple[int, list[str], list[tuple[int, int]], list[str]]:
        if (
            tile._board_coordinates[0] + direction[0] * len(word) > 14
            or tile._board_coordinates[1] + direction[1] * len(word) > 14
        ):
            #            print(f"word {word}; ends out of bounds: {(tile._board_coordinates[0] + direction[0] * len(word), tile._board_coordinates[1] + direction[1] * len(word))}; start tile {tile._board_coordinates}; direction {direction}")
            return False  # word goes out of field bounds

        index: int = 0
        has_no_adjacent_letters: bool = True
        lies_on_no_letters: bool = True
        opposite_direction: tuple[int, int] = (1, 0) if direction == (0, 1) else (0, 1)
        while index < len(word):
            check_tile_coordinate: tuple[int, int] = (
                tile._board_coordinates[0] + direction[0] * index,
                tile._board_coordinates[1] + direction[1] * index,
            )
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
            return False  # the attempted word has no adjacent tiles and does not lie on any already used tile

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
                return False  # the attempted word has a letter before it

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
                return False  # the attempted word has a letter behind it

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
        print(f"attempted word: {attempted_word_as_state}, current_board_state: {current_board_state}")
        for index in range(0, 15):
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
                if current_board_state[index] != "_" and current_board_state[index] != attempted_word_as_state[index]:
                    #                    print(f"{word} starting at {tile._board_coordinates} with direction {direction} replaces or reassigns previously occupied tiles")
                    return False  # replacing previously filled tiles with either other letters or empty is not allowed

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

        main_word, main_word_value = self._board.get_word_from_tile(
            first_tile_coordinates, direction, set_tiles_list
        )
        #print(main_word_value)
        if len(main_word) > 1:
            attempted_words.append(main_word)
            total_points += main_word_value
        for tile in set_tiles_list:
            word_created, word_value = self._board.get_word_from_tile(
                tile, opposite_direction, set_tiles_list
            )
            if len(word_created) > 1:
                if not self._board._word_tree.search_word(word_created):
                    #print(f"secondary word {word_created} not found")
                    self._board.reset_tiles(set_tiles_list)
                    return False
                attempted_words.append(word_created)
                total_points += word_value
                
        if len(set_tiles_list) == 7:
            total_points += 40  # add 40 for all tiles set
        self._board.reset_tiles(set_tiles_list)
        #print(f"attempted words: {attempted_words}")
        if not word_attempt_tiles:
            return False
        
        return (total_points, attempted_words, word_attempt_tiles, word_attempt_letters)

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
        print("Filter in:", letters_on_selected, "->", len(res), "woorden")
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

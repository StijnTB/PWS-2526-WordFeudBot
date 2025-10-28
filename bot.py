from globals import *
from boardclass import Board
from tilebagclass import TileBag
from tileclass import *
from tilerowclass import BotTileRow


class Bot:
    def __init__(
        self,
        tilebag: TileBag,
        board: Board,
    ):
        self._game_board = board
        self._tilebag = tilebag
        self._tilerow: BotTileRow = BotTileRow(self._tilebag)
        self._is_turn: bool = True

    def play(self):
        print("bot turn")
        self._is_turn = True
        while self._is_turn:
            pass

    @property
    def tilerow(self) -> BotTileRow:
        return self._tilerow

from typing import TypedDict


class BotMovePropertiesDict(TypedDict):
    letters: list[str]
    words: list[str]
    coordinates: list[tuple[int, int]]
    direction: tuple[int, int]
    base_score: int
    bingo_bonus_score: float
    position_degradation_score: float
    total_score: float


class BotMoveObject:
    def __init__(
        self,
        move_attempted_letters: list[str],
        move_attempted_words: list[str],
        move_coordinates: list[tuple[int, int]],
        move_direction: tuple[int, int],
        attempt_score: int,
        bingo_bonus_score: float = 0,
        position_degradation_score: float = 0,
    ):
        self._move_attempted_letters: list[str] = move_attempted_letters
        self._move_attempted_words: list[str] = move_attempted_words
        self._move_coordinates: list[tuple[int, int]] = move_coordinates
        self._move_direction: tuple[int, int] = move_direction
        self._score: int = attempt_score
        self._bingo_bonus_score: float = bingo_bonus_score
        self._position_degradation_score: float = position_degradation_score
        self._properties: BotMovePropertiesDict = {
            "letters": self.move_attempted_letters,
            "words": self.move_attempted_words,
            "coordinates": self.move_coordinates,
            "direction": self.move_direction,
            "base_score": self.score,
            "bingo_bonus_score": self.bingo_bonus_score,
            "position_degradation_score": self.position_degradation_score,
            "total_score": (self.score + self.get_bingo_score()) - self.get_deg_score(),
        }

    @property
    def move_attempted_letters(self) -> list[str]:
        return self._move_attempted_letters

    @property
    def move_attempted_words(self) -> list[str]:
        return self._move_attempted_words

    @property
    def move_coordinates(self) -> list[tuple[int, int]]:
        return self._move_coordinates

    @property
    def move_direction(self) -> tuple[int, int]:
        return self._move_direction

    @property
    def score(self) -> int:
        return self._score

    @property
    def bingo_bonus_score(self) -> float:
        return self._bingo_bonus_score

    @bingo_bonus_score.setter
    def bingo_bonus_score(self, bingo_bonus_score: float) -> None:
        self._bingo_bonus_score = bingo_bonus_score

    @property
    def position_degradation_score(self) -> float:
        return self._position_degradation_score

    @position_degradation_score.setter
    def position_degradation_score(self, position_degradation_score: float) -> None:
        self._position_degradation_score = position_degradation_score

    @property
    def properties(self) -> BotMovePropertiesDict:
        self.recalculate_properties()
        return self._properties

    def get_deg_score(self) -> float:
        return self.position_degradation_score

    def get_bingo_score(self) -> float:
        return self.bingo_bonus_score

    def recalculate_properties(self) -> None:
        self._properties: BotMovePropertiesDict = {
            "letters": self.move_attempted_letters,
            "words": self.move_attempted_words,
            "coordinates": self.move_coordinates,
            "direction": self.move_direction,
            "base_score": self.score,
            "bingo_bonus_score": self.bingo_bonus_score,
            "position_degradation_score": self.position_degradation_score,
            "total_score": (self.score + self.get_bingo_score()) - self.get_deg_score(),
        }

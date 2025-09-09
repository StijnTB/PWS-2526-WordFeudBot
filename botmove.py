class BotMoveObject:
    def __init__(
        self,
        move_attempted_letters: list[str],
        move_attempted_words: list[str],
        move_coordinates: list[tuple[int, int]],
        move_direction: tuple[int, int],
        attempt_score: int,
    ):
        self._move_attempted_letters: list[str] = move_attempted_letters
        self._move_attempted_words: list[str] = move_attempted_words
        self._move_coordinates: list[tuple[int, int]] = move_coordinates
        self._move_direction: tuple[int, int] = move_direction
        self._score: int = attempt_score

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

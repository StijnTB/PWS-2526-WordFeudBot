import pygame

alphabet_list: list[str] = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
alphabet_indexes: dict[str, int] = {}
for index in range(0, 26):
    alphabet_indexes[alphabet_list[index]] = index


def floor(number: float) -> int:
    if round(number) - number > 0:
        return int(number - (round(number) - number))
    else:
        return round(number)


def ceil(number: float) -> int:
    if round(number) - number > 0:
        return round(number)
    else:
        return int(number - (round(number) - number))


def recalculate_letters(
    pygame_font: pygame.font.Font, text: str, central_coordinates: tuple[int, int]
):
    highest_letter_height: int = 0
    text_width: int = 0
    for letter_used in text:
        letter_width, letter_height = pygame_font.size(letter_used)
        text_width += letter_width
        if letter_height > highest_letter_height:
            highest_letter_height = letter_height
    text_coordinates: tuple = (
        central_coordinates[0] - floor(text_width / 2),
        central_coordinates[1] - floor(highest_letter_height / 2),
    )
    return text_coordinates


def calculate_text_dimensions(
    pygame_font: pygame.font.Font, text: str
) -> tuple[int, int]:
    highest_letter_height: int = 0
    text_width: int = 0
    for letter_used in text:
        letter_width, letter_height = pygame_font.size(letter_used)
        text_width += letter_width
        if letter_height > highest_letter_height:
            highest_letter_height = letter_height
    return (text_width, highest_letter_height)

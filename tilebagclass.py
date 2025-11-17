import random
from globals import *

random.seed(Globals.RANDOM_SEED)


class TileBag:
    def __init__(self) -> None:
        self._tile_bag_dict = Globals.TILE_LETTER_DICT
        self._bag_list: list[str] = []
        self.fill_bag()

    def fill_bag(self) -> None:
        for letter in self._tile_bag_dict:
            for _ in range(0, self._tile_bag_dict[letter]["amount"]):
                self._bag_list.append(letter)

    def grab_letters(self, amount_of_letters: int) -> list[str]:
        grabbed_letter_list: list[str] = []
        random.shuffle(self._bag_list)
        while amount_of_letters > 0:
            letter_grabbed = self._bag_list[0]
            self._bag_list.pop(0)
            grabbed_letter_list.append(letter_grabbed)
            amount_of_letters -= 1
        return grabbed_letter_list

    def swap_letters(self, returned_letters: list[str]) -> list[str]:
        amount_of_letters: int = len(returned_letters)
        grabbed_letters: list[str] = self.grab_letters(amount_of_letters)
        self._bag_list.extend(returned_letters)
        return grabbed_letters

    def get_amount_of_letters_remaining(self) -> int:
        return len(self._bag_list)
    
    def get_amount_of_letter(self, letter):
        return self._bag_list.count(letter)

    @property
    def bag_list(self) -> list[str]:
        return self._bag_list

    @bag_list.setter
    def bag_list(self, new_bag_list: list[str]) -> None:
        self._bag_list = new_bag_list

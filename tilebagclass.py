import pygame
import random
from globals import *


class TileBag:
    def __init__(self) -> None:
        self._tile_bag_dict = Globals.TILE_LETTER_DICT
        self._bag_list: list = []
        self.fill_bag()

    def fill_bag(self):

        for letter in self._tile_bag_dict:
            for i in range(0, self._tile_bag_dict[letter]["amount"]):
                self._bag_list.append(letter)

    def grab_letters(self, amount_of_letters: int) -> list:
        grabbed_letter_list = []
        random.shuffle(self._bag_list)
        while amount_of_letters > 0:
            letter_grabbed = self._bag_list[0]
            self._bag_list.pop(0)
            grabbed_letter_list.append(letter_grabbed)
            amount_of_letters -= 1
        return grabbed_letter_list

    def swap_letters(self, returned_letters: list) -> list:
        grabbed_letters: list = returned_letters
        if len(self._bag_list) >= 7:
            amount_of_letters: int = len(returned_letters)
            grabbed_letters = self.grab_letters(amount_of_letters)
            self._bag_list.extend(returned_letters)
        return grabbed_letters

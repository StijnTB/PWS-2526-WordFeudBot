class TRIENode:
    def __init__(self) -> None:
        self.children = {}
        self.is_word = False


class TRIE:
    def __init__(self):
        self.root = TRIENode()
        self._amount_of_words: int = 0

    def insert(self, word: str) -> None:
        word = word.upper()
        node = self.root
        if len(word) <= 15:
            for letter in word:
                if letter not in [
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
                ]:
                    return
            self._amount_of_words += 1
            for letter in word:
                if letter not in node.children:
                    node.children[letter] = TRIENode()
                node = node.children[letter]
            node.is_word = True

    def search_word(self, word: str) -> bool:
        node = self.root
        word = word.upper()
        for letter in word:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_word

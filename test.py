import Levenshtein
from kami.preprocessing.transformation import TextToSentences


class _WordRegister:
    """A simple dictionnary with auto-incremental index"""
    def __init__(self):
        self._register = {}

    def __getitem__(self, key):
        if key in self._register:
            val = self._register[key]
        else:
            self._register[key] = val = chr(0x0000 + len(self._register))
        return val

    def __str__(self):
        return f'Actual register : {self._register}'


def _hot_encode(word_lists: list) -> list:
    """Pre-process the truth and hypothesis into a words form that Levenshtein can handle.

    Take word_lists, transform them into hot-encoded strings.

    :Example:

    >>> list(hot_encode([["w1", "w2", "w3"], ["w4", "w5", "w1"]]))
    ['\x00\x01\x02', '\x03\x04\x00']

    :param word_lists: List of List of words (generally 2)
    :type word_lists: list
    :return: hot-encoded string
    :rtype: list
    """
    wtox = _WordRegister()
    for word_list in word_lists:
        yield "".join([wtox[word] for word in word_list])


reference = "Je m'appelle Mr. C est je, vais à Montpellier. Je prends le TGV. J'aime prendre le train."
prediction = ""

group = TextToSentences()([reference, prediction])

print(group)


lev_distance_sequences = Levenshtein.distance(*_hot_encode(
            [group[0], group[1]]))


total_sequences_ref = len(group[0])

ser = (lev_distance_sequences / total_sequences_ref) * 100

print(f'SER : {ser} %')



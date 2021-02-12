"""Common code for all metrics.
"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Contibutors : Thibault Clérice <thibault.clerice@chartes.psl.eu>
# Licence : MIT

import decimal

__all__ = [
    "WordRegister",
    "_hot_encode",
    "_truncate_score",
    "_get_percent"
]


class WordRegister:
    """A simple dictionnary with auto-incremental index"""
    def __init__(self):
        self._register = {}

    def __getitem__(self, key):
        if key in self._register:
            val = self._register[key]
        else:
            self._register[key] = val = chr(0x0000 + len(self._register))
        return val


def _hot_encode(word_lists):
    """ Pre-process the truth and hypothesis into a words form that Levenshtein can handle.

    Take word_lists, transform them into hot-encoded strings.

    >>> list(hot_encode([["w1", "w2", "w3"], ["w4", "w5", "w1"]]))
    ['\x00\x01\x02', '\x03\x04\x00']

    Args:
        word_list (list) : List of List of words (generally 2)
        wtox (dict) : Word Register object

    Returns:
        str : hot-encoded string

    """
    wtox = WordRegister()
    for word_list in word_lists:
        yield "".join([wtox[word] for word in word_list])



def _truncate_score(score, round):
    """truncate the result with predifined digits after the decimal point (does not display zeros)

    Args:
        score (float) : result of computation to truncate
        round (str) : number of digits after the decimal point (exemple format : ".001")

    Returns:
        float : result truncated
    """
    result_truncate = float(decimal.Decimal(score).quantize(decimal.Decimal(round),
                                                             rounding=decimal.ROUND_DOWN))
    return result_truncate


def _get_percent(score):
    """Make score in percentage format

    Args:
        score (float) : result of computation

    Returns:
        float : result in percentage
    """
    return score * 100


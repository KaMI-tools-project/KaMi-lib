# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Contibutors : Thibault Clérice
# Licence : MIT
"""Common code for all metrics.
"""

import decimal
from typing import Sequence, List

__all__ = [
    "_WordRegister",
    "_hot_encode",
    "_truncate_score",
    "_get_percent"
]


class _WordRegister:
    """A simple dictionnary with auto-incremental index"""
    def __init__(self):
        self._register = {}

    def __getitem__(self, key: str):
        if key in self._register:
            val = self._register[key]
        else:
            self._register[key] = val = chr(0x0000 + len(self._register))
        return val

    def __str__(self):
        return f'Actual register : {self._register}'


def _hot_encode(word_lists: Sequence[Sequence[str]]) -> List[str]:
    """Pre-process the truth and hypothesis into a words form that Levenshtein can handle.

    Take word_lists, transform them into hot-encoded strings.

    :Example:

    >>> list(_hot_encode([["w1", "w2", "w3"], ["w4", "w5", "w1"]]))
    ['\x00\x01\x02', '\x03\x04\x00']

    :param word_lists: List of List of words (generally 2)
    :type word_lists: list
    :return: hot-encoded string
    :rtype: list
    """
    wtox = _WordRegister()
    for word_list in word_lists:
        yield "".join([wtox[word] for word in word_list])


def _truncate_score(score: float, round_digits: str) -> float:
    """truncate the result with predifined digits after the decimal point (does not display zeros)

    :Exemple:

    >>> _truncate_score(3.1415926, round_digits='.001')
    3.141
    >>> _truncate_score(3.1415926, round_digits='.01')
    3.14

    :param score: result of computation to truncate
    :type score: float
    :param round_digits: number of digits after the decimal point (exemple format : ".001")
    :type round_digits: str
    :return: result truncated
    :rtype: float
    """
    result_truncate = float(
        decimal.Decimal(score).quantize(
            decimal.Decimal(round_digits),
            rounding=decimal.ROUND_DOWN))
    return result_truncate


def _get_percent(score: float) -> float:
    """Return score in percentage format

    :Example:

    >>> _get_percent(0.234)
    23.4

    :param score: result of computation
    :type: float
    :return: result in percentage
    :rtype: float
    """
    return score * 100

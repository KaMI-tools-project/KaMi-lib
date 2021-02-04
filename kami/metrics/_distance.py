#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Metrics to assess distance calculation

"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT

from .config_cdll import _distance_dll


def _levensthein_distance(reference, prediction):
    """

    """
    result_lev = _distance_dll.levenshtein(reference, prediction)
    return result_lev


def _hamming_distance(reference, prediction):
    """

    """
    if len(reference) != len(prediction):
        return 'Ø'
    else:
        result_hamming = _distance_dll.hamming(reference, prediction)
        return result_hamming


# Test :
if __name__ == '__main__':
    text1 = "Bonjour je suis un camembert"
    text2 = "Bonsoir je suis du cheedar"
    a = "100011"
    b = "100010"
    print(f'Result Lev : {_levensthein_distance(a, b)}')
    print(f'Result hamming : {_hamming_distance(a, b)}')
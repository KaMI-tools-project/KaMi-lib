#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Metrics to assess distance calculation
"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT


__all__ = [
    "_levensthein_distance",
    "_hamming_distance"
]


def _levensthein_distance(source, target):
    """

    """
    thisrow = list(range(1, len(target) + 1)) + [0]
    rows = [thisrow]
    for x in range(len(source)):
        oneago, thisrow = thisrow, [0] * len(target) + [x + 1]
        for y in range(len(target)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (source[x] != target[y])
            thisrow[y] = min(delcost, addcost, subcost)
        rows.append(thisrow)
    return thisrow[len(target) - 1]


def _hamming_distance(source, target):
    """

    """
    if len(source) != len(target):
        return 'Ø'
    else:
        result_hamming = 0
        for n in range(len(source)):
            if source[n] != target[n]:
                result_hamming += 1

        return result_hamming

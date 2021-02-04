#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common code for all metrics.

"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT


import decimal

def _truncate_score(score):
    """truncate the result to 2 digits after the decimal point (does not display zeros)

    Parameters
    ----------
    score : float, result of computation
        result of computation to truncate

    Returns:
        int : result truncate
    """
    result_truncate = float(decimal.Decimal(score).quantize(decimal.Decimal('.01'),
                                                             rounding=decimal.ROUND_DOWN))
    return result_truncate


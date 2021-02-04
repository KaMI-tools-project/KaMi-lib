#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Metrics to assess text recognition

"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT

from .config_cdll import _score_text_recognition_dll


def _word_error_rate(length_total_words_reference,
                     lev_distance):
    """

    """
    result_wer = _score_text_recognition_dll.wer(length_total_words_reference,
                                                 lev_distance)
    return result_wer


def _character_error_rate(length_total_char_reference,
                          lev_distance):
    """

    """
    result_cer = _score_text_recognition_dll.cer(length_total_char_reference,
                                                 lev_distance)
    return result_cer


def _word_accuracy(length_total_words_reference, lev_distance):
    """

    """
    result_wacc = _score_text_recognition_dll.wacc(length_total_words_reference,
                                                 lev_distance)
    return result_wacc

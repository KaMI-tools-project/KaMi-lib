import pytest
import unittest

from kami.metrics.evaluation import Scorer as kamiScorer

"""Run python -m pytest tests in root dir"""

class testMetrics(unittest.TestCase):
    reference = "Six semaines plus tard, Claude peignait un matin dans un flot de soleil qui tombait par la baie vitrée de l’atelier."
    prediction_same = "Six semaines plus tard, Claude peignait un matin dans un flot de soleil qui tombait par la baie vitrée de l’atelier."
    prediction_change = "Six semaiNEs plus tard, lCCaude peignait un MA dans un flotille de soleil qui tombait baie vitrée de l’atelier."
    prediction_empty = ""
    my_scorer_1 = kamiScorer(reference, prediction_same, show_percent=True, truncate_score=True, round_digits='.001')
    my_scorer_2 = kamiScorer(reference, prediction_change, show_percent=True, truncate_score=True, round_digits='.001')
    my_scorer_3 = kamiScorer(reference, prediction_empty, show_percent=True, truncate_score=True, round_digits='.001')

    def test_success_with_same_string(self):
        assert self.my_scorer_1.board == {'levensthein_distance_char': 0,
                                     'levensthein_distance_words': 0,
                                     'hamming_distance': 0,
                                     'wer': 0.0,
                                     'cer': 0.0,
                                     'wacc': 100.0,
                                     'mer': 0.0,
                                     'cil': 0.0,
                                     'cip': 100.0,
                                     'hits': 116,
                                     'substitutions': 0,
                                     'deletions': 0,
                                     'insertions': 0}

    def test_success_with_change_string(self):
        assert self.my_scorer_2.board == {'levensthein_distance_char': 20,
                                          'levensthein_distance_words': 6,
                                          'hamming_distance': 'Ø',
                                          'wer': 28.571,
                                          'cer': 17.241,
                                          'wacc': 71.428,
                                          'mer': 16.528,
                                          'cil': 20.775,
                                          'cip': 79.224,
                                          'hits': 101,
                                          'substitutions': 5,
                                          'deletions': 10,
                                          'insertions': 5}


    def test_success_with_empty_string(self):
        assert self.my_scorer_3.board == {'levensthein_distance_char': 116,
                                          'levensthein_distance_words': 21,
                                          'hamming_distance': 'Ø',
                                          'wer': 100.0,
                                          'cer': 100.0, 'wacc': 0.0,
                                          'mer': 100.0, 'cil': 0.0,
                                          'cip': 0,
                                          'hits': 0,
                                          'substitutions': 0,
                                          'deletions': 116,
                                          'insertions': 0}


    # TODO(Luca) : test with no strings

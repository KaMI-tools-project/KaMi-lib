#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
# Author : Lucas Terriel <lucas.terriel@inria.fr>
# License : MIT

from kami.metrics._distance import (_levensthein_distance,
                                    _hamming_distance)

from kami.metrics._score_text_recognition import (_word_error_rate,
                                                  _character_error_rate,
                                                  _word_accuracy)

class Scorer():
    """

    """
    def __init__(self, reference, hypothesis):
        self.source = reference
        self.target = hypothesis
        self.length_reference = len(reference)
        self.length_hypothesis = len(hypothesis)
        self.tokens_word_reference = reference.split(" ")
        self.tokens_char_reference = list(reference)
        self.length_words_reference = len(self.tokens_word_reference)
        self.length_char_reference = len(self.tokens_char_reference)

    def distance(self, type):
        """

        :param type:
        :return:
        """
        if type == 'levensthein':
            return _levensthein_distance(self.source,
                                         self.target)
        if type == 'hamming':
            return _hamming_distance(self.source,
                                     self.target)


    def text_recognition_metrics(self,
                                 type):
        """

        :param type:
        :return:
        """
        distance_lev = _levensthein_distance(self.source,
                                             self.target)

        #TODO levensethein and hamming as attribute and text recognition as method
        if type == 'wer':
            return _word_error_rate(self.length_words_reference,
                                    distance_lev)
        if type == 'cer':
            return _character_error_rate(self.length_char_reference,
                                         distance_lev)
        if type == 'wacc':
            return _word_accuracy(self.length_words_reference,
                                  distance_lev)

# each file with class
"""
class Parser():
    pass

class Transcriber():
    pass

class vizualizer():
    pass
    
"""
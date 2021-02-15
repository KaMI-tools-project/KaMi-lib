# -*- coding: utf-8 -*-

"""Metrics to assess text recognition (OCR/HTR)
"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT

import Levenshtein

from ._base import (_truncate_score,
                    _hot_encode,
                    _get_percent)

__all__ = [
    "Scorer",
]


class Scorer:
    """Global class to compute classic HTR/OCR metrics.

    Args:
        reference (str): Human readable string describing
                        the reference to compare with
                        prediction (ground truth).
        prediction (str): Human readable string describing the
                        prediction to compare with reference.
        show_percent (:obj:`bool`, optional): To pass final scores
                                            in percentage. Defaults
                                            to False.
        truncate_score (:obj:`bool`, optional): To truncate final
                                            score. Defaults to False.
        round_digits (:obj:`str`, optional): To set the number of digits
                                    after the decimal point.
                                    Defaults to ".01".

    Attributes:
        opt_percent (bool): User option on percentage.
        opt_truncate (bool): User option on truncate.
        round_digits (str): User option set type of truncate.
        reference (str): User reference string.
        prediction (str): User prediction string.
        length_char_reference (int): Total characters in reference string.
        length_char_prediction (int): Total characters in prediction string.
        length_words_reference (int): Total words in reference string.
        length_words_prediction (int): Total words in prediction string.
        lev_distance_words (int): Levensthein distance on words.
        lev_distance_char (int): Levensthein distance on characters.
        hamming (str or float): Hamming distance.
        wer (float): Word error rate.
        cer (float): Character error rate.
        wacc (float): Word accuracy.
        H (int): Total number of Hints between reference and prediction.
        S (int): Total number of Substitutions between reference and prediction.
        D (int): Total number of Deletions between reference and prediction.
        I (int): Total number of Insertions between reference and prediction.
        cip (float): Character information preserve.
        cil (float): Character information lost.
        mer (float): Match error rate.
        board (dict): A general board of all above metrics in
                     key (name of metric) / value (score) struct
    """

    # Collection of distance metrics #

    def _levensthein_distance(self):
        """C extension module to compute Levensthein distance
        from Python-Levensthein

        See also : https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : result of Levensthein distance on words
            int : result of Levensthein distance on characters
        """
        # Computes levensthein on words level
        lev_distance_words = Levenshtein.distance(*_hot_encode(
            [self.reference.split(), self.prediction.split()]
        )
                                      )
        # Computes levensthein on char level
        lev_distance_char = Levenshtein.distance(self.reference, self.prediction)

        return lev_distance_words, lev_distance_char

    def _hamming_distance(self):
        """C extension module to compute Hamming distance on two strings of same
        length from Python-Levensthein

        See also : https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : result of hamming distance or Ø if two strings have not the same length
        """
        if self.length_char_reference != self.length_char_prediction:
            hamming_score = "Ø"
        else:
            hamming_score = Levenshtein.hamming(self.reference, self.prediction)
        return hamming_score

    # Collection of HTR/OCR metrics #
    def _wer(self):
        """Computes the word error rate (WER).

        The word error rate is derived from the Levenshtein distance
        which works at word level instead of characters. It indicates the
        rate of incorrectly recognized words compared to a reference text.
        The lower the rate (minimum 0.0), the better the recognition.
        The maximum rate is not limited and can exceed 1.0 in the event
        of very poor recognition if there are many insertions.

        In kami, the rate is bounded between 0 and 1 and
        it is calculated as D(R,H)/total words in reference
        where D is Levenshtein distance and equivalent to
        S (incorrectly recognized words) + I (added words) + D (deletions words).

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : result of word error rate (opt : truncate / decimal or percentage)

        """
        wer = (self.lev_distance_words / self.length_words_reference)

        if self.opt_percent:
            wer = _get_percent(wer)

        if self.opt_truncate:
            wer = _truncate_score(wer, self.round_digits)

        return wer

    def _cer(self):
        """Computes the character error rate (CER).

        As WER, the character error rate which works at character level
        instead of words. In Kami as WER, the rate is bounded between 0 and 1.

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : result of character error rate (opt : truncate / decimal or percentage)
        """
        cer = (self.lev_distance_char / self.length_char_reference)


        if self.opt_percent:
            cer = _get_percent(cer)

        if self.opt_truncate:
            cer = _truncate_score(cer, self.round_digits)

        return cer

    def _wacc(self):
        """Computes the word accuracy (Wacc).

        The word accuracy calculates the number of perfectly recognized words
        and helps assess overall recognition of HTR/ OCR.
        This recognition rate can be negative.

        In kami, it is calculated as (1-WER), where 1 corresponding to
        the best score.

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : result of word accuracy (opt : truncate / decimal or percentage)
        """
        wacc = (1 - (self.lev_distance_words / self.length_words_reference))


        if self.opt_percent:
            wacc = _get_percent(wacc)

        if self.opt_truncate:
            wacc = _truncate_score(wacc, self.round_digits)

        return wacc


    def _cip(self):
        """Computes the character information preserved (CIP).

        It is roughly equivalent to word accuracy but it work on character.
        In kami, It is calculated as number of
        (H/total characters of reference) * (H/total characters of hypothesis)
        where H number of correctly recognized characters.

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : result of word information preserved (opt : truncate / decimal or percentage)
        """
        if self.prediction:
            cip = (float(self.H)
                   / self.length_char_reference) * (float(self.H) /
                                                    len(self.prediction))
            if self.opt_percent:
                cip = _get_percent(cip)
            if self.opt_truncate:
                cip = _truncate_score(cip, self.round_digits)
        else:
            cip = 0
        return cip

    def _cil(self):
        """Computes the character information lost (CIL).

        In kami, It is calculated as 1 - CIP. The lower the rate,
        the more information has disappeared.

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : result of word information lost (opt : truncate / decimal or percentage)
        """
        if self.prediction:
            cil = (1 - (float(self.H)
                        / self.length_char_reference)
                  * (float(self.H) /
                     len(self.prediction)))
        else:
            cil = 0

        if self.opt_percent:
            cil = _get_percent(cil)

        if self.opt_truncate:
            cil = _truncate_score(cil, self.round_digits)

        return cil

    def _mer(self):
        """Computes the match error rate (MER).


        the lower the rate, more errors are minimized and
        better the recognition of characters is effective. It corresponds to an
        overall error ratio of text recognition. It's a another way
        to compute CER.

        In kami, It is calculated as S + D + I / H + S + D + I

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : result of match error rate (opt : truncate / decimal or percentage)
        """
        mer = float(self.S + self.D + self.I) / float(self.H + self.S + self.D + self.I)

        if self.opt_percent:
            mer = _get_percent(mer)

        if self.opt_truncate:
            mer = _truncate_score(mer, self.round_digits)

        return mer

    def _get_operation_counts(self):
        """Based on editops function from C extension module python-Levenshtein.
         Find sequence of edit operations transforming one string to another.

        See also : https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html

        Args:
            reference (str) : reference string (ground truth)
            prediction (str) : prediction string to compare (hypothesis)

        Returns:
            int : number of hints (corrects characters)
            int : number of subsitutions (substituted characters)
            int : number of deletions (removed characters)
            int : number of insertions (added characters)
        """

        result_editops = Levenshtein.editops(self.reference, self.prediction)

        substitutions = sum(1 if operations[0] == "replace" else 0 for operations in result_editops)
        deletions = sum(1 if operations[0] == "delete" else 0 for operations in result_editops)
        insertions = sum(1 if operations[0] == "insert" else 0 for operations in result_editops)
        hits = self.length_char_reference - (substitutions + deletions)

        return hits, \
               substitutions, \
               deletions, \
               insertions

    def __str__(self):
        return f"class {self.__class__.__name__}"

    def __init__(self,
                 reference,
                 prediction,
                 show_percent=False,
                 truncate_score=False,
                 round_digits='.01'):
        # Options
        self.opt_percent = show_percent
        self.opt_truncate = truncate_score
        self.round_digits = round_digits
        # Strings to compare
        self.reference = reference
        self.prediction = prediction
        # Length set of sentences
        self.length_char_reference = len(reference)
        self.length_char_prediction = len(prediction)
        self.length_words_reference = len(reference.split())
        self.length_words_prediction = len(prediction.split())
        # Distances
        self.lev_distance_words, \
        self.lev_distance_char = self._levensthein_distance()
        self.hamming = self._hamming_distance()
        # HTR/OCR Metrics
        self.wer = self._wer()
        self.cer = self._cer()
        self.wacc = self._wacc()
        self.H, self.S, self.D, self.I = self._get_operation_counts()
        self.cip = self._cip()
        self.cil = self._cil()
        self.mer = self._mer()
        # Summary of all metrics
        self.board = {
            "levensthein_distance_char": self.lev_distance_char,
            "levensthein_distance_words": self.lev_distance_words,
            "hamming_distance": self.hamming,
            "wer": self.wer,
            "cer": self.cer,
            "wacc": self.wacc,
            "mer": self.mer,
            "cil": self.cil,
            "cip": self.cip,
            "hits": self.H,
            "substitutions": self.S,
            "deletions": self.D,
            "insertions": self.I,
        }

# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""
    The ``evaluation`` module to assess text recognition (OCR/HTR) scores
    ======================================================================

"""

from typing import Sequence, Tuple, Union
import Levenshtein
from ._base_metrics import (_truncate_score,
                            _hot_encode,
                            _get_percent)

__all__ = [
    "Scorer",
]


class Scorer:
    """This class calculates the set of HTR / OCR scores.

    User can accesses directly to metrics/scores via the attributes of the :class: `Scorer` class
    in constructor method or via :class: `Kami` facade class.

    Parameters
    ----------

        :param reference: Ground-truth text or string
        :type reference: str
        :param prediction: model string or text prediction or test text or string
        to compare to :param: `reference` parameter
        :type prediction: str
        :param show_percent: `True` if the user want to show result in percent else `False`, defaults to False
        :type show_percent: bool, optional
        :param truncate_score: `True` if the user want to truncate result in percent else `False`,
        can indicate the number of digits after floating point with :param: `round_digits` parameter, defaults to False
        :type truncate_score: bool, optional
        :param round_digits: Set the number of digits after floating point in string form, defaults to '.01'
        :type round_digits: str, optional

    Attributes
    ----------

        :ivar _opt_percent: Option to show result in percent
        :type _opt_percent: bool
        :ivar _opt_truncate: Option to truncate result
        :type _opt_truncate: bool
        :ivar _round_digits: Number of digits after floating points
        :type _round_digits: str
        :ivar reference: Ground-truth text or string
        :type reference: str
        :ivar prediction: Text to compare or predicted sequence
        :type prediction: str
        :ivar length_char_reference: Total number of characters in reference string
        :type length_char_reference: int
        :ivar length_char_prediction: Total number of characters in predicted string
        :type length_char_prediction: int
        :ivar length_words_reference: Total number of words in reference string
        :type length_words_reference: int
        :ivar length_words_prediction: Total number of words in predicted string
        :type length_words_prediction: int
        :ivar lev_distance_words: Edit distance (levensthein) between reference and prediction based on words
        :type lev_distance_words: int
        :ivar lev_distance_char: Edit distance (levensthein) between reference and prediction based on characters
        :type lev_distance_char: int
        :ivar hamming: Hamming distance between reference and prediction based on words
        :type hamming: int or str ("Ø") if sequences have not the same numbers of characters
        :ivar wer: Word Error Rate
        :type wer: float
        :ivar cer: Character Error Rate
        :type cer: float
        :ivar wacc: Word Accuracy
        :type wacc: float
        :ivar cip: Character Information Preserved
        :type cip: float
        :ivar cil: Character Information Lost
        :type cil: float
        :ivar mer: Match Error Rate
        :type mer: float
        :ivar hits: number of characters that matches between reference and prediction string
        :type hits: int
        :ivar substs: number of characters substituted between reference and prediction string
        :type substs: int
        :ivar deletions: number of characters deleted between reference and prediction string
        :type deletions: int
        :ivar insertions: number of characters inserted between reference and prediction string
        :type insertions: int
        :ivar board: A benchmark of all metrics
        :type board: dict


    """
    def __init__(self,
                 reference: str,
                 prediction: str,
                 show_percent: bool = False,
                 truncate_score: bool = False,
                 round_digits: str = '.01'):

        # Options
        self._opt_percent = show_percent
        self._opt_truncate = truncate_score
        self._round_digits = round_digits

        # Strings to compare
        self.reference = reference
        self.prediction = prediction

        # Length set of sentences
        self.length_char_reference = len(reference)
        self.length_char_prediction = len(prediction)
        self.length_words_reference = len(reference.split())
        self.length_words_prediction = len(prediction.split())

        # Distances
        self.lev_distance_words, self.lev_distance_char = self._levensthein_distance()
        self.hamming = self._hamming_distance()

        # Operations
        self.hits, self.substs, self.deletions, self.insertions = self._get_operation_counts()

        # HTR/OCR Metrics
        self.wer = self._wer()
        self.cer = self._cer()
        self.wacc = self._wacc()
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
                "hits": self.hits,
                "substitutions": self.substs,
                "deletions": self.deletions,
                "insertions": self.insertions
        }

    # Collection of distance metrics #

    def _levensthein_distance(self) -> Tuple[int, int]:
        """Compute Levensthein distance from C extension module Python-Levensthein."""
        # Compute levensthein at word level
        lev_distance_words = Levenshtein.distance(*_hot_encode(
            [self.reference.split(), self.prediction.split()]))
        # Compute levensthein at char level
        lev_distance_char = Levenshtein.distance(self.reference, self.prediction)
        return lev_distance_words, lev_distance_char

    def _hamming_distance(self) -> Union[str, int]:
        """Compute Hamming distance from C extension module Python-Levensthein."""
        if self.length_char_reference != self.length_char_prediction:
            hamming_score = "Ø"
        else:
            hamming_score = Levenshtein.hamming(self.reference, self.prediction)
        return hamming_score

    # Collection of HTR/OCR metrics #

    def _wer(self) -> float:
        """Compute word error rate (WER)."""
        wer = (self.lev_distance_words/self.length_words_reference)
        if self._opt_percent:
            wer = _get_percent(wer)
        if self._opt_truncate:
            wer = _truncate_score(wer, self._round_digits)
        return wer

    def _cer(self) -> float:
        """Compute character error rate (CER)."""
        cer = (self.lev_distance_char/self.length_char_reference)
        if self._opt_percent:
            cer = _get_percent(cer)
        if self._opt_truncate:
            cer = _truncate_score(cer, self._round_digits)
        return cer

    def _wacc(self) -> float:
        """Compute word accuracy (Wacc)."""
        wacc = (1 - (self.lev_distance_words/self.length_words_reference))
        if self._opt_percent:
            wacc = _get_percent(wacc)
        if self._opt_truncate:
            wacc = _truncate_score(wacc, self._round_digits)
        return wacc

    def _cip(self) -> Union[float, int]:
        """Compute character information preserved (CIP)."""
        if self.prediction:
            cip = (float(self.hits)/self.length_char_reference)*(float(self.hits)/self.length_char_prediction)
            if self._opt_percent:
                cip = _get_percent(cip)
            if self._opt_truncate:
                cip = _truncate_score(cip, self._round_digits)
        else:
            cip = 0
        return cip

    def _cil(self) -> Union[float, int]:
        """Compute character information lost (CIL)."""
        if self.prediction:
            cil = (1 - (float(self.hits)/self.length_char_reference)*(float(self.hits)/self.length_char_prediction))
        else:
            cil = 0
        if self._opt_percent:
            cil = _get_percent(cil)
        if self._opt_truncate:
            cil = _truncate_score(cil, self._round_digits)
        return cil

    def _mer(self) -> float:
        """Compute match error rate (MER)."""
        mer = float(
            self.substs
            + self.deletions
            + self.insertions) \
            / float(
            self.hits
            + self.substs
            + self.deletions
            + self.insertions)

        if self._opt_percent:
            mer = _get_percent(mer)
        if self._opt_truncate:
            mer = _truncate_score(mer, self._round_digits)
        return mer

    def _get_operation_counts(self) -> Tuple[int, int, int, int]:
        """Find sequence of edit operations transforming one string to another.
        Based on editops function from C extension module python-Levenshtein."""
        result_editops = Levenshtein.editops(self.reference, self.prediction)

        def _sum_operations(keyword: str, results: Sequence[Tuple[str, int, int]]) -> int:
            """Compute a sum of define operations"""
            total = sum(1 if operations[0] == keyword else 0 for operations in results)
            return total

        substitutions = _sum_operations("replace", result_editops)
        deletions = _sum_operations("delete", result_editops)
        insertions = _sum_operations("insert", result_editops)
        hits = self.length_char_reference - (substitutions + deletions)
        return hits, substitutions, deletions, insertions

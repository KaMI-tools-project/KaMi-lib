# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""
    The ``evaluation`` module to assess text recognition (OCR/HTR) scores
    ======================================================================

"""

from typing import Sequence, Tuple, Union
from Levenshtein import (distance, 
                         hamming, 
                         editops)
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

        :param reference: Ground-truth text or string.
        :type reference: str
        :param prediction: model string or text prediction or test text or string.
        to compare to :param: `reference` parameter
        :type prediction: str
        :param insertion_cost: predefined a weight for insertions errors. Defaults to 1.0.
        :type insertion_cost: float
        :param substitution_cost: predefined a weight for substitution errors. Defaults to 1.0.
        :type substitution_cost: float
        :param deletion_cost: predefined a weight for insertions errors. Defaults to 1.0.
        :type deletion_cost: float
        :param show_percent: `True` if the user want to show result in percent else `False`, defaults to False.
        :type show_percent: bool, optional
        :param truncate_score: `True` if the user want to truncate result in percent else `False`,
        can indicate the number of digits after floating point with :param: `round_digits` parameter, defaults to False.
        :type truncate_score: bool, optional
        :param round_digits: Set the number of digits after floating point in string form, defaults to '.01'.
        :type round_digits: str, optional

    Attributes
    ----------

        :ivar _opt_percent: Option to show result in percent. 
        :type _opt_percent: bool
        :ivar _opt_truncate: Option to truncate result. 
        :type _opt_truncate: bool
        :ivar _round_digits: Number of digits after floating point. 
        :type _round_digits: str
        :ivar reference: Ground-truth text or string.
        :type reference: str
        :ivar prediction: Text to compare or predicted sequence.
        :type prediction: str
        :ivar insertion_cost: predefined a weight for insertions errors. 
        :type insertion_cost: float
        :ivar substitution_cost: predefined a weight for substitution errors. 
        :type substitution_cost: float
        :ivar deletion_cost: predefined a weight for insertions errors. 
        :type deletion_cost: float
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
        :ivar wer_hunt: Hunt word error rate
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
                 insertion_cost: int = 1.0,
                 deletion_cost: int = 1.0,
                 substitution_cost: int = 1.0,
                 show_percent: bool = False,
                 truncate_score: bool = False,
                 round_digits: str = '.01') -> None:

        # Scores display options
        self._opt_percent  = show_percent
        self._opt_truncate = truncate_score
        self._round_digits = round_digits
        
        # Strings to compare
        self.reference  = reference
        self.prediction = prediction

        # Operations weigthts pre-defined (default to 1)
        self.insertion_cost    = insertion_cost
        self.deletion_cost     = deletion_cost
        self.substitution_cost = substitution_cost

        # Length set of sentences
        self.length_char_reference   = len(reference)
        self.length_char_prediction  = len(prediction)
        self.length_words_reference  = len(reference.split())
        self.length_words_prediction = len(prediction.split())

        # Strings operations (weighted and unweighted / char-based and word-based)
        self.hits, self.substs, self.deletions, self.insertions, self.substs_weighted, self.deletions_weighted, self.insertions_weighted, self.word_substs, self.word_deletions, self.word_insertions, self.word_substs_weighted, self.word_deletions_weighted, self.word_insertions_weighted = self._get_operation_counts()

        # Distances
        if self.insertion_cost == 1 and self.deletion_cost  == 1 and self.substitution_cost == 1:
            self.lev_distance_words, self.lev_distance_char = self._levensthein_distance()
        else:
            self.lev_distance_words, self.lev_distance_char = self._weighted_levensthein_distance()

        self.hamming = self._hamming_distance()

        # HTR/OCR Metrics
        self.wer      = self._wer()
        self.wer_hunt = self._wer_hunt()
        self.cer      = self._cer()
        self.wacc     = self._wacc()
        self.cip      = self._cip()
        self.cil      = self._cil()
        self.mer      = self._mer()

        if self._opt_percent:
            self.wer       = _get_percent(self.wer)
            self.wer_hunt  = _get_percent(self.wer_hunt)
            self.cer       = _get_percent(self.cer)
            self.wacc      = _get_percent(self.wacc)
            self.cip       = _get_percent(self.cip)
            self.cil       = _get_percent(self.cil)
            self.mer       = _get_percent(self.mer)

        if self._opt_truncate:
            self.wer       = _truncate_score(self.wer, self._round_digits)
            self.wer_hunt  = _truncate_score(self.wer_hunt, self._round_digits)
            self.cer       = _truncate_score(self.cer, self._round_digits)
            self.wacc      = _truncate_score(self.wacc, self._round_digits)
            self.cip       = _truncate_score(self.cip, self._round_digits)
            self.cil       = _truncate_score(self.cil, self._round_digits)
            self.mer       = _truncate_score(self.mer, self._round_digits)

        # Summary of all metrics
        self.board = {
                "levensthein_distance_char": self.lev_distance_char,
                "levensthein_distance_words": self.lev_distance_words,
                "hamming_distance": self.hamming,
                "wer": self.wer,
                "cer": self.cer,
                "wacc": self.wacc,
                "wer_hunt": self.wer_hunt,
                "mer": self.mer,
                "cil": self.cil,
                "cip": self.cip,
                "hits": self.hits,
                "substitutions": self.substs,
                "deletions": self.deletions,
                "insertions": self.insertions
        }

    # Collection of distance metrics # 
    def _levensthein_distance(self) -> Tuple[float, float]:
        """Compute Levensthein distance from C extension module Python-Levensthein.
        
        Returns:
            Tuple[float, float]: weighted levensthein distance based on char level, weighted levensthein distance based on word level
        """
        return distance(*_hot_encode(
            [self.reference.split(), self.prediction.split()])), distance(self.reference, self.prediction)

    def _weighted_levensthein_distance(self) -> Tuple[float, float]:
        """Compute Levensthein distance from predefined cost.

        Returns:
            Tuple[float, float]: weighted levensthein distance based on word level, weighted levensthein distance based on char level
        """
        return sum(
            [self.word_substs_weighted,
            self.word_deletions_weighted,
            self.word_insertions_weighted]
            ), sum(
            [self.substs_weighted,
            self.deletions_weighted,
            self.insertions_weighted]
            )

    def _hamming_distance(self) -> Union[str, int]:
        """Compute Hamming distance from C extension module Python-Levensthein."""
        return "Ø" if self.length_char_reference != self.length_char_prediction else hamming(self.reference, self.prediction)

    # Collection of HTR/OCR metrics #

    def _wer(self) -> float:
        """Compute word error rate (WER)."""
        return (self.lev_distance_words/self.length_words_reference)

    def _wer_hunt(self) -> float:
        """Compute Hunt word error rate that minimize errors of deletions and insertions."""
        return (sum([
                self.word_substs,
                0.5 * self.word_deletions, 
                0.5 * self.word_insertions
                ]
                )/self.length_words_reference)if (
                    self.insertion_cost == 1 
                    and self.deletion_cost  == 1 
                    and self.substitution_cost == 1)else (sum(
                        [
                            self.word_substs_weighted,
                            0.5 * self.word_deletions_weighted,
                            0.5 * self.word_insertions_weighted
                        ]
                        )/self.length_words_reference)

    def _cer(self) -> float:
        """Compute character error rate (CER)."""
        return (self.lev_distance_char/self.length_char_reference)

    def _wacc(self) -> float:
        """Compute word accuracy (Wacc)."""
        return (1 - (self.lev_distance_words/self.length_words_reference))

    # Collection of experimental ASR (Automatic Speech Recognition) metrics #
    def _cip(self) -> float:
        """Compute character information preserved (CIP)."""
        return (float(self.hits)/self.length_char_reference)*(float(self.hits)/self.length_char_prediction) if self.prediction else 0.0

    def _cil(self) -> float:
        """Compute character information lost (CIL)."""
        return (1 - (float(self.hits)/self.length_char_reference)*(float(self.hits)/self.length_char_prediction)) if self.prediction else 0.0

    def _mer(self) -> float:
        """Compute match error rate (MER)."""
        return float(
            self.substs
            + self.deletions
            + self.insertions) \
            / float(
            self.hits
            + self.substs
            + self.deletions
            + self.insertions)

    def _get_operation_counts(self) -> Tuple[int, int, int, int]:
        """Find sequence of edit operations transforming one string to another.
        Based on editops function from C extension module python-Levenshtein."""
        result_editops_char = editops(self.reference, self.prediction)
        result_editops_word = editops(*_hot_encode(
            [
                self.reference.split(), 
                self.prediction.split()
                ]
            )
        )

        def _sum_operations(keyword: str, results: Sequence[Tuple[str, int, int]]) -> int:
            """Compute a sum of define operations"""
            total = sum(1 if operations[0] == keyword else 0 for operations in results)
            return total

        def _sum_operations_weighted(keyword: str, results: Sequence[Tuple[str, int, int]], weight: int) -> float:
            total = sum(1 * weight if operations[0] == keyword else 0 for operations in results)
            return total

        substitutions = _sum_operations("replace", result_editops_char)
        deletions     = _sum_operations("delete", result_editops_char)
        insertions    = _sum_operations("insert", result_editops_char)

        substitutions_weighted = _sum_operations_weighted("replace", result_editops_char, weight=self.substitution_cost)
        deletions_weighted     = _sum_operations_weighted("delete", result_editops_char, weight=self.deletion_cost)
        insertions_weighted    = _sum_operations_weighted("insert", result_editops_char, weight=self.insertion_cost)

        word_substitutions = _sum_operations("replace", result_editops_word)
        word_deletions     = _sum_operations("delete", result_editops_word)
        word_insertions    = _sum_operations("insert", result_editops_word)

        word_substitutions_weighted = _sum_operations_weighted("replace", result_editops_word, weight=self.substitution_cost)
        word_deletions_weighted     = _sum_operations_weighted("delete", result_editops_word, weight=self.deletion_cost)
        word_insertions_weighted    = _sum_operations_weighted("insert", result_editops_word, weight=self.insertion_cost)

        hits = self.length_char_reference - (substitutions + deletions)
        return hits, substitutions, deletions, insertions, substitutions_weighted, deletions_weighted, insertions_weighted, word_substitutions, word_deletions, word_insertions, word_substitutions_weighted, word_deletions_weighted, word_insertions_weighted

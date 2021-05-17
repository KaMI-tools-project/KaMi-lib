# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""
    The ``evaluation`` module to assess text recognition (OCR/HTR) metrics
    ======================================================================

"""


import Levenshtein

from ._base_metrics import (_truncate_score,
                            _hot_encode,
                            _get_percent)

__all__ = [
    "Scorer",
]


class Scorer:
    """Global class to compute classic HTR/OCR metrics."""

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
        self.hits, self.substs, self.deletions, self.insertions = self._get_operation_counts()
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

    def _levensthein_distance(self):
        """Compute Levensthein distance from C extension module Python-Levensthein."""
        # Compute levensthein at word level
        lev_distance_words = Levenshtein.distance(*_hot_encode(
            [self.reference.split(), self.prediction.split()]))
        # Compute levensthein at char level
        lev_distance_char = Levenshtein.distance(self.reference, self.prediction)
        return lev_distance_words, lev_distance_char

    def _hamming_distance(self):
        """Compute Hamming distance from C extension module Python-Levensthein."""
        if self.length_char_reference != self.length_char_prediction:
            hamming_score = "Ø"
        else:
            hamming_score = Levenshtein.hamming(self.reference, self.prediction)
        return hamming_score

    # Collection of HTR/OCR metrics #

    def _wer(self):
        """Compute word error rate (WER)."""
        wer = (self.lev_distance_words/self.length_words_reference)
        if self.opt_percent:
            wer = _get_percent(wer)
        if self.opt_truncate:
            wer = _truncate_score(wer, self.round_digits)
        return wer

    def _cer(self):
        """Compute character error rate (CER)."""
        cer = (self.lev_distance_char/self.length_char_reference)
        if self.opt_percent:
            cer = _get_percent(cer)
        if self.opt_truncate:
            cer = _truncate_score(cer, self.round_digits)
        return cer

    def _ser(self):
        """Compute sentence error rate (SER)."""
        ser = (self.lev_distance_char/self.length_char_reference)
        if self.opt_percent:
            ser = _get_percent(ser)
        if self.opt_truncate:
            ser = _truncate_score(ser, self.round_digits)
        return ser

    def _wacc(self):
        """Compute word accuracy (Wacc)."""
        wacc = (1 - (self.lev_distance_words/self.length_words_reference))
        if self.opt_percent:
            wacc = _get_percent(wacc)
        if self.opt_truncate:
            wacc = _truncate_score(wacc, self.round_digits)
        return wacc

    def _cip(self):
        """Compute character information preserved (CIP)."""
        if self.prediction:
            cip = (float(self.hits)/self.length_char_reference)*(float(self.hits)/len(self.prediction))
            if self.opt_percent:
                cip = _get_percent(cip)
            if self.opt_truncate:
                cip = _truncate_score(cip, self.round_digits)
        else:
            cip = 0
        return cip

    def _cil(self):
        """Compute character information lost (CIL)."""
        if self.prediction:
            cil = (1 - (float(self.hits)/self.length_char_reference)*(float(self.hits)/len(self.prediction)))
        else:
            cil = 0
        if self.opt_percent:
            cil = _get_percent(cil)
        if self.opt_truncate:
            cil = _truncate_score(cil, self.round_digits)
        return cil

    def _mer(self):
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

        if self.opt_percent:
            mer = _get_percent(mer)
        if self.opt_truncate:
            mer = _truncate_score(mer, self.round_digits)
        return mer

    def _get_operation_counts(self):
        """Find sequence of edit operations transforming one string to another.
        Based on editops function from C extension module python-Levenshtein."""
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




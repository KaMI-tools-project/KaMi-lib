# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""
    The ``evaluation`` module to assess text recognition (OCR/HTR) metrics
    ======================================================================

    Use this module standalone with :py:class:`kami.metrics.evaluation.Scorer()`
    class in evaluation or as part of KaMI :py:class:`kami.pipeline.Core()` class
    in pipeline module to assess text recognition (OCR/HTR) metrics.

    Metrics overview in KaMI
    ------------------------

    Distance metrics
    ****************

    To compute distance KaMI use C extension module from
    `Python-Levensthein <https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html>`_
    package.

    **Levenshtein distance** (or edit distance) :
                                                 Gives a measure of the difference between two strings.
                                                 It is equal to the minimum number of characters that must be deleted,
                                                 inserted or replaced to switch from one string to another.

    .. note :: In KaMI, you can access to distance on words and characters. These two kind of distance are utils
              for compute WER and CER.

    **Hamming distance** :
                          It very close from Levenshtein distance definition but gives a measure only between two strings
                          have the same length.

    Recognition measure
    *******************

    **Word Error Rate (WER)**:
                              The word error rate is derived from the Levenshtein distance
                              which works at word level instead of characters. It indicates the
                              rate of incorrectly recognized words compared to a reference text.
                              The lower the rate (minimum 0.0), the better the recognition.
                              The maximum rate is not limited and can exceed 1.0 in the event
                              of very poor recognition if there are many insertions.

                              In KaMI, the WER is bounded between 0 and 1 and it is calculated as

                              .. math::

                                \\frac{D(R,H)}{total\,words} \,where \,D \,is \,Levenshtein \,distance

    **Character Error Rate (CER)**:
                                   As WER, the character error rate which works at character level
                                   instead of words. In Kami as WER, the rate is bounded between 0 and 1.

    **Word accuracy (Wacc)**:
                              The word accuracy calculates the number of perfectly recognized words
                              and helps assess overall recognition of HTR/ OCR.
                              This recognition rate can be negative.

                              In kami, it is calculated as (1-WER), where 1 corresponding to
                              the best score.

    **Character information preserved (CIP)**:
                                              It is roughly equivalent to word accuracy but it work on character.

                                              In kami, It is calculated as number of
                                              (H/total characters of reference) * (H/total characters of hypothesis)
                                              where H number of correctly recognized characters.

    **Character information lost (CIL)**:
                                          In kami, It is calculated as 1 - CIP. The lower the rate,
                                          the more information has disappeared.

    **Match error rate (MER)**:
                                the lower the rate, more errors are minimized and
                                better the recognition of characters is effective. It corresponds to an
                                overall error ratio of text recognition. It's a another way
                                to compute CER.

                                In kami, It is calculated as S + D + I / H + S + D + I


    Access to different metrics with :py:class:`kami.metrics.evaluation.Scorer()`
    -----------------------------------------------------------------------------

    First, can use attribute define in :py:class:`kami.metrics.evaluation.Scorer()` (see the documentation)

        :Example:

        >>>

    Note catch individually hints, substitutions characters...

        :Example:

        >>>

    You can retrieve all the metrics in dictionnary with .. py:attribute:: `.board` attribute

        :Example:

        >>>


        .. note:: Can truncate and percentage score with parameters.
                 See the documentation :py:class:`kami.metrics.evaluation.Scorer()` documentation.

        .. seealso:: :py:class:`kami.metrics.evaluation.Scorer()` and :py:class:`kami.pipeline.Core()`


"""


import Levenshtein
from ._base_metrics import (_truncate_score,
                            _hot_encode,
                            _get_percent)

__all__ = [
    "Scorer",
]



class Scorer:
    """Global class to compute classic HTR/OCR metrics.

    :param reference: Reference string or text (ground truth).
    :type reference: str
    :param prediction: Hypothesis string or text to compare with reference.
    :type prediction: str
    :param show_percent: Option to show score as percentage.
    :type show_percent: bool
    :param truncate_score: Option to truncate score.
    :type truncate_score: bool
    :param round_digits: Option to select number of digit after the round score truncted.
    :type round_digits: str


    :cvar opt_percent: User option on percentage.
    :type opt_percent: bool
    :cvar opt_truncate: User option on truncate.
    :type opt_truncate:
    :cvar round_digits: User option set type of truncate.
    :type round_digits: str
    :cvar reference: User reference string.
    :type reference: str
    :cvar prediction: User prediction string.
    :type prediction: str
    :cvar length_char_reference: Total characters in reference string.
    :type length_char_reference: int
    :cvar length_char_prediction: Total characters in prediction string.
    :type length_char_prediction: int
    :cvar length_words_reference: Total words in reference string.
    :type length_words_reference: int
    :cvar length_words_prediction: Total words in prediction string.
    :type length_words_prediction: int
    :cvar lev_distance_words: Levensthein distance on words.
    :type lev_distance_words: int
    :cvar lev_distance_char: Levensthein distance on characters.
    :type lev_distance_char: int
    :cvar hamming: Hamming distance.
    :type hamming: str or float
    :cvar wer: Word error rate.
    :type wer: float
    :cvar cer: Character error rate.
    :type cer: float
    :cvar wacc: Word accuracy.
    :type wacc: float
    :cvar hints: Total number of Hints between reference and prediction.
    :type hints: int
    :cvar substs: Total number of Substitutions between reference and prediction.
    :type substs: int
    :cvar deletions: Total number of Deletions between reference and prediction.
    :type deletions: int
    :cvar insertions: Total number of Insertions between reference and prediction.
    :type insertions: int
    :cvar cip: Character information preserve.
    :type cip: float
    :cvar cil: Character information lost.
    :type cil: float
    :cvar mer: Match error rate.
    :type mer: float
    :cvar board: A general board of all above metrics in
                     key (name of metric) / value (score) struct
    :type board: dict
    :returns: OCR/HTR metrics in attributes of :py:class:`kami.metrics.evaluation.Scorer()`
    """


    # Collection of distance metrics #

    def _levensthein_distance(self):
        """Compute Levensthein distance from C extension module Python-Levensthein."""
        # Computes levensthein on words level
        lev_distance_words = Levenshtein.distance(*_hot_encode(
            [self.reference.split(), self.prediction.split()]
        )
                                                  )
        # Computes levensthein on char level
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
        """Computes the word error rate (WER)."""
        wer = (self.lev_distance_words / self.length_words_reference)

        if self.opt_percent:
            wer = _get_percent(wer)

        if self.opt_truncate:
            wer = _truncate_score(wer, self.round_digits)

        return wer

    def _cer(self):
        """Computes the character error rate (CER)."""
        cer = (self.lev_distance_char / self.length_char_reference)

        if self.opt_percent:
            cer = _get_percent(cer)

        if self.opt_truncate:
            cer = _truncate_score(cer, self.round_digits)

        return cer

    def _wacc(self):
        """Computes the word accuracy (Wacc)."""
        wacc = (1 - (self.lev_distance_words / self.length_words_reference))

        if self.opt_percent:
            wacc = _get_percent(wacc)

        if self.opt_truncate:
            wacc = _truncate_score(wacc, self.round_digits)

        return wacc

    def _cip(self):
        """Computes the character information preserved (CIP)."""
        if self.prediction:
            cip = (float(self.hints)
                   / self.length_char_reference) * (float(self.hints) /
                                                    len(self.prediction))
            if self.opt_percent:
                cip = _get_percent(cip)
            if self.opt_truncate:
                cip = _truncate_score(cip, self.round_digits)
        else:
            cip = 0
        return cip

    def _cil(self):
        """Computes the character information lost (CIL)."""
        if self.prediction:
            cil = (1 - (float(self.hints)
                        / self.length_char_reference)
                   * (float(self.hints) /
                      len(self.prediction)))
        else:
            cil = 0

        if self.opt_percent:
            cil = _get_percent(cil)

        if self.opt_truncate:
            cil = _truncate_score(cil, self.round_digits)

        return cil

    def _mer(self):
        """Computes the match error rate (MER)."""
        mer = float(
            self.substs
            + self.deletions
            + self.insertions) \
            / float(
            self.hints
            + self.substs
            + self.deletions
            + self.insertions
        )

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
        self.hints, self.substs, self.deletions, self.insertions = self._get_operation_counts()
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
            "hits": self.hints,
            "substitutions": self.substs,
            "deletions": self.deletions,
            "insertions": self.insertions,
        }

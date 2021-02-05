"""Metrics to assess text recognition (OCR/HTR)
"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT

import Levenshtein

from ._base import _truncate_score
from ._distance import _levensthein_distance, _hamming_distance

__all__ = [
    "wer",
    "cer",
    "wacc",
    "cip",
    "cil",
    "mer",
    "_get_operation_counts",
    "board"
]


def wer(reference, prediction):
    """Computes the word error rate (WER).

    The word error rate is derived from the Levenshtein distance
    which works at word level instead of characters. It indicates the
    rate of incorrectly recognized words compared to a reference text.
    The lower the rate (minimum 0.0), the better the recognition.
    The maximum rate is not limited and can exceed 1.0 in the event
    of very poor recognition if there are many insertions.
    (src : Wikipédia)

    In kami, the rate is bounded between 0 and 1 and
    it is calculated as D(R,H)/total words in reference
    where D is Levenshtein distance and equivalent to
    S (incorrectly recognized words) + I (added words) + D (deletions words).

    Args:
        reference (str) : reference string (ground truth)
        prediction (str) : prediction string to compare (hypothesis)

    Returns:
        int : result of word error rate

    """
    scorer = board(reference, prediction)
    return scorer["wer"]


def cer(reference, prediction):
    """Computes the character error rate (CER).

    As WER, the character error rate which works at character level
    instead of words. In Kami as WER, the rate is bounded between 0 and 1.

    Args:
        reference (str) : reference string (ground truth)
        prediction (str) : prediction string to compare (hypothesis)

    Returns:
        int : result of character error rate
    """
    scorer = board(reference, prediction)
    return scorer["cer"]

def wacc(reference, prediction):
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
        int : result of word accuracy
    """
    scorer = board(reference, prediction)
    return scorer["wacc"]

def cip(reference, prediction):
    """Computes the character information preserved (CIP).

    It is roughly equivalent to word accuracy but it work on character.
    In kami, It is calculated as number of (H/total characters of reference) * (H/total characters of hypothesis)
    where H number of correctly recognized characters.

    Args:
        reference (str) : reference string (ground truth)
        prediction (str) : prediction string to compare (hypothesis)

    Returns:
        int : result of word information preserved
    """
    scorer = board(reference, prediction)
    return scorer["cip"]

def cil(reference, prediction):
    """Computes the character information lost (CIL).

    In kami, It is calculated as 1 - CIP. The lower the rate,
    the more information has disappeared.

    Args:
        reference (str) : reference string (ground truth)
        prediction (str) : prediction string to compare (hypothesis)

    Returns:
        int : result of word information lost
    """
    scorer = board(reference, prediction)
    return scorer["cil"]

def mer(reference, prediction):
    """Computes the match error rate (MER).


    the lower the rate, the more errors are minimized and
    the better the recognition. It corresponds to an
    overall error ratio of text recognition.

    In kami, It is calculated as S + D + I / H + S + D + I

    Args:
        reference (str) : reference string (ground truth)
        prediction (str) : prediction string to compare (hypothesis)

    Returns:
        int : result of match error rate
    """
    scorer = board(reference, prediction)
    return scorer["mer"]


def board(truth, hypothesis):
    """Computes all the recognition metrics, distances and
    characters operations between string.

    Distance : levensthein, hamming
    Rates : WER, CER, Wacc, MER, CIP, CIL
    Operations : H (hints), S (Substitutions), D (Deletions), I (Insertions)

    Args:
        reference (str) : reference string (ground truth)
        prediction (str) : prediction string to compare (hypothesis)

    Returns:
        dict : result of recognition metrics, distances and
    characters operations
    """
    # Computes levensthein distance on words for WER
    lev_distance_words = _levensthein_distance(truth.split(), hypothesis.split())
    # Computes levensthein distance on words for CER (that's the rate in result)
    lev_distance_characters = _levensthein_distance(truth, hypothesis)
    # Computes Hamming distance on characters
    hamming_distance = _hamming_distance(truth, hypothesis)
    # Computes the WER
    wer = (lev_distance_words / len(truth.split()))
    # Computes the CER
    cer = (lev_distance_characters / len(truth))
    # Computes the Word accuracy
    wacc = (1 - wer)
    # Computes the Word accuracy
    H, S, D, I = _get_operation_counts(truth, hypothesis)
    # Computes the match error rate
    mer = float(S + D + I) / float(H + S + D + I)
    # Computes the character information preserved
    cip = (float(H) / len(truth)) * (float(H) / len(hypothesis)) if hypothesis else 0
    # Computes the character information loss
    cil = 1 - cip



    return {
        "levensthein_distance": lev_distance_characters,
        "hamming_distance": hamming_distance,
        "wer": wer,
        "cer": cer,
        "wacc": wacc,
        "mer": mer,
        "cil": cil,
        "cip": cip,
        "hits": H,
        "substitutions": S,
        "deletions": D,
        "insertions": I,
    }

def _get_operation_counts(source, destination):
    """on character

    :param source:
    :param destination:
    :return:
    """

    editops = Levenshtein.editops(source,
                                  destination)

    substitutions = sum(1 if operations[0] == "replace" else 0 for operations in editops)
    deletions = sum(1 if operations[0] == "delete" else 0 for operations in editops)
    insertions = sum(1 if operations[0] == "insert" else 0 for operations in editops)
    hits = len(source) - (substitutions + deletions)

    return hits, \
           substitutions, \
           deletions, \
           insertions
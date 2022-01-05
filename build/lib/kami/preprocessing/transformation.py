# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""
    The ``transformation`` module to preprocess text data
    =====================================================

"""


import re
import string
import unicodedata
from typing import (Union,
                    List,
                    Mapping,
                    TypeVar,
                    Optional)

import unidecode

from kami.kamutils._utils import _timing

__all__ = [
    "ToCompose",
    "_AbstractTransform",
    "_Composer",
    "_SentencesToTokens",
    "RemovePunctuation",
    "RemoveDigits",
    "RemoveDiacritics",
    "RemoveNonUsefulWords",
    "RemoveSpecificWords",
    "Strip",
    "SubRegex",
    "ToLowerCase",
    "ToUpperCase"
]

# Declare preprocessing class types can only use with ToCompose() class
TRemovePunctuation = TypeVar('TRemovePunctuation', bound='RemovePunctuation')
TRemoveDiacritics = TypeVar('TRemoveDiacritics', bound='RemoveDiacritics')
TRemoveDigits = TypeVar('TRemoveDigits', bound='RemoveDigits')
TRemoveNonUsefulWords = TypeVar('TRemoveNonUsefulWords', bound='RemoveNonUsefulWords')
TRemoveSpecificWords = TypeVar('TRemoveSpecificWords', bound='RemoveSpecificWords')
TStrip = TypeVar('TStrip', bound='Strip')
TSubRegex = TypeVar('TSubRegex', bound='SubRegex')
TToLowerCase = TypeVar('TToLowerCase', bound='ToLowerCase')
TToUpperCase = TypeVar('TToUpperCase', bound='ToUpperCase')


class ToCompose:
    """

    """
    def __init__(self, sentences: list,
                 type_transforms: Optional[List[Union[
                     TRemovePunctuation,
                     TRemoveDigits,
                     TRemoveNonUsefulWords,
                     TRemoveDiacritics,
                     TRemoveSpecificWords,
                     TStrip,
                     TSubRegex,
                     TToLowerCase,
                     TToUpperCase]]]):
        process = _Composer(type_transforms)(sentences)
        self.reference = process[0]
        self.prediction = process[1]


class _AbstractTransform(object):
    def __call__(self, sentences: Union[str, List[str]]):
        if isinstance(sentences, str):
            return self.process_string(sentences)
        elif isinstance(sentences, list):
            return self.process_list(sentences)
        else:
            raise ValueError(
                f"input {sentences} was expected to be a string or list of strings"
            )

    def process_string(self, sequence: str):
        raise NotImplementedError()

    def process_list(self, group: List[str]):
        return [self.process_string(sequence) for sequence in group]


class _Composer(object):
    def __init__(self, transforms: List[_AbstractTransform]):
        self.transforms = transforms

    def __call__(self, text):
        for transform in self.transforms:
                text = transform(text)
        return text


#
# Tokenizers
#


class _SentencesToTokens(_AbstractTransform):
    """

    """
    def __init__(self, delimiter: str = " "):
        self.delimiter = delimiter

    def process_string(self, sequence: str):
        return sequence.split(self.delimiter)


#
# Modifiers
#


class RemovePunctuation(_AbstractTransform):
    """Remove punctuation from text. Default remove : !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~
    User can specify punctuation want to keep in text.

    User can directly access to this class or via :class: `ToCompose` class.

    Parameters
    ----------
    :param keep_punctuation: list of punctuation to keep in text.
    :type keep_punctuation: list, optional

    Attributes
    ----------
    See Parameters
    """
    def __init__(self, keep_punctuation: Optional[List[str]] = ''):
        self.keep_punctuation = keep_punctuation

    def process_string(self, sequence: str):
        default_punctuation = string.punctuation
        if len(self.keep_punctuation) == 0:
            table = str.maketrans('', '', default_punctuation)
        else:
            new_punctuation = "".join(
                [symbol for symbol in default_punctuation if symbol not in self.keep_punctuation])
            table = str.maketrans('', '', new_punctuation)

        sequence = sequence.translate(table)

        return sequence


class RemoveDiacritics(_AbstractTransform):
    """Remove digits from text.

    User can directly access to this class or via :class: `ToCompose` class.
    """
    def process_string(self, sequence: str):

        sequence = unidecode.unidecode(sequence)
        sequence = re.sub(r'<{2,}', "", sequence)
        sequence = re.sub(r'>{2,}', "", sequence)
        sequence = re.sub(r'-{2,}', "", sequence)
        #sequence = unicodedata.normalize('NFD', sequence)\
           #.encode('ascii', 'ignore')\
           #.decode("utf-8")
        return str(sequence)


class RemoveDigits(_AbstractTransform):
    """Remove digits from text.

    User can directly access to this class or via :class: `ToCompose` class.
    """
    def process_string(self, sequence: str):
        sequence = re.sub(r"\d+", "", sequence)
        return sequence


class RemoveNonUsefulWords(_AbstractTransform):
    """Remove empties tokens from text.

    User can directly access to this class or via :class: `ToCompose` class.
    """
    def process_string(self, sequence: str):
        sequence = " ".join([token for token in sequence.split() if token != ''])
        return sequence


class RemoveSpecificWords(_AbstractTransform):
    """Remove specifics words that predefined by user.

    User can directly access to this class or via :class: `ToCompose` class.

    Parameters
    ----------
    :param words_to_remove: list of words to remove.
    :type words_to_remove: list

    Attributes
    ----------
    See Parameters

    """
    def __init__(self, words_to_remove: List[str]):
        self.words_to_remove = words_to_remove

    def process_string(self, sequence: str):
        # TODO(@Luca) : tokenization better eg. "Curée," to ["Curée", ","]
        sequence = " ".join([token for token in sequence.split() if token not in self.words_to_remove])
        return sequence


class Strip(_AbstractTransform):
    """Performs text strip.

    User can directly access to this class or via :class: `ToCompose` class.
    """
    def process_string(self, sequence: str):
        return sequence.strip()


class SubRegex(_AbstractTransform):
    """Performs substitutions in text with regex patterns.

    User can directly access to this class or via :class: `ToCompose` class.

    Parameters
    ----------
    :param substitutions: a dictionary where the key is a regex pattern
    and value is the element to substitute.
    :type substitutions: dict

    Attributes
    ----------
    See Parameters
    """
    def __init__(self, substitutions: dict):
        self.substitutions = substitutions

    def process_string(self, sequence: str):
        sequence = " ".join([re.sub(key, value, sequence) for key, value in self.substitutions.items()])
        return sequence


class ToLowerCase(_AbstractTransform):
    """Pass a string to lowercase.

    User can directly access to this class or via :class: `ToCompose` class.
    """
    def process_string(self, sequence: str):
        return sequence.lower()


class ToUpperCase(_AbstractTransform):
    """Pass a string to uppercase.

    User can directly access to this class or via :class: `ToCompose` class.
    """
    def process_string(self, sequence: str):
        return sequence.upper()


# Utils functions relative to transformation

def count_diacritics(string):
    """A simple diacritics counter"""
    total_diacritics = []
    for char in string:
        char_transform = unidecode.unidecode(char)
        #char_transform = unicodedata.normalize('NFD', char)\
           #.encode('ascii', 'ignore')\
           #.decode("utf-8")
        if char != char_transform:
            total_diacritics.append(char)

    return len(total_diacritics)

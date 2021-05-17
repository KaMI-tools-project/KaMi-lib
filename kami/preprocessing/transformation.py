# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""
    The ``transformation`` module to preprocess text data
    =====================================================

"""


from typing import Union, List, Mapping
import string
import re

from kami.kamutils._utils import (_report_log, _timing)

__all__ = [
    "AbstractTransform",
    "Composer",
    "SentencesToTokens",
    "RemovePunctuation",
    "RemoveDigits",
    "RemoveNonUsefulWords",
    "RemoveSpecificWords",
    "Strip",
    "SubRegex",
    "ToLowerCase",
    "ToUpperCase"
]


class AbstractTransform(object):
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


class Composer(object):
    def __init__(self, transforms: List[AbstractTransform]):
        self.transforms = transforms

    @_timing
    def __call__(self, text):
        for transform in self.transforms:
                text = transform(text)
        return text

#
# Tokenizers
#


class SentencesToTokens(AbstractTransform):
    def __init__(self, delimiter: str = " "):
        self.delimiter = delimiter

    def process_string(self, sequence: str):
        return sequence.split(self.delimiter)


#
# Modifiers
#


class RemovePunctuation(AbstractTransform):
    def __init__(self, keep_punctuation: list = []):
        self.keep_punctuation = keep_punctuation

    def process_string(self, sequence: str):
        default_punctuation = string.punctuation
        if len(self.keep_punctuation) == 0:
            table = str.maketrans('', '', default_punctuation)
        else:
            new_punctuation = " ".join(
                [symbol for symbol in default_punctuation if symbol not in self.keep_punctuation])
            table = str.maketrans('', '', new_punctuation)

        sequence = sequence.translate(table)

        return sequence


class RemoveDigits(AbstractTransform):
    def process_string(self, sequence: str):
        sequence = " ".join([re.sub(r"\d+", "", token) for token in sequence.split() if not token.isdigit()])
        return sequence


class RemoveNonUsefulWords(AbstractTransform):
    def process_string(self, sequence: str):
        sequence = " ".join([token for token in sequence.split() if token != ''])
        return sequence


class RemoveSpecificWords(AbstractTransform):
    def __init__(self, words_to_remove: List[str]):
        self.words_to_remove = words_to_remove

    def process_string(self, sequence: str):
        sequence = " ".join([token for token in sequence.split() if token not in self.words_to_remove])
        return sequence


class Strip(AbstractTransform):
    def process_string(self, sequence: str):
        return sequence.strip()


class SubRegex(AbstractTransform):
    def __init__(self, substitutions: Mapping[str, str]):
        self.substitutions = substitutions

    def process_string(self, sequence: str):
        sequence = " ".join([re.sub(key, value, sequence) for key, value in self.substitutions.items()])
        return sequence


class ToLowerCase(AbstractTransform):
    def process_string(self, sequence: str):
        return sequence.lower()


class ToUpperCase(AbstractTransform):
    def process_string(self, sequence: str):
        return sequence.upper()




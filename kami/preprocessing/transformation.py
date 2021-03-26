# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""

    The ``transformation`` module to preprocess text data
    =====================================================

    Inspiration : Jiwer Python package @Nik Vaessen (https://pypi.org/project/jiwer/)

    This module can be necessary to apply a few preprocessing steps on ground truth and
    hypothesis texts.

    The transformation are accessible via different types of methods : ...

    TODO add Composer doc + doc of each preprocess methods here

"""


from typing import Union, List, Mapping
import string

from kami.kamutils._utils import (_report_log, _timing)
from kami.preprocessing._base_preprocessing import (
    lowercase,
    uppercase,
    tokens_nonpunct,
    tokens_nondigits,
    tokens_non_words,
    tokens_remove,
    stripper,
    regex_subts,
    _stop_words_process)


__all__ = [
    "AbstractTransform",
    "Composer",
    "SentencesToTokens",
    "SentencesToListOfWords",
    "RemovePunctuation",
    "RemoveDigits",
    "RemoveNonUsefulWords",
    "RemoveSpecificWords",
    "SpacyEngineFrStopsWords",
    "SpacyEngineEnStopsWords",
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


# Tokenisers methods

class SentencesToTokens(AbstractTransform):
    def __init__(self, delimiter: str = " "):
        self.delimiter = delimiter

    def process_string(self, sequence: str):
        return sequence.split(self.delimiter)


class SentencesToListOfWords(SentencesToTokens):
    def __init__(self, delimiter: str = " "):
        self.delimiter = delimiter

    def process_list(self, group: List[str]):
        words = []
        for sentence in group:
            words.extend(self.process_string(sentence))
        return words


# Deletetions methods

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
        _report_log(f'+ Remove punctuation applied on sequence.', 'V')
        return tokens_nonpunct(sequence, table)

    def __str__(self):
        return "removepunct_method"


class RemoveDigits(AbstractTransform):
    def process_string(self, sequence: str):
        _report_log(f'+ Remove digits applied on sequence.', 'V')
        return tokens_nondigits(sequence)

    def __str__(self):
        return "removedigits_method"


class RemoveNonUsefulWords(AbstractTransform):
    def process_string(self, sequence: str):
        _report_log(f'+ Remove non useful words applied on sequence.', 'V')
        return tokens_non_words(sequence)

    def __str__(self):
        return "nonusefulwords_method"


class RemoveSpecificWords(AbstractTransform):
    def __init__(self, words_to_remove: List[str]):
        self.words_to_remove = words_to_remove

    def process_string(self, sequence: str):
        _report_log(f'+ Remove specific words applied on sequence.', 'V')
        return tokens_remove(sequence, self.words_to_remove)

    def __str__(self):
        return "specificwords_method"


class SpacyEngineFrStopsWords(AbstractTransform):
    def __init__(self, add_stops_words: list = [], keep_stops_words: list = []):
        self.add_stops_words = add_stops_words
        self.keep_stops_words = keep_stops_words

    def process_string(self, sequence: str):
        try:
            _report_log("...load French stops words base from spaCy...")
            from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
        except Exception as e:
            _report_log("Cannot load French stops words from spaCy.", "E")

        sequence = _stop_words_process(sequence, fr_stop, self.add_stops_words, self.keep_stops_words)
        _report_log(f'+ French stops words filter applied on sequence.', 'V')
        return sequence

    def __str__(self):
        return "frstopwords_method"


class SpacyEngineEnStopsWords(AbstractTransform):
    def __init__(self, add_stops_words: list = [], keep_stops_words: list = []):
        self.add_stops_words = add_stops_words
        self.keep_stops_words = keep_stops_words

    def process_string(self, sequence: str):
        try:
            _report_log("...load English stops words base from spaCy...")
            from spacy.lang.en.stop_words import STOP_WORDS as en_stop
        except Exception as e:
            _report_log("Cannot load English stops words from spaCy.", "E")

        sequence = _stop_words_process(sequence, en_stop, self.add_stops_words, self.keep_stops_words)
        _report_log(f'+ English stops words filter applied on sequence.', 'V')
        return sequence

    def __str__(self):
        return "enstopwords_method"


class Strip(AbstractTransform):
    def process_string(self, sequence: str):
        _report_log(f'+ Strip spaces method applied on sequence.', 'V')
        return stripper(sequence)

    def __str__(self):
        return "strip_method"


# Substitute methods

class SubRegex(AbstractTransform):
    def __init__(self, substitutions: Mapping[str, str]):
        self.substitutions = substitutions

    def process_string(self, sequence: str):
        _report_log(f'+ Substitutions regex performed on sequence.', 'V')
        return regex_subts(sequence, self.substitutions)

    def __str__(self):
        return "subregex_method"


class SubWords(AbstractTransform):
    pass  # TODO if necessary


# Modifiers methods

class ToLowerCase(AbstractTransform):
    def process_string(self, sequence: str):
        _report_log(f'+ Lowercase applied on sequence.', 'V')
        return lowercase(sequence)

    def __str__(self):
        return "lowercase_method"


class ToUpperCase(AbstractTransform):
    def process_string(self, sequence: str):
        _report_log(f'+ Uppercase applied on sequence.', 'V')
        return uppercase(sequence)

    def __str__(self):
        return "uppercase_method"




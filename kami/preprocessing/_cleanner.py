# -*- coding: utf-8 -*-

"""Basic text processing function for ground truth and prediction
"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
# TODO(Luca) : documentation / Pylint
import string
import re

from kami.kamutils._utils import (report_log, timing)

__all__ = [
    "cleanner",
]

## Lambda collection function ##

# <-- Pass string in lowercase -->
lowercase = lambda sequence: " ".join([token.lower()
                                       for token
                                       in sequence.split()])

# <-- Remove punctuation from predefined list of symbols drom string -->
tokens_nonpunct = lambda sequence, table: " ".join([token.translate(table)
                                                    for token
                                                    in sequence.split()])

# <-- Remove all digits from string -->
tokens_nondigits = lambda sequence: " ".join([re.sub(r"\d+", "", token)
                                              for token
                                              in sequence.split()
                                              if not token.isdigit()])

# <-- Remove non useful words as empty tokens ('') and newline characters (\r, \n) -->
tokens_non_words = lambda sequence: " ".join([token
                                              for token
                                              in sequence.split()
                                              if token != ''])


def _stop_words_process(sentence, lang_stop_defined, app_swords, keep_swords):
    """sub-routine
    """
    lang_stopwords = [stop for stop in lang_stop_defined]
    if app_swords != None:
        for word in app_swords:
            lang_stopwords.append(word)
    if keep_swords != None:
        for word in keep_swords:
            if word in lang_stopwords:
                lang_stopwords.remove(word)

    sequence = " ".join([token
                         for token
                         in sentence.split()
                         if token.lower()
                         not in lang_stopwords])
    return sequence



@timing
def cleanner(reference,
             prediction,
             options=None,
             keep_punct=None,
             append_stop_words=None,
             keep_stop_words=None):
    """

    """
    report_log('Init text preprocessing sequence...')

    if options == None:
        report_log('No cleanning options selected ! '
                   'Sequences passed are same from origin. '
                   'Try to add options in options parameter '
                   'of cleanner function', 'W')
        return reference, prediction

    else:
        # Parse options in lower for user
        options = [opt.lower() for opt in options]

        if "lowercase" in options:
            reference = lowercase(reference)
            prediction = lowercase(prediction)
            report_log('+ Lowercase applied.', 'V')
        if "remove_punctuation" in options:
            # Default punct : !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
            punctuation = string.punctuation
            if keep_punct == None:
                # Make a table that translates all punctuation to an empty value (`None`)
                table = str.maketrans('', '', punctuation)
            else:
                new_punctuation = " ".join([symbol for symbol in punctuation if symbol not in keep_punct])
                table = str.maketrans('', '', new_punctuation)
            reference = tokens_nonpunct(reference, table)
            prediction = tokens_nonpunct(prediction, table)
            report_log('+ Remove punctuation applied', 'V')
        if "remove_digits" in options:
            reference = tokens_nondigits(reference)
            prediction = tokens_nondigits(reference)
            report_log('+ Remove digits applied', 'V')
        if "non_words_remove" in options:
            reference = tokens_non_words(reference)
            prediction = tokens_non_words(reference)
            report_log('+ Non words remove applied', 'V')
        if "remove_fr_stops_words" in options:
            try:
                report_log("...load french stops words base from spaCy...")
                from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
            except:
                report_log("Cannot load french stops words from spaCy.", "E")
            reference = _stop_words_process(reference, fr_stop, append_stop_words, keep_stop_words)
            prediction = _stop_words_process(prediction, fr_stop, append_stop_words, keep_stop_words)
            report_log('+ French stops words filter applied', 'V')
        if "remove_en_stops_words" in options:
            try:
                report_log("...load english stops words base from spaCy...")
                from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
            except:
                report_log("Cannot load english stops words from spaCy.", "E")
            from spacy.lang.en.stop_words import STOP_WORDS as en_stop
            reference = _stop_words_process(reference, en_stop, append_stop_words, keep_stop_words)
            prediction = _stop_words_process(prediction, en_stop, append_stop_words, keep_stop_words)
            report_log('+ English stops words filter applied', 'V')

        report_log('All text preprocessing filters were applied ', "S")

        return reference, prediction

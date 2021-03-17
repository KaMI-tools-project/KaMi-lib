# -*- coding: utf-8 -*-

"""Common code to preprocessing text
"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
import string
import re

from kami.kamutils._utils import (_report_log,
                                  _timing)

## Lambda collection functions ##

# <-- Pass string in lowercase -->
lowercase = lambda sequence: " ".join([token.lower()
                                       for token
                                       in sequence.split()])

# <-- Pass string in uppercase -->
uppercase = lambda sequence: " ".join([token.upper()
                                       for token
                                       in sequence.split()])


# <-- remove starting and finish spaces in sequence -->
stripper = lambda sequence: sequence.strip()

# <-- Remove punctuation from predefined list of symbols from string -->
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

# <-- Remove specific words -->
tokens_remove = lambda sequence, list_words_remove : " ".join([token
                                                               for token
                                                               in sequence.split()
                                                               if token not in list_words_remove])

# <-- Substitute regex patterns in sequence -->
regex_subts = lambda sequence, subts: " ".join([re.sub(key, value, sequence)
                                                for key, value
                                                in subts.items()])

def _stop_words_process(sentence: str,
                        stops_predefined: list,
                        app_swords: list,
                        keep_swords: list) -> str:
    """Remove stops words from sequence.

    Routine of :py:func:`_cleanner()` that optionnal append and remove
    specific users words from predefined list of stop words and apply
    transformation to a specific sequence.

    :Example:

    >>> stop_words = ['le', 'la', 'par', 'de']
    >>> app_swords = ['dans']
    >>> keep_swords = ['la']
    >>> string_user = "le chaperon rouge dans les bois à la recherche de mamie."
    >>> _stop_words_process(string_user, stop_words, keep_swords, app_swords)
    chaperon rouge les bois à la recherche mamie

    :param sentence: string sequence
    :type sentence: str
    :param stops_predefined: list of predefined words
    :type stops_predefined: list
    :param app_swords: stop words added to stops_predefined param
    :type app_swords: list
    :param keep_swords: keep words in stops_predefined
    :type keep_swords: list
    :return: sequence without stops words
    :rtype: str
    """
    lang_stopwords = [stop for stop in stops_predefined]
    if app_swords != None:
        for word in app_swords:
            if word not in lang_stopwords:
                lang_stopwords.append(word.lower())
    if keep_swords != None:
        for word in keep_swords:
            if word in lang_stopwords:
                lang_stopwords.remove(word.lower())

    sequence = " ".join([token
                         for token
                         in sentence.split()
                         if token.lower()
                         not in lang_stopwords])
    return sequence

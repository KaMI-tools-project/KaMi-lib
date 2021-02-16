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



@_timing
def _cleanner(sequence: str,
              functions_clean: list = None,
              keep_punct: list = None,
              append_stop_words: list = None,
              keep_stop_words: list = None,
              _type_sequence: str = None) -> str:
    """Returns a sequence with applied text preprocessing transformations.

    the transformations was defined by user in parameters
    of :py:class:`Composer()`.

    .. note::
        - Text preprocessing steps schema is :
        *lowercase -> remove punctuation -> remove digits ->
        remove non words -> remove stops words*

        - This function return also an global execution time.

    .. seealso::
        Lambda collection functions in same module.

    :param sequence:
    :type sequence:
    :param type_sequence:
    :type type_sequence:
    :param functions_clean:
    :type functions_clean:
    :param keep_punct:
    :type keep_punct:
    :param append_stop_words:
    :type append_stop_words:
    :param keep_stop_words:
    :type keep_stop_words:
    :return:
    :rtype:
    """

    _report_log(f'Init text preprocessing on {_type_sequence} sequence...')

    # Parse options in lower for user
    options = [opt.lower() for opt in functions_clean]
    if "lowercase" in options:
        sequence = lowercase(sequence)
        _report_log(f'+ Lowercase applied on {_type_sequence} sequence.', 'V')
    if "remove_punctuation" in options:
        # Default punct : !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        punctuation = string.punctuation
        if keep_punct == None:
            # Make a table that translates all punctuation to an empty value (`None`)
            table = str.maketrans('', '', punctuation)
        else:
            new_punctuation = " ".join([symbol for symbol in punctuation if symbol not in keep_punct])
            table = str.maketrans('', '', new_punctuation)
        sequence = tokens_nonpunct(sequence, table)
        _report_log(f'+ Remove punctuation applied on {_type_sequence} sequence.', 'V')
    if "remove_digits" in options:
        sequence = tokens_nondigits(sequence)
        _report_log(f'+ Remove digits applied on {_type_sequence} sequence.', 'V')
    if "non_words_remove" in options:
        sequence = tokens_non_words(sequence)
        _report_log(f'+ Non words remove applied on {_type_sequence} sequence.', 'V')
    if "remove_fr_stops_words" in options:
        try:
            _report_log("...load french stops words base from spaCy...")
            from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
        except:
            _report_log("Cannot load french stops words from spaCy.", "E")
        sequence = _stop_words_process(sequence, fr_stop, append_stop_words, keep_stop_words)
        _report_log(f'+ French stops words filter applied on {_type_sequence} sequence.', 'V')
    if "remove_en_stops_words" in options:
        try:
            _report_log("...load english stops words base from spaCy...")
            from spacy.lang.en.stop_words import STOP_WORDS as en_stop
        except:
            _report_log("Cannot load english stops words from spaCy.", "E")
        sequence = _stop_words_process(sequence, en_stop, append_stop_words, keep_stop_words)
        _report_log(f'+ English stops words filter applied on {_type_sequence} sequence.', 'V')

    _report_log(f'All text preprocessing filters were applied on {_type_sequence} sequence.', "S")

    return sequence

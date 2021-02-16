""""""

import string
import re

from kami.kamutils._utils import _report_log
from ._base_preprocessing import _cleanner

class _InitComposer:
    """Private class to control strings (1 or 2 sequences, no empties strings).
    """
    def __init__(self, *strings):
        if len(strings) == 1:
            _report_log('It seems you use kami text preprocessing '
                        'on one string (reference).', 'V')
            self.reference = strings[0]
            self.hypothesis = None
            if len(self.reference) == 0:
                _report_log('It seems your reference string is empty.', 'E')
            else:
                pass


        if len(strings) == 2:
            self.reference = strings[0]
            self.hypothesis = strings[1]
            if len(self.reference) == 0:
                _report_log('It seems your reference string is empty.', 'E')
            if len(self.hypothesis) == 0:
                self.hypothesis = ""
            else:
                pass

        if len(strings) >= 3:
            _report_log(f"The Kami composer deal with only one or two texts/strings.", "E")


class Composer(_InitComposer):
    """
    DOCU
    """
    def __init__(self,
                 *strings,
                 functions_clean=None,
                 keep_punct=None,
                 append_stop_words=None,
                 keep_stop_words=None):

        super().__init__(*strings)

        self.functions_clean = functions_clean
        self.keep_punct = keep_punct
        self.append_stop_words = append_stop_words
        self.keep_stop_words = keep_stop_words

        _type_sequence = None

        if functions_clean is None:
            print('1')
            _report_log('Indicate your clean functions want apply. No filters were applied.', 'W')
            self.reference = self.reference
            self.hypothesis = self.hypothesis

        if self.reference == self.hypothesis \
                and functions_clean is not None:
            print('2')
            self.reference = _cleanner(self.reference,
                                       self.functions_clean,
                                       self.keep_punct,
                                       self.append_stop_words,
                                       self.keep_stop_words,
                                       _type_sequence='same string')
            self.hypothesis = self.reference

        if self.reference != self.hypothesis \
                and functions_clean is not None \
                and self.hypothesis is not None:
            print('3')
            self.reference = _cleanner(self.reference,
                                       self.functions_clean,
                                       self.keep_punct,
                                       self.append_stop_words,
                                       self.keep_stop_words,
                                       _type_sequence='reference',)

            self.hypothesis = _cleanner(self.hypothesis,
                                        self.functions_clean,
                                        self.keep_punct,
                                        self.append_stop_words,
                                        self.keep_stop_words,
                                        _type_sequence='hypothesis')

        if self.hypothesis is None:
            print('4')
            self.reference = _cleanner(self.reference,
                                       self.functions_clean,
                                       self.keep_punct,
                                       self.append_stop_words,
                                       self.keep_stop_words,
                                       _type_sequence='reference')

            self.hypothesis = 'No hypothesis string to perform'

    def __repr__(self):
        """Look up actual state of strings transformations"""

        print("""
        My Kami cleanner text processing
        --------------------------------
        """)
        if self.hypothesis is None:
            print("You applied Kami text preprocessing on one sequence (reference) as standalone program")

        print(f"""
        * Options choosen:
        """)
        if (self.functions_clean and self.keep_punct and self.append_stop_words and  self.keep_stop_words) is None:
            print("""
        No cleanning functions choosen
            """)
        else:
            for function in self.functions_clean:
                print(f"""
        - {function}
                      """)

        print(f"""
        <|> 
        * Actual Reference sequence : {self.reference} 
        <|> 
        """)

        if self.hypothesis is not None:
            print(f"""
        * Actual Hypothesis sequence : {self.hypothesis}
            """)

        return print("-----------------")

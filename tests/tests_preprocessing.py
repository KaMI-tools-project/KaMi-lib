import pytest
import unittest

# from kami.preprocessing._cleanner import cleanner


class testMetrics(unittest.TestCase):
    def setUp(self) -> None:
        """Initialize tests strings"""
        self.reference = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."
        self.prediction = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."
        self.empties_strings = ""

    # 1- Tests on same strings  #
    def test_lower_same(self):
        """test a lower function on same french strings"""
        r, h = cleanner(self.reference,
                        self.reference,
                        functions_clean=["lowercase"])
        assert (r and h) == "les 13 ans de maxime ? étaient, déjà terriblement, savants ! - la curée, 1871. en avant, pour la lecture."

    def test_nopunc_same(self):
        """test a no punctuation function on same french strings"""
        r, h = cleanner(self.reference,
                        self.reference,
                        functions_clean=["remove_punctuation"])
        assert (r and h) == "Les 13 ans de Maxime  étaient Déjà terriblement savants   La Curée 1871 En avant pour la lecture"

    def test_nopunc_opts_same(self):
        """test a lowercase and no punctuation functions combine with options to preserve symbols predefined on same french strings"""
        r, h = cleanner(self.reference,
                        self.reference,
                        functions_clean=["lowercase",
                                 "remove_punctuation"],
                        keep_punct=['?', '!']
                        )
        assert (r and h) == "les 13 ans de maxime ? étaient déjà terriblement savants !  la curée 1871 en avant pour la lecture"

    def test_nodigits_same(self):
        """test a non-digits function on same french strings"""
        r, h = cleanner(self.reference,
                        self.reference,
                        functions_clean=["remove_digits"])
        assert (r and h) == "Les ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, . En avant, pour la lecture."

    def test_nowords_same(self):
        """test a non word remove function on same french strings"""
        r, h = cleanner(self.reference,
                        self.reference,
                        functions_clean=["non_words_remove"])
        assert (r and h) == "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."

    def test_stopswordsfr_same(self):
        """test a french stop words remove function on same french strings"""
        r, h = cleanner(self.reference,
                        self.reference,
                        functions_clean=["remove_fr_stops_words"])
        assert (r and h) == "13 ans Maxime ? étaient, Déjà terriblement, savants ! - Curée, 1871. avant, lecture."

    def test_stopswordsfr_opts_same(self):
        """test a french stop words remove function with options on same french strings"""
        r, h = cleanner(self.reference,
                        self.reference,
                        functions_clean=["remove_fr_stops_words"],
                        append_stop_words=['ans'],
                        keep_stop_words=['en', 'pour'])
        assert (r and h) == "13 Maxime ? étaient, Déjà terriblement, savants ! - Curée, 1871. En avant, pour lecture."

    def test_all_same(self):
        """test all functions and all options on same french strings"""
        r, h = cleanner(self.reference,
                        self.reference,
                        functions_clean=["lowercase",
                                         "non_words_remove",
                                         "remove_punctuation",
                                         "remove_digits",
                                         "remove_fr_stops_words"],
                        keep_punct=['?', '!'],
                        append_stop_words=['ans'],
                        keep_stop_words=['en', 'pour'])

        assert (r and h) == "maxime ? déjà terriblement savants ! curée en pour lecture"

    # 2- Tests with no strings or on one string  #
    def test_no_strings(self):
        """tests all functions with no strings"""
        r, h = cleanner(self.empties_strings,
                        self.empties_strings,
                        functions_clean=["lowercase",
                                         "non_words_remove",
                                         "remove_punctuation",
                                         "remove_digits",
                                         "remove_fr_stops_words"],
                        keep_punct=['?', '!'],
                        append_stop_words=['ans'],
                        keep_stop_words=['en', 'pour'])

        assert (r and h) == ""

    def test_one_string(self):
        r, h = cleanner(self.reference,
                        self.empties_strings,
                        functions_clean=["lowercase",
                                         "non_words_remove",
                                         "remove_punctuation",
                                         "remove_digits",
                                         "remove_fr_stops_words"],
                        keep_punct=['?', '!'],
                        append_stop_words=['ans'],
                        keep_stop_words=['en', 'pour'])



    # TODO(Luca) : write a test with no strings and with one string reference
    # missing positional argument
    # TODO(Luca) : tests with different french strings
    # TODO(Luca) : tests with english strings
    # TODO(Luca) : tests with differents english strings
    # TODO(Luca) : write a test with error
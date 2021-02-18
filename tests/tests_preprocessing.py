import pytest
import unittest

from kami.preprocessing.transformation import Composer


class testMetrics(unittest.TestCase):
    def setUp(self) -> None:
        """Initialize tests strings"""
        self.reference = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."
        self.prediction = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."
        self.empties_strings = ""

    # 1- Tests on same strings  #
    def test_lower_same(self):
        """test a lower function on same french strings"""
        composer_test = Composer(self.reference,
                        self.reference,
                        functions_clean=["lowercase"])
        assert (composer_test.reference and composer_test.hypothesis) == "les 13 ans de maxime ? étaient, déjà terriblement, savants ! - la curée, 1871. en avant, pour la lecture."

    def test_nopunc_same(self):
        """test a no punctuation function on same french strings"""
        composer_test = Composer(self.reference,
                        self.reference,
                        functions_clean=["remove_punctuation"])
        assert (composer_test.reference and composer_test.hypothesis) == "Les 13 ans de Maxime  étaient Déjà terriblement savants   La Curée 1871 En avant pour la lecture"

    def test_nopunc_opts_same(self):
        """test a lowercase and no punctuation functions combine with options to preserve symbols predefined on same french strings"""
        composer_test = Composer(self.reference,
                        self.reference,
                        functions_clean=["lowercase",
                                 "remove_punctuation"],
                        keep_punct=['?', '!']
                        )
        assert (composer_test.reference and composer_test.hypothesis) == "les 13 ans de maxime ? étaient déjà terriblement savants !  la curée 1871 en avant pour la lecture"

    def test_nodigits_same(self):
        """test a non-digits function on same french strings"""
        composer_test = Composer(self.reference,
                        self.reference,
                        functions_clean=["remove_digits"])
        assert (composer_test.reference and composer_test.hypothesis) == "Les ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, . En avant, pour la lecture."

    def test_nowords_same(self):
        """test a non word remove function on same french strings"""
        composer_test = Composer(self.reference,
                        self.reference,
                        functions_clean=["non_words_remove"])
        assert (composer_test.reference and composer_test.hypothesis) == "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."

    def test_stopswordsfr_same(self):
        """test a french stop words remove function on same french strings"""
        composer_test = Composer(self.reference,
                        self.reference,
                        functions_clean=["remove_fr_stops_words"])
        assert (composer_test.reference and composer_test.hypothesis) == "13 ans Maxime ? étaient, Déjà terriblement, savants ! - Curée, 1871. avant, lecture."

    def test_stopswordsfr_opts_same(self):
        """test a french stop words remove function with options on same french strings"""
        composer_test = Composer(self.reference,
                        self.reference,
                        functions_clean=["remove_fr_stops_words"],
                        append_stop_words=['ans'],
                        keep_stop_words=['en', 'pour'])
        assert (composer_test.reference and composer_test.hypothesis) == "13 Maxime ? étaient, Déjà terriblement, savants ! - Curée, 1871. En avant, pour lecture."

    def test_all_same(self):
        """test all functions and all options on same french strings"""
        composer_test = Composer(self.reference,
                        self.reference,
                        functions_clean=["lowercase",
                                         "non_words_remove",
                                         "remove_punctuation",
                                         "remove_digits",
                                         "remove_fr_stops_words"],
                        keep_punct=['?', '!'],
                        append_stop_words=['ans'],
                        keep_stop_words=['en', 'pour'])

        assert (composer_test.reference and composer_test.hypothesis) == "maxime ? déjà terriblement savants ! curée en pour lecture"

    # 2- Tests with no strings or on one string  #
    def test_no_strings(self):
        """tests all functions with no strings"""
        with pytest.raises(AttributeError) as e:
            Composer(functions_clean=["lowercase",
                                         "non_words_remove",
                                         "remove_punctuation",
                                         "remove_digits",
                                         "remove_fr_stops_words"],
                        keep_punct=['?', '!'],
                        append_stop_words=['ans'],
                        keep_stop_words=['en', 'pour'])
        assert str(e.value) == "'Composer' object has no attribute 'reference'"





    def test_one_string(self):
        composer_test = Composer(self.reference,
                        functions_clean=["lowercase",
                                         "non_words_remove",
                                         "remove_punctuation",
                                         "remove_digits",
                                         "remove_fr_stops_words"],
                        keep_punct=['?', '!'],
                        append_stop_words=['ans'],
                        keep_stop_words=['en', 'pour'])

        assert composer_test.reference =="maxime ? déjà terriblement savants ! curée en pour lecture" \
               and \
               composer_test.hypothesis == "No hypothesis string to perform"




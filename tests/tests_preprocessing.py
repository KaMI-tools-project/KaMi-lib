import pytest
import unittest

from kami.preprocessing._cleanner import cleanner


class testMetrics(unittest.TestCase):
    reference = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."
    prediction = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."

    def test_lower_same(self):
        r, h = cleanner(self.reference, self.reference, options=["lowercase"])
        assert (r and h) == "les 13 ans de maxime ? étaient, déjà terriblement, savants ! - la curée, 1871. en avant, pour la lecture."

    def test_nopunc_same(self):
        r, h = cleanner(self.reference, self.reference, options=["remove_punctuation"])
        assert (r and h) == "Les 13 ans de Maxime  étaient Déjà terriblement savants   La Curée 1871 En avant pour la lecture"

        #TODO(Luca) : write a test with punc options

    def test_nodigits_same(self):
        r, h = cleanner(self.reference, self.reference, options=["remove_digits"])
        assert (r and h) == "Les ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, . En avant, pour la lecture."

    def test_nowords_same(self):
        r, h = cleanner(self.reference, self.reference, options=["non_words_remove"])
        assert (r and h) == "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."

    def test_stopswordsfr_same(self):
        r, h = cleanner(self.reference, self.reference, options=["remove_fr_stops_words"])
        assert (r and h) == "13 ans Maxime ? étaient, Déjà terriblement, savants ! - Curée, 1871. avant, lecture."

        # TODO(Luca) : write a test with fr stops words options

    def test_all_same(self):
        r, h = cleanner(self.reference, self.reference, options=["lowercase",
                                                                 "non_words_remove",
                                                                 "remove_punctuation",
                                                                 "remove_digits",
                                                                 "remove_fr_stops_words"])

        assert r,h == "ans maxime déjà terriblement savants curée lecture"

    # TODO(Luca) : write a test with all func and all options
    # TODO(Luca) : write a test with no strings
    # TODO(Luca) : write a test with error
import unittest

from kami.Kami import Kami


class testKamiClient(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

        self.reference = "Six semaines plus tard, Claude peignait un matin dans un flot de soleil qui tombait par la baie vitrée de l’atelier."
        self.prediction = "Six semaiNEs plus tard, lCCaude peignait un MA dans un flotille de soleil qui tombait baie vitrée de l’atelier."

        self.gt_page = "../datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_page.xml"
        self.image_page = "../datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0.png"
        self.model_page = "../datatest/lectaurep_set/models/mixte_mrs_15.mlmodel"

    """
    def test_sentences(self):
        k1 = Kami([self.reference, self.prediction], verbosity=False, truncate=True, percent=True, round_digits='0.01')
        self.assertEqual(k1.scores.board, {'levensthein_distance_char': 20,
                                          'levensthein_distance_words': 6,
                                          'hamming_distance': 'Ø',
                                          'wer': 28.57,
                                          'cer': 17.24,
                                          'wacc': 71.42,
                                          'mer': 16.52,
                                          'cil': 20.77,
                                          'cip': 79.22,
                                          'hits': 101,
                                          'substitutions': 5,
                                          'deletions': 10,
                                          'insertions': 5})

    def test_page(self):
        k2 = Kami(self.gt_page, model=self.model_page, image=self.image_page, verbosity=False, truncate=True, percent=True, round_digits='0.01')

        self.assertEqual(k2.scores.board, {'cer': 0.49,
                                           'cil': 0.59,
                                           'cip': 99.4,
                                           'deletions': 0,
                                           'hamming_distance': 'Ø',
                                           'hits': 1002,
                                           'insertions': 4,
                                           'levensthein_distance_char': 5,
                                           'levensthein_distance_words': 2,
                                           'mer': 0.49,
                                           'substitutions': 1,
                                           'wacc': 98.94,
                                           'wer': 1.05})
    """
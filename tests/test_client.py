import unittest

from kami.Kami import Kami


class testKamiClient(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

        self.reference = "Six semaines plus tard, Claude peignait un matin dans un flot de soleil qui tombait par la baie vitrée de l’atelier."
        self.prediction = "Six semaiNEs plus tard, lCCaude peignait un MA dans un flotille de soleil qui tombait baie vitrée de l’atelier."

        self.gt_text = "./datatest/text_jpeg/GT_1.txt"
        self.gt_page = "./datatest/page_jpeg/22_c266f_default_PAGE.xml"

        self.image_text = "./datatest/text_jpeg/Voyage_au_centre_de_la_[...]Verne_Jules_btv1b8600259v_16.jpeg"
        self.image_page = "./datatest/page_jpeg/22_c266f_default_PAGE.jpeg"

        self.model_text = "./datatest/on_hold/KB-app_model_JulesVerne1_best.mlmodel"
        self.model_page = "./datatest/models/model_tapuscrit_n2_(1).mlmodel"

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

    def test_text(self):
        k3 = Kami(self.gt_text, model=self.model_text, image=self.image_text, verbosity=False, truncate=True, percent=True, round_digits='0.01')

        self.assertEqual(k3.scores.board, {'cer': 6.62,
                                           'cil': 9.55,
                                           'cip': 90.44,
                                           'deletions': 59,
                                           'hamming_distance': 'Ø',
                                           'hits': 2398,
                                           'insertions': 30,
                                           'levensthein_distance_char': 168,
                                           'levensthein_distance_words': 90,
                                           'mer': 6.54,
                                           'substitutions': 79,
                                           'wacc': 79.54,
                                           'wer': 20.45})
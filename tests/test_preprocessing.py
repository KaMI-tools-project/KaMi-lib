import unittest

from kami.preprocessing.transformation import (ToLowerCase,
                                               ToUpperCase,
                                               RemovePunctuation,
                                               RemoveDiacritics,
                                               RemoveDigits,
                                               RemoveNonUsefulWords,
                                               RemoveSpecificWords,
                                               Strip,
                                               SubRegex,
                                               ToCompose)


class testPreprocessing(unittest.TestCase):
    def setUp(self) -> None:
        self.sentence = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."

    def test_removeLowercase(self):
        transform = ToLowerCase()(self.sentence)
        self.assertEqual(transform, "les 13 ans de maxime ? étaient, déjà terriblement, savants ! - la curée, 1871. en avant, pour la lecture.")

    def test_removeUppercase(self):
        transform = ToUpperCase()(self.sentence)
        self.assertEqual(transform, "LES 13 ANS DE MAXIME ? ÉTAIENT, DÉJÀ TERRIBLEMENT, SAVANTS ! - LA CURÉE, 1871. EN AVANT, POUR LA LECTURE.")

    def test_removePunct(self):
        transform = RemovePunctuation()(self.sentence)
        self.assertEqual(transform, "Les 13 ans de Maxime  étaient Déjà terriblement savants   La Curée 1871 En avant pour la lecture")

    def test_removeDiacritics(self):
        transform = RemoveDiacritics()(self.sentence)
        self.assertEqual(transform, "Les 13 ans de Maxime ? etaient, Deja terriblement, savants ! - La Curee, 1871. En avant, pour la lecture.")

    def test_removeDigits(self):
        transform = RemoveDigits()(self.sentence)
        self.assertEqual(transform, "Les  ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, . En avant, pour la lecture.")

    def test_removeNonUsefulWords(self):
        transform = RemoveNonUsefulWords()(self.sentence)
        self.assertEqual(transform, "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture.")

    def test_removeSpecificWords(self):
        words_to_remove = ["Maxime", "Déjà"]
        transform = RemoveSpecificWords(words_to_remove=words_to_remove)(self.sentence)
        self.assertEqual(transform, "Les 13 ans de ? étaient, terriblement, savants ! - La Curée, 1871. En avant, pour la lecture.")

    def test_strip(self):
        transform = Strip()(self.sentence)
        self.assertEqual(transform, "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture.")

    def test_subRegex(self):
        substitutions = {"[L|l]\w+": "-- REPLACE --"}
        transform = SubRegex(substitutions=substitutions)(self.sentence)
        self.assertEqual(transform, "-- REPLACE -- 13 ans de Maxime ? étaient, Déjà terrib-- REPLACE --, savants ! - -- REPLACE -- Curée, 1871. En avant, pour -- REPLACE -- -- REPLACE --.")

    def test_multipleReplace(self):
        transform = ToCompose([self.sentence, ""], [RemoveDiacritics(), RemovePunctuation(), ToLowerCase(), RemoveNonUsefulWords()])
        self.assertEqual(transform.reference, "les 13 ans de maxime etaient deja terriblement savants la curee 1871 en avant pour la lecture")






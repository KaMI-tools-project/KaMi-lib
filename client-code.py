#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kami.Kami import Kami
from kami.preprocessing.transformation import (ToCompose,
                                               ToLowerCase,
                                               ToUpperCase,
                                               RemovePunctuation,
                                               Strip,
                                               RemoveNonUsefulWords,
                                               RemoveSpecificWords,
                                               RemoveDigits)
import pprint
import re

#############################
# Entry Point : code client #
# *  Use for test only  *   #
# change the code in
# client_code()             #
#############################

def client_code() -> None:
    """
    The client code works with complex subsystems through a simple interface
    provided by the Kami Facade. The client might not even know about the existence of the
    Kami subsystems.

    """

    file = "datatest/text_jpeg/GT_1.txt"
    textfile_gt2 = "./datatest/GT_2.txt"

    page_file = "datatest/page_jpeg/22_c266f_default_PAGE.xml"
    image = "./datatest/text_jpeg/Voyage_au_centre_de_la_[...]Verne_Jules_btv1b8600259v_16.jpeg"
    image_page = "./datatest/page_jpeg/22_c266f_default_PAGE.jpeg"
    model = "./datatest/on_hold/KB-app_model_JulesVerne1_best.mlmodel"
    model_page = "./datatest/models/model_tapuscrit_n2_(1).mlmodel"

    ground_truth = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."
    hypothesis = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."





    k = Kami([ground_truth, hypothesis], verbosity=False, truncate=True, percent=True, round_digits='0.01')
    reference = k.reference
    prediction = k.prediction

    print(reference)
    print("--------------------")
    print(prediction)

    pprint.pprint(k.scores.board)






if __name__ == "__main__":
    client_code()

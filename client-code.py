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

    # Select ground truth (raw text, sequences and XML PAGE also support),
    # image (.jpeg/.jpg only),
    # and  transcription model (.mlmodel only, you can use Kraken to create one).
    # Tips : Use files in datatest/ directory to test freely
    file = "datatest/text_jpeg/GT_1.txt"
    image = "./datatest/text_jpeg/Voyage_au_centre_de_la_[...]Verne_Jules_btv1b8600259v_16.jpeg"
    model = "./datatest/on_hold/KB-app_model_JulesVerne1_best.mlmodel"

    # Create a kami object

    k = Kami(file,  # Apply ground truth file here
             model=model,  # Apply HTR/OCR model here
             image=image,  # Apply image here
             apply_transforms="XP",  # Compute with some transformations as remove diacritics and punctuations
             # (List transformations : D : digits / U : uppercase / L : lowercase / P : punctuation / X : diacritics [OPTIONAL])
             verbosity=False,  # Add some comments during process
             truncate=True,  # Truncate final scores
             percent=True,  # Indicate scores in percent
             round_digits='0.01')  # number of digits after floating point


    # Get the reference text
    print(k.reference)

    print(f"\n{'-' * 20}\n")

    # Get the prediction text
    print(k.prediction)

    print(f"\n{'=' * 20}\n")

    # Get the reference modified with transforms
    print(k.reference_preprocess)

    print(f"\n{'*' * 20}\n")

    # Get the prediction modified with transforms
    print(k.prediction_preprocess)

    print(f"\n{'*' * 20}\n")

    # Get all scores
    pprint.pprint(k.scores.board)






if __name__ == "__main__":
    client_code()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kami.kami import Kami
import pprint

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


    textfile_gt = "./datatest/GT_1.txt"

    page_file = "./datatest/22_c266f_default_PAGE.xml"
    image = "./datatest/Voyage_au_centre_de_la_[...]Verne_Jules_btv1b8600259v_16.jpeg"
    image_page = "./datatest/22_c266f_default_PAGE.jpg"
    model = "./datatest/on_hold/KB-app_model_JulesVerne1_best.mlmodel"
    model_page = "./datatest/models/model_tapuscrit_n2_(1).mlmodel"

    k = Kami(textfile_gt, image=image, model=model, verbosity=True, truncate=True, round_digits='.001')
    reference = k.reference
    prediction = k.prediction

    print(reference)
    print("--------------------")
    print(prediction)

    pprint.pprint(k.scores.board, sort_dicts=False)









if __name__ == "__main__":
    client_code()

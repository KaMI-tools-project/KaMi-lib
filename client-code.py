#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kami.kami import Kami


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
    my_sentences = ["Ceci est une phrase correcte, sans problème", "CETTE phrase comporte des incertiREdutes"]
    k = Kami(my_sentences, truncate=True)




    textfile_gt = "./datatest/GT_1.txt"
    image = "./datatest/Voyage_au_centre_de_la_[...]Verne_Jules_btv1b8600259v_16.jpeg"
    model = "./datatest/on_hold/KB-app_model_JulesVerne1_best.mlmodel"

    k = Kami(textfile_gt, image=image, model=model)
    print(k.scores.board)









if __name__ == "__main__":
    client_code()

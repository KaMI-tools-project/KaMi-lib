#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import time
from kami.Kami import Kami
from kami.preprocessing.transformation import (ToCompose,
                                               ToLowerCase,
                                               ToUpperCase,
                                               RemovePunctuation,
                                               Strip,
                                               RemoveNonUsefulWords,
                                               RemoveSpecificWords,
                                               RemoveDigits)



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

    # TEST DATA (change with your own data)
    # Sentences 
    ground_truth = "Les 13 ans de Maxime ? étaient, Déjà terriblement, savants ! - La Curée, 1871. En avant, pour la lecture."
    prediction = "Les 14a de Maxime ! étaient, djàteriblement, savants - La Curée, 1871. En avant? pour la leTTture."
    # Text files
    textfile_gt = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_gt.txt"
    textfile_pred = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_prediction_finetuned.txt"
    # XML
    alto_gt = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_alto.xml"
    page_gt = "./datatest/medium_set/FRAN_0150_0002_L-medium_page.xml"
    # Model
    model_medium = "./datatest/medium_set/model_tapuscrit_n2_(1).mlmodel"
    model_lectaurep = "./datatest/lectaurep_set/models/mixte_mrs_15.mlmodel"
    image_medium = "./datatest/medium_set/FRAN_0150_0002_L-medium.jpg"
    image_lectaurep = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0.png"


    # to Memory 
    """
    k = Kami(file,  # Apply ground truth file here
             model=model,  # Apply HTR/OCR model here
             image=image,  # Apply image here
             apply_transforms="XP",  # Compute with some transformations as remove diacritics and punctuations
             # (List transformations : D : digits / U : uppercase / L : lowercase / P : punctuation / X : diacritics [OPTIONAL])
             verbosity=False,  # Add some comments during process
             truncate=True,  # Truncate final scores
             percent=True,  # Indicate scores in percent
             round_digits='0.01')  # number of digits after floating point
    """
    current_all = time.time()
    current = time.time()
    # TEST CASES
    # Part 1 : Agnostic OCR/HTR engines uses cases
    # A : Compare two sequences of character
    print("PART 1 - A \n")
    k = Kami([ground_truth, prediction])  
    print(k.scores.board)
    print(k.scores.wer)
    print(f"\n * TOTAL Time P1A : {time.time() - current}")
    print("="*10)
    # B : Compare two text file
    current = time.time()
    print("PART 1 - B \n")
    k = Kami([textfile_gt, textfile_pred],
             apply_transforms="", 
             verbosity=False,  
             truncate=True,  
             percent=True,  
             round_digits='0.01')  
    print(k.scores.board)
    print(f"\n * TOTAL Time P1B : {time.time() - current}")
    print("="*10)
    # C : Compare two sequences of character (with preprocess/severity)
    current = time.time()
    print("PART 1 - C \n")
    k = Kami([ground_truth, prediction],
             apply_transforms="DUP", 
             verbosity=False,  
             truncate=True,  
             percent=True,  
             round_digits='0.01')  
    print(k.scores.board)
    print(f"\n * TOTAL Time P1C : {time.time() - current}")
    print("="*10)
    # D : Compare two text file (with preprocess/severity)
    current = time.time()
    print("PART 1 - D \n")
    k = Kami([textfile_gt, textfile_pred],
             apply_transforms="DUP", 
             verbosity=False,  
             truncate=True,  
             percent=True,  
             round_digits='0.01')  
    print(k.scores.board)
    print(f"\n * TOTAL Time P1D: {time.time() - current}")
    print("="*10)

    # Part 2 : Kraken uses cases
    # A : Compare XML ALTO + model, image with kraken prediction  output
    current = time.time()
    print("PART 2 - A \n")
    k = Kami(alto_gt,
             model=model_lectaurep,
             image=image_lectaurep)  
    print(k.scores.board)
    print(f"\n * TOTAL Time P2A: {time.time() - current}")
    print("="*10)
    # B : Compare XML PAGE + model, image with kraken prediction  output
    current = time.time()
    print("PART 2 - B \n")
    k = Kami(page_gt,
             model=model_medium,
             image=image_medium,
             apply_transforms="", 
             verbosity=False,  
             truncate=True,  
             percent=True,  
             round_digits='0.01')  
    print(k.scores.board)
    print(f"\n * TOTAL Time P2B: {time.time() - current}")
    print("="*10)
    # C : Compare XML ALTO + model, image with kraken prediction  output (with preprocess/severity)
    current = time.time()
    try:
        print("PART 2 - C \n")
        k = Kami(alto_gt,
             model=model_lectaurep,
             image=image_lectaurep,
             apply_transforms="XLP", 
             verbosity=False,  
             truncate=True,  
             percent=True,  
             round_digits='0.01')  
        print(k.scores.board)
        print(f"\n * TOTAL Time P2C: {time.time() - current}")
        print("="*10)
    except:
        print("no alto implementation here")
    # D : Compare XML PAGE + model, image with kraken prediction  output (with preprocess/severity)
    current = time.time()
    print("PART 2 - D \n")
    k = Kami(page_gt,
             model=model_medium,
             image=image_medium,
             apply_transforms="XLP", 
             verbosity=False,  
             truncate=True,  
             percent=True,  
             round_digits='0.01')  
    print(k.scores.board)
    print(f"\n * TOTAL Time P2D: {time.time() - current}")
    print("="*10)

    # Part 3 : Error cases 
    # A : Compare text file + model, image with kraken prediction output
    # B : Forget model
    # C : Forget image
    # D : Forget alto, page
    # E : Forget sentence to compare
    # F : Forget a text file to compare

    print(f"\n * TOTAL Time spent with client code : {time.time() - current_all}")

  






if __name__ == "__main__":
    client_code()

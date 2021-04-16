# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
#           Alix Chagué <alix.chague@inria.fr>
# Licence : MIT
"""
    The ``Prediction`` module to generate HTR/OCR pipeline on data
    ==============================================================

"""
from kami.transcription._base_prediction import _binarize_image, _segment_image, _predict_transcription
from kraken import rpred
import unicodedata
from kami.kamutils._utils import _report_log
import sys



class Prediction:
    def __init__(self, image, model_loaded, verbosity=False):
        self.image = image
        self.model = model_loaded
        self.verbosity = verbosity

    def get_transcription_txt(self):
        """built from images and an offline recognition model of the text
            of the separate transcripts for each image.
            Process
            -------
            * 2- Binarization
            * 3- Segmentation
            * 4- Text recognition
            * 5- Convert transcription kraken object in string format

            Args:
                images_loaded (list): list of user's images
                model_loaded (<object>): loaded kraken model
                verbosity (bool): if user activate verbose option

            Returns:
                list: list contains the text prediction
            """
        _report_log(f"{'#' * 10} HTR/OCR Pipeline initialize ... {'#' * 10}", "I")
        image_binarized = _binarize_image(self.image, self.verbosity)
        image_segmented = _segment_image(image_binarized, self.verbosity)
        # create binarized image-segmented image pairs in order to create text recognition
        pair_image_segments = (image_binarized, image_segmented)
        prediction = _predict_transcription(pair_image_segments, self.model, self.verbosity)

        _report_log(f"{'#' * 10} Kraken object in string format converted  {'#' * 10}", "S")
        canvas = ""
        try:
            for line in prediction:
                # .prediciton is a kraken_ocr_record class attribute for recover the text in
                # kraken.rpred.mm_rpred object
                canvas += f"{unicodedata.normalize('NFC', line.prediction)}"
        except Exception as exception:
                _report_log(f"Error : unable to transcribe - {prediction}", "E")
                _report_log(f"type : {exception}")
                sys.exit('program exit')


        return canvas
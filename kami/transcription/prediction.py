# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
#           Alix Chagué <alix.chague@inria.fr>
# Licence : MIT
"""
    The ``Prediction`` module to generate HTR/OCR pipeline on data
    ==============================================================

"""
import unicodedata
import sys

from kraken import rpred

from kami.kamutils._utils import _report_log
from kami.transcription._base_prediction import _binarize_image, _segment_image, _predict_transcription


class Prediction:
    def __init__(self, filename, image, model_loaded, verbosity, reference=None):
        self.filename = filename
        self.image = image
        self.model = model_loaded
        self.verbosity = verbosity
        self.reference = reference

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
        if self.verbosity:
            _report_log(f"{'#' * 10} HTR/OCR Pipeline initialize for text file : {self.filename} ... {'#' * 10}", "I")

        image_bin = _binarize_image(self.image, self.verbosity)

        image_segmented = _segment_image(image_bin, self.verbosity)
        # create binarized image-segmented image pairs in order to create text recognition

        prediction = _predict_transcription(image=image_bin,
                                            bound=image_segmented,
                                            model_loaded=self.model,
                                            verbosity=self.verbosity)
        if self.verbosity:
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

    def get_transcription_xml(self):
        """Generate a transcription from a series of images and coordinates
        Parameters
        ----------
        images_loaded (list): images loaded with PIL
        model_loaded (object): mlmodel loaded with kraken
        ground_truth_files (list): list of PagexmlParser
        verbosity (bool): (unused)

        Returns (list): transcriptions (a list of str)
        -------

        """

        if self.verbosity:
            _report_log(f"{'#' * 10} HTR/OCR Pipeline initialize for XML file : {self.filename} ... {'#' * 10}", "I")

        canvas = ""
        for bound in self.reference.bounds:
            prediction = _predict_transcription(image=self.image,
                                                bound=bound,
                                                model_loaded=self.model,
                                                verbosity=self.verbosity)

        canvas += "".join(prediction) + "\n"

        # run the model and get a prediction -> https://github.com/mittagessen/kraken/blob/master/kraken/rpred.py#L353
        # return a list of transcription (can we have the same type of objects as
        # get_transcriptions_txt()
        return canvas

# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
#           Alix Chagué <alix.chague@inria.fr>
# Licence : MIT
"""
    The ``Prediction`` module to generate HTR/OCR pipeline on data
    ==============================================================

"""
import unicodedata

from kami.kamutils._utils import _report_log
from kami.transcription._base_prediction import (_binarize_image,
                                                 _segment_image,
                                                 _predict_transcription)

__all__ = [
    "_Prediction",
]

class _Prediction:
    """this class create a prediction from an offline model, image, and ground truth file.

    User cannot access to this class via :class: `Kami` facade class.
    """
    def __init__(self, filename, image, model_loaded, verbosity, code, reference=None):
        self.filename = filename
        self.image = image
        self.model = model_loaded
        self.verbosity = verbosity
        self.code = code
        self.reference = reference

    def get_transcription(self):
        """built from image/coordinates and an offline recognition model of the text/xml
        a transcript.

        Process Text
        ------------
        * 1- Binarization
        * 2- Segmentation
        * 3- Prediction (Text recognition)
        * 4- Convert transcription kraken object in string format

        Process XML
        ------------
        * 1- Extract Segments/Bounds
        * 2- Prediction (Text recognition)
        * 3- Convert transcription kraken object in string format
        """

        if self.verbosity:
            _report_log(
                f"{'#' * 10} HTR/OCR Pipeline initialize "
                f"for {self.code} file : {self.filename} ... "
                f"{'#' * 10}",
                "I"
            )

        canvas = ""

        try:
            if self.code == "txt":
                image_bin = _binarize_image(self.image, self.verbosity)
                image_seg = _segment_image(image_bin, self.verbosity)
                prediction = _predict_transcription(image=image_bin,
                                                    bound=image_seg,
                                                    model_loaded=self.model,
                                                    verbosity=self.verbosity,
                                                    code="txt")
                for line in prediction:
                    # .prediction is a kraken_ocr_record class attribute for recover the text in
                    # kraken.rpred.mm_rpred object
                    canvas += f"{unicodedata.normalize('NFC', line.prediction)}" + "\n"
                    if self.verbosity:
                        _report_log(
                            f"{'#' * 10} Kraken object "
                            f"in string format converted  {'#' * 10}",
                            "S"
                        )

            if self.code == "xml":
                for bound in self.reference.bounds:
                    prediction = _predict_transcription(image=self.image,
                                                        bound=bound,
                                                        model_loaded=self.model,
                                                        verbosity=self.verbosity,
                                                        code="xml")

                    canvas += f"{unicodedata.normalize('NFC', prediction)}" + "\n"
                    if self.verbosity:
                        _report_log(
                            f"{'#' * 10} Kraken object in "
                            f"string format converted  {'#' * 10}",
                            "S"
                        )

        except Exception as exception:
            _report_log(
                f"Error : unable to transcribe {self.code} file",
                "E"
            )
            _report_log(
                f"type : {exception}"
            )

        # run the model and get a
        # prediction -> https://github.com/mittagessen/kraken/blob/master/kraken/rpred.py#L353
        # return a list of transcription (can we have the same type of objects as
        # get_transcriptions_txt()
        return canvas

    def __str__(self):
        return f"Prediction(\n" \
               f"filename={self.filename},\n" \
               f"image={self.image},\n" \
               f"model={self.model}),\n" \
               f"verbosity={self.verbosity},\n" \
               f"code={self.code},\n" \
               f"reference={self.reference}"

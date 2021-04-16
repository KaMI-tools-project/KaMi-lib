# -*- coding: utf-8 -*-
# Authors : Alix Chagué <alix.chague@inria.fr>
#           Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""Client interface calls several sub-system of Kami-lib
"""

from typing import Union

from kami.transcription._base_prediction_io import _load_model, _load_image

from kami.parser import parser_text, parser_page
from kami.metrics.evaluation import Scorer
from kami.transcription.prediction import Prediction

class Kami:
    """
    This is a Facade class provides a simple interface to the complex logic of one or
    several subsystems in Kami. This hide a complexity of Kami subsystems.
    """

    def __init__(self,
                 data: Union[str, list],
                 image="",
                 model="",
                 binarize=False,
                 verbosity=False,
                 truncate=False
                 ) -> None:
        """
        """
        self.reference = None
        self.prediction = None
        self.model = None
        self.scores = None

        self.truncate = truncate
        self.verbosity = verbosity
        self.binarize = binarize

        if isinstance(data, list) and len(data) > 1:
            # case with two text files => compute score
            if data[0].endswith('txt') and data[1].endswith('txt'):
                self.reference = parser_text.TextParser(data[0]).text
                self.prediction = parser_text.TextParser(data[1]).text
            # case with two strings => compute score
            else:
                self.reference = data[0]
                self.prediction = data[1]

            self.scores = Scorer(self.reference,
                                 self.prediction,
                                 truncate_score=self.truncate)

        # case with GT RAW TEXT file => create a HTR pipeline => compute scores
        elif isinstance(data, str) and data.endswith('txt'):
            self.reference = parser_text.TextParser(data).text
            self.model = _load_model(model)
            self.image = _load_image(image, verbosity=self.verbosity)
            pipeline = Prediction(self.image, self.model)
            self.prediction = pipeline.get_transcription_txt()
            self.scores = Scorer(self.reference,
                                 self.prediction,
                                 truncate_score=self.truncate)

        # case with GT XML PAGE => create a HTR pipeline => compute scores
        elif isinstance(data, str) and data.endswith('xml'):
            self.reference = parser_page.PageParser(data)
            # TODO : pass transcription part
            # TODO : pass the scorer part

        else:
            raise ValueError("Something is wrong. Check your data.")
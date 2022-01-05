# -*- coding: utf-8 -*-
# Authors : Alix Chagué <alix.chague@inria.fr>
#           Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""Client interface calls several sub-system of Kami-lib
"""
import os.path
from typing import Union

from kami.parser import (parser_text,
                         parser_page)
from kami.preprocessing.transformation import (RemoveDigits,
                                               ToLowerCase,
                                               ToUpperCase,
                                               RemovePunctuation,
                                               RemoveDiacritics,
                                               _Composer,
                                               count_diacritics)
from kami.transcription._base_prediction_io import (_load_model,
                                                    _load_image)
from kami.transcription.prediction import _Prediction
from kami.metrics.evaluation import Scorer


class Kami:
    """A Facade class provides a simple interface to the complex logic of one or
    several subsystems in Kami.

    This hide a complexity of Kami subsystems as :
    * Preprocessing
    * Prediction
    * Metrics
    """

    def __init__(self,
                 data: Union[str, list],
                 image="",
                 model="",
                 apply_transforms="",
                 verbosity=False,
                 truncate=False,
                 percent=False,
                 round_digits='.01'
                 ) -> None:
        # Inputs

        self.reference = None
        self.prediction = None
        self.model = None
        self.scores = None
        self.apply_transforms = [code for line in apply_transforms.split() for code in line]

        # Options

        self.truncate = truncate
        self.percent = percent
        self.verbosity = verbosity
        self.round_digits = round_digits

        # Preprocess sentences output
        self.reference_preprocess = ""
        self.prediction_preprocess = ""

        if isinstance(data, list) and len(data) > 1:
            # case with two text files => compute score
            if data[0].endswith('txt') and data[1].endswith('txt'):
                self.reference = parser_text._TextParser(data[0]).text
                self.prediction = parser_text._TextParser(data[1]).text
            # case with two strings => compute score
            else:
                self.reference = data[0]
                self.prediction = data[1]

            self.scores = Scorer(self.reference,
                                 self.prediction,
                                 truncate_score=self.truncate,
                                 show_percent=self.percent,
                                 round_digits=self.round_digits)

        # case with GT RAW TEXT file => create a HTR pipeline => compute scores
        elif isinstance(data, str) and data.endswith('txt'):
            self.reference = parser_text._TextParser(data).text
            self.file_name = os.path.basename(data)
            self.model = _load_model(model,
                                     verbosity=self.verbosity)
            self.image = _load_image(image,
                                     verbosity=self.verbosity)
            pipeline = _Prediction(self.file_name,
                                  self.image,
                                  self.model,
                                  code='txt',
                                  verbosity=self.verbosity)
            self.prediction = pipeline.get_transcription()
            self.scores = Scorer(self.reference,
                                 self.prediction,
                                 truncate_score=self.truncate,
                                 show_percent=self.percent,
                                 round_digits=self.round_digits)

        # case with GT XML PAGE => create a HTR pipeline => compute scores
        elif isinstance(data, str) and data.endswith('xml'):
            self.reference_parse = parser_page._PageParser(data)
            self.reference = "\n".join(self.reference_parse.transcriptions)
            self.file_name = os.path.basename(data)
            self.model = _load_model(model,
                                     verbosity=self.verbosity)
            self.image = _load_image(image,
                                     verbosity=self.verbosity)
            pipeline = _Prediction(self.file_name,
                                  self.image,
                                  self.model,
                                  reference=self.reference_parse,
                                  code='xml',
                                  verbosity=self.verbosity)
            self.prediction = pipeline.get_transcription()
            self.scores = Scorer(self.reference,
                                 self.prediction,
                                 truncate_score=self.truncate,
                                 show_percent=self.percent,
                                 round_digits=self.round_digits)


        else:
            raise ValueError("Something is wrong. Check your data (ground truth and/or prediction).")

        # Case with preprocessing and modulate .board dict of Scorer object
        if len(apply_transforms) > 0:
            # Create a new dict to save the different state of computations during the transformations
            new_score = dict()

            # Create a new list to save the functions of transformations
            to_compose = list()

            # A dictionary associate the user code / the preprocessing function / readable name of function
            # Codes legend for users :  D : digits / U : uppercase / L : lowercase / P : punctuation / X : diacritics
            CODES_TRANSFORMS = {
                "D": (RemoveDigits(), "non_digits"),
                "U": (ToUpperCase(), "uppercase"),
                "L": (ToLowerCase(), "lowercase"),
                "P": (RemovePunctuation(), "remove_punctuation"),
                "X": (RemoveDiacritics(), "remove_diacritics")
            }

            # Initialize the default dict that corresponding to computations on sequences before the applications of
            # transformations
            new_score["default"] = self.scores.board

            for code in CODES_TRANSFORMS.items():
                if code[0] in apply_transforms:
                    to_compose.append(code[1][0])
                    # Retrieve the scores of one transformation and add this in new dict with readable name
                    new_score[code[1][1]] = self._compute_state_transformations(code[1][0]).board
            # Retrieve the scores of all transformations in same time and add this in new dict with readable name
            scores_all_transforms, sequences_all_transforms = self._compute_all_transformations(to_compose)
            new_score["all_transforms"] = scores_all_transforms.board


            # Count total char transformed with
            # transformations in reference and prediction :
            # Add transformed sentences
            self.reference_preprocess = sequences_all_transforms[0]
            self.prediction_preprocess = sequences_all_transforms[1]


            if "D" or "P" in apply_transforms:
                # Compute the different lengths between string
                # (initial reference and transformed reference / initial reference and transformed prediction)
                # to compute the number of digits or punctuation remove
                total_char_removed_reference \
                    = (len(self.reference)
                        - len(self.reference_preprocess))
                total_char_removed_prediction \
                    = (len(self.prediction)
                        - len(self.prediction_preprocess))

                new_score["Total_char_removed_from_reference"] = total_char_removed_reference
                new_score["Total_char_removed_from_prediction"] = total_char_removed_prediction

            if "X" in apply_transforms:
                # Compute the number of diacritics removed
                total_diacritics_reference \
                    = (
                        count_diacritics(self.reference)
                        - count_diacritics(self.reference_preprocess))
                total_diacritics_prediction \
                    = (
                        count_diacritics(self.prediction)
                        - count_diacritics(self.prediction_preprocess))
                new_score["Total_diacritics_removed_from_reference"] = total_diacritics_reference
                new_score["Total_diacritics_removed_from_prediction"] = total_diacritics_prediction

            if "U" in apply_transforms:
                def count_lower(string):
                    total = sum(1 for c in string if c.islower())
                    return total
                # Compute total of lowercase char pass in uppercase in reference after transform
                total_lower_reference = count_lower(self.reference)
                total_lower_prediction = count_lower(self.prediction)
                new_score["Total_char_pass_in_uppercase_in_reference"] = total_lower_reference
                new_score["Total_char_pass_in_uppercase_in_prediction"] = total_lower_prediction

            if "L" in apply_transforms:
                def count_upper(string):
                    total = sum(1 for c in string if c.isupper())
                    return total
                # Compute total of lowercase char pass in uppercase in reference after transform
                total_upper_reference = count_upper(self.reference)
                total_upper_prediction = count_upper(self.prediction)
                new_score["Total_char_pass_in_lowercase_in_reference"] = total_upper_reference
                new_score["Total_char_pass_in_lowercase_in_prediction"] = total_upper_prediction

            if "D" or "P" or "L" or "U" or "X" in apply_transforms:
                new_score["Length_reference"] = len(self.reference)
                new_score["Length_prediction"] = len(self.prediction)
                new_score["Length_reference_transformed"] = len(self.reference_preprocess)
                new_score["Length_prediction_transformed"] = len(self.prediction_preprocess)

            # Add all scores to a final board
            self.scores.board = new_score

    def _compute_state_transformations(self, type_transform):
        """Compute scores for one transformation
        """
        transform = type_transform(
            [self.reference, self.prediction]
        )
        scores_transform = Scorer(
            transform[0],
            transform[1],
            truncate_score=self.truncate,
            show_percent=self.percent,
            round_digits=self.round_digits
        )

        return scores_transform

    def _compute_all_transformations(self, types_transforms):
        """Compute scores for all transformations
        """
        transform_for_all = _Composer(types_transforms)(
            [self.reference,
             self.prediction]
        )

        scores_transform_all = Scorer(
            transform_for_all[0],
            transform_for_all[1],
            truncate_score=self.truncate,
            show_percent=self.percent,
            round_digits=self.round_digits
        )

        return scores_transform_all, transform_for_all

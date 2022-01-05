# -*- coding: utf-8 -*-
# Authors : Alix Chagué <alix.chague@inria.fr>
#           Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""Client interface calls several sub-system of Kami-lib
"""
from typing import Union

from kami.parser import (parser_text,
                         parser_xml)
from kami.preprocessing.transformation import (RemoveDigits,
                                               ToLowerCase,
                                               ToUpperCase,
                                               RemovePunctuation,
                                               RemoveDiacritics,
                                               _Composer,
                                               count_diacritics)
from kami.transcription.prediction import _KrakenPrediction
from kami.metrics.evaluation import Scorer

import warnings
warnings.filterwarnings("ignore")

class Kami:
    """A Facade class provides a simple interface to the complex logic of one or
    several subsystems in Kami.

    This hide a complexity of Kami subsystems as :
    * Preprocessing (optionnal)
    * Prediction (if Kraken is use)
    * Metrics

    Parameters
    ----------
        :param data: Data to evaluate as two strings or two text file in list eg. ["./gt.txt", "./pred.txt"]; or a path to single ALTO or PAGE XML.
        :type data: Union[str,list]
        :param image: Path to image use to prediction if Kraken is use.
        :type image: str
        :param model: Path to transcription model use by Kraken.
        :type model: str
        :param apply_transforms: Code to apply textual variations eg. "XPD" 
        (List transformations : D : remove digits / U : uppercase / L : lowercase / P : remove punctuation / X : remove diacritics). Defaults to "".
        :type: str
        :param workers: Number of cpu workers use for inference. Defaults to 3.
        :type workers: int
        :param text_direction: principal text direction for column ordering use by Kraken : 
        "horizontal-lr", "horizontal-rl", "vertical-lr", "vertical-rl". Defaults to "horizontal-lr".
        :type: str
        :param script: script use by Kraken. Defaults to "default". 
        :type script: str
        :param verbosity: Display logs message during execution. Defaults to False. 
        :type verbosity: bool
        :param insertion_cost: predefined a weight for insertions errors. Defaults to 1.0.
        :type insertion_cost: float
        :param substitution_cost: predefined a weight for substitutions errors. Defaults to 1.0.
        :type substitution_cost: float
        :param deletion_cost: predefined a weight for deletions errors. Defaults to 1.0. 
        :type deletion_cost: float
        :param truncate: Option to truncate result. Defaults to "False". 
        :type truncate: str
        :param percent: `True` if the user want to show result in percent else `False`. Defaults to False.
        :type percent: bool
        :param round_digits: Set the number of digits after floating point in string form. Defaults to to '.01'.
        :type round_digits: str

    Attributes
    ----------
        :ivar reference: ground truth text.
        :type reference: str
        :ivar prediction: prediction by htr/ocr model.
        :type prediction: str
        :ivar model: path to the transcription model.
        :type model: str
        :ivar apply_transforms: see also `Parameters` section for more details.
        :type apply_transforms: list
        :ivar workers: see also `Parameters` section for more details.
        :type workers: int
        :ivar text_direction: see also `Parameters` section for more details.
        :type text_direction: str
        :ivar script: see also `Parameters` section for more details.
        :type script: str
        :ivar verbosity: see also `Parameters` section for more details.
        :type verbosity: bool
        :ivar insertion_weigtht: see also `Parameters` section for more details.
        :type insertion_weigtht: float
        :ivar substitution_weigtht: see also `Parameters` section for more details.
        :type substitution_weigtht: float
        :ivar deletion_weight: see also `Parameters` section for more details.
        :type deletion_weight: float
        :ivar truncate: see also `Parameters` section for more details.
        :type truncate: bool
        :ivar percent: see also `Parameters` section for more details.
        :type percent: bool
        :ivar round_digits: see also `Parameters` section for more details.
        :type round_digits: str
        :ivar reference_preprocess: ground truth with text preprocessing applied
        :type reference_preprocess: str
        :ivar prediction_preprocess: prediction with text preprocessing applied
        :type prediction_preprocess: str
        :ivar scores: KaMI Scorer object that contains all metrics.
        :type scores: KaMI Scorer object 

    """

    def __init__(self,
                 data: Union[str, list],
                 image: str = "",
                 model: str = "",
                 apply_transforms: str = "",
                 workers: int = 3,
                 text_direction : str = "horizontal-lr",
                 script= "default",
                 verbosity: bool = False,
                 insertion_cost: float = 1.0,
                 substitution_cost: float = 1.0,
                 deletion_cost: float = 1.0,
                 truncate: bool = False,
                 percent: bool = False,
                 round_digits: str = '.01'
                 ) -> None:

        # Data inputs
        self.reference = None
        self.prediction = None
        self.model = None

        # Preprocessing options inputs
        self.apply_transforms = [code for line in apply_transforms.split() for code in line]

        # Kraken options inputs
        self.workers = workers
        self.text_direction = text_direction
        self.script = script

        # Debug options
        self.verbosity = verbosity

        # Options for score weighting
        self.insertion_weigtht=insertion_cost
        self.substitution_weigtht=substitution_cost
        self.deletion_weight=deletion_cost

        # Display options for scores output
        self.truncate = truncate
        self.percent = percent
        self.round_digits = round_digits

        # Output
        self.reference_preprocess = ""
        self.prediction_preprocess = ""
        self.scores = None

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
                                 insertion_cost=self.insertion_weigtht,
                                 deletion_cost=self.deletion_weight,
                                 substitution_cost=self.substitution_weigtht,
                                 truncate_score=self.truncate,
                                 show_percent=self.percent,
                                 round_digits=self.round_digits)

        # case with GT XML PAGE / XML ALTO => create a HTR pipeline => compute scores
        elif isinstance(data, str) and data.endswith('xml'):
            self.reference_parse = parser_xml._XMLParser(xml_path=data, 
                                                         text_direction=self.text_direction, 
                                                         script=self.script)
            self.file_name = self.reference_parse.filename
            self.reference = self.reference_parse.content
            bounds = self.reference_parse.list_bounds
            pipeline = _KrakenPrediction(image_path=image,
                                         model_path=model,
                                         workers=self.workers,
                                         seg_bounds=bounds,
                                         verbosity=self.verbosity)
            self.prediction = pipeline.pred_content
            self.scores = Scorer(self.reference,
                                 self.prediction,
                                 insertion_cost=self.insertion_weigtht,
                                 deletion_cost=self.deletion_weight,
                                 substitution_cost=self.substitution_weigtht,
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

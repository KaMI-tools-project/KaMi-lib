# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
#           Alix Chagué <alix.chague@inria.fr>
# Licence : MIT
"""Common code for inputs in prediction process.
"""

import sys

from kraken import lib
from PIL import Image

from kami.kamutils._utils import _report_log

def _load_model(model: str, verbosity: bool) -> object:
    """Load an mlmodel with Kraken"""
    # STEP 1 : Loading model
    # Loading the model like kraken.lib.models.TorchSeqRecognizer object
    # --- Issue : find a way to ignore the output precautionary message
    model_loaded = lib.models.load_any(model)
    # At each new step, a validation message is displayed :
    if verbosity:
        _report_log(f"{'#' * 10} Model loaded  {'#' * 10}", "S")
        _report_log(model_loaded, "V")
    return model_loaded

def _load_image(image: str, verbosity: bool) -> list:
    """Load images with PIL and return a list of loaded images (PIL objects)"""
    # At each new step we create an empty list to receive the new objects, such as :
    try:
        img_pil = Image.open(image)
        if verbosity:
            _report_log(f"{'#' * 10} Image loaded  {'#' * 10}", "S")
    except Exception as exception:
        _report_log(f"type : {exception}")
        _report_log(f"Error : unable to load images - {image}", "E")
        sys.exit('program exit')

    if verbosity:
        _report_log(img_pil, "V")

    return img_pil

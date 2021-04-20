# -*- coding: utf-8 -*-
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
#           Alix Chagué <alix.chague@inria.fr>
# Licence : MIT
"""Common code for prediction process.
"""

import sys

from kami.kamutils._utils import _report_log
from kraken import rpred, pageseg, binarization

def _binarize_image(image_loaded: object, verbosity: bool) -> object:
    """Binarize a series of images"""
    try:
        # create binarized image
        im_bin = binarization.nlbin(image_loaded)
        if verbosity:
            _report_log(f"{'#' * 10} Binarization procceded  {'#' * 10}", "S")
    except Exception as exception:
        _report_log(f"type : {exception}")
        _report_log(f"Error : unable to binarize - {image_loaded}", "E")
        sys.exit('program exit')

    if verbosity:
        _report_log(im_bin, "V")

    return im_bin


def _segment_image(image_loaded: object, verbosity: bool) -> list:
    """Perform segmentation on a image"""
    try:
        segments_image = pageseg.segment(image_loaded, text_direction='horizontal-lr')
        if verbosity:
            _report_log(f"{'#' * 10} Segmentation procceded  {'#' * 10}", "S")
    except Exception as exception:
        _report_log(f"type : {exception}")
        _report_log(f"Error : unable to segment - {image_loaded}", "E")
        sys.exit('program exit')

    if verbosity:
        _report_log(segments_image, "V")

    return segments_image


def _predict_transcription(image: object, segments, model_loaded: object, verbosity: bool) -> list:
    """Perform transcription on a series of images given a series of segments"""

    # created the text prediction (kraken.rpred.mm_rpred object)
    output_rpred = rpred.rpred(network=model_loaded,
                               im=image,
                               bounds=segments,
                               pad=16,
                               bidi_reordering=True)
    if verbosity:
        _report_log(f"{'#' * 10} Text recognition procceded  {'#' * 10}", "S")

    if verbosity:
        _report_log(output_rpred, "V")
    return output_rpred



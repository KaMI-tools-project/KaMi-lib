from kraken import rpred, pageseg, binarization
import sys
from kami.kamutils._utils import _report_log

def _binarize_image(image_loaded: object, verbosity: bool) -> object:
    """Binarize a series of images"""
    try:
        # create binarized image
        im_bin = binarization.nlbin(image_loaded)
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
        _report_log(f"{'#' * 10} Segmentation procceded  {'#' * 10}", "S")
    except Exception as exception:
        _report_log(f"type : {exception}")
        _report_log(f"Error : unable to segment - {image_loaded}", "E")
        sys.exit('program exit')

    if verbosity:
        _report_log(segments_image, "V")

    return segments_image


def _predict_transcription(pair_image_segments: tuple, model_loaded: object, verbosity: bool) -> list:
    """Perform transcription on a series of images given a series of segments"""
    binarized_element = pair_image_segments[0]
    segment_element = pair_image_segments[1]
    # created the text prediction (kraken.rpred.mm_rpred object)
    output_rpred = rpred.rpred(model_loaded,
                               binarized_element,
                               segment_element,
                               bidi_reordering=True)

    _report_log(f"{'#' * 10} Text recognition procceded  {'#' * 10}", "S")

    if verbosity:
        _report_log(output_rpred, "V")
    return output_rpred



# -*- coding: utf-8 -*-
# Authors : Alix Chagué <alix.chague@inria.fr>
#           Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""
    The ``Text recognizer`` module based on Kraken OCR/HTR engine
    =============================================================

    - Doc Kraken : http://kraken.re/master/api.html#api-quickstart 
    - Work only for ALTO and PAGE XML segmentation
    - Future : make prediction with text (no script for re-order lines
      in output for now) and default segmentation model (blla)

"""

from multiprocessing import Pool
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from PIL import Image

from kraken.lib import models
from kraken import rpred

from kami.kamutils._utils import (_report_log)


class _KrakenPrediction:
    """A OCR/HTR engine based on Kraken to create predictions from text recognizer model.


    Attributes
    ----------
        :ivar im: Image open as PIL object.
        :type im: PIL image object
        :ivar model: Load valid ocropus model and instanciate from the RNN configuration.
        :type model: A kraken.lib.models.TorchSeqRecognizer object
        :ivar bounds: Boundaries extract from ALTO or PAGE file.
        :type bounds: list
        :ivar pred_sentences: List of sentences predicted.
        :type pred_sentences: list
        :ivar pred_content: All prediction ; one sentence per line.
        :type pred_content: str
        :ivar verbosity: Details during prediction process. Defaults to False.
        :type verbosity: bool
        :ivar workers: Number of cpu workers use for inference. Defaults to 3.
        :type workers: int
    """
    def __init__(self, 
                    image_path : str, 
                    model_path : str, 
                    seg_bounds : list, 
                    verbosity: bool = False, 
                    workers: int = 3) -> None:
        self.im = Image.open(image_path)
        self.model = models.load_any(model_path)
        self.bounds = seg_bounds
        self.pred_sentences = []
        try:
            if verbosity:
                _report_log("Start with Kraken prediction...", type_log="I")
            # Create a pool process executor for turbo-charge (heavy cpu task) Kraken transcription model inference function (repred.rpred)
            with Pool(processes=workers) as p:
                self.pred_sentences = p.map(self._transcribe, self.bounds)
            # if pool remove : self.pred_sentences = [self._transcribe(bound) for bound in self.bounds]
            if verbosity:
                _report_log("Kraken prediction finished with success.", type_log="I")
        except Exception as e:
            _report_log(f"[ERROR] Prediction with Kraken failed : {e}")
        
        # Retrieve all text with one sentence per line
        self.pred_content = "\n".join(self.pred_sentences)

    def _transcribe(self, bound):
        """Kraken method for recognition.

        Args:
            bound ([dict]): segment extract from ALTO/PAGE XML

        Returns:
            [str]: prediction.
        """
        return next(rpred.rpred(
            network=self.model, 
            im=self.im, 
            bounds=bound, 
            pad=16,
            bidi_reordering=True)).prediction

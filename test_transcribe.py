import sys

from os import cpu_count
from os.path import basename, isfile

import time
from kraken.lib import models, xml, exceptions
from kraken import rpred, blla
from kraken.kraken import SEGMENTATION_DEFAULT_MODEL 

from kraken.lib import vgsl
from PIL import Image
import numpy as np
from multiprocessing import Pool

np.seterr(divide='ignore', invalid='ignore')

import warnings
warnings.filterwarnings("ignore")


if __name__ == "__main__":
    import time
    from kami.parser.parser_xml import _XMLParser
    from kami.transcription.prediction import _KrakenPrediction
    curent = current = time.time()
    image = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0.png"
    alto = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_alto.xml"
    page = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_page.xml"
    model = "./datatest/lectaurep_set/models/mixte_mrs_15.mlmodel"
    parser = _XMLParser(xml_path=page, text_direction="horizontal-lr", script="default")
    bounds = parser.list_bounds
    predictor = _KrakenPrediction(image_path=image,model_path=model,seg_bounds=bounds)
    print(f"\n * TOTAL Prediction : {time.time() - current}")




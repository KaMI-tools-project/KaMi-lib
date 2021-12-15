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


class _XMLParser:
    """A XML Parser for KaMI (ALTO/PAGE).

    """
    def __init__(self, xml_path : str) -> None:
        self.file_path = xml_path
        self.filename = basename(self.file_path) if isfile(self.file_path) else ""
        self.base_bounds = ""
        self.TEXT_DIRECTION = 'horizontal-lr'
        self.SCRIPT = 'default'
        try:
            self.base_bounds = xml.parse_xml(self.file_path)
        except exceptions.KrakenInputException as eK:
            print(f"Something went wrong while parsing XML content (XMLParser expects PAGE or ALTO XML content or a .xml file) : {eK}")

        self.list_bounds = self._get_list_of_boundaries()
        self.sentences = self._get_content_textlines()
        self.content = "\n".join(self._get_content_textlines())
    
    def _get_content_textlines(self):
        return [line['text'] for line in self.base_bounds['lines']]
    
    def _get_list_of_boundaries(self):
        return [{
                'lines': [
                {
                    'baseline': bound['baseline'],
                    'boundary': bound['boundary'],
                    'text_direction': self.TEXT_DIRECTION,
                    'script': self.SCRIPT}
                    ],  
                'type': 'baselines',
            } for bound in self.base_bounds['lines']] 



        
class _KrakenPrediction:
    """A OCR/HTR engine based on Kraken to create predictions from text recognizer model.

    """
    def __init__(self, image_path : str, model_path : str) -> None:
        self.im = Image.open(image_path)
        self.model = models.load_any(model_path)
        self.model_seg = vgsl.TorchVGSLModel.load_model(SEGMENTATION_DEFAULT_MODEL)
        self.baseline_seg = blla.segment(self.im, model=self.model_seg)
        self.boundaries_for_txt = self._get_list_of_boundaries_from_seg_model()
        self.sentences = [sentence.prediction for bound in self.boundaries_for_txt for sentence in self._transcribe(bound)]
        #self.content = "\n".join([sentence for sentence in self.sentences])
        
    def _get_list_of_boundaries_from_seg_model(self):
        return [{
                'lines': [
                {
                    'baseline': bound['baseline'],
                    'boundary': bound['boundary'],
                    'text_direction': 'horizontal-lr',
                    'script': 'default'}
                    ],  
                'type': 'baselines',
            } for bound in self.baseline_seg['lines']] 
    
    def _transcribe(self, bound):
        return rpred.rpred(
            network=self.model, 
            im=self.im, 
            bounds=bound, 
            pad=16,
            bidi_reordering='L')




    """
        with Pool(3) as p:
            self.pred_sentences = p.map(self._transcribe, self.bounds)
        
        self.pred_content = "\n".join(self.pred_sentences)

    def _transcribe(self, bound):
        return rpred.rpred(
            network=self.model, 
            im=self.im, 
            bounds=bound, 
            pad=16,
            bidi_reordering=True).prediction
    """

 




if __name__ == "__main__":
    page="./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_page.xml"
    alto="./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_alto.xml"
    text="./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0_gt.txt"
    image = "./datatest/lectaurep_set/image_gt_page1/FRAN_0187_16402_L-0.png"
    model = "./datatest/lectaurep_set/models/mixte_mrs_15.mlmodel"
    from kami.metrics.evaluation_ import Scorer
    print(Scorer(reference="bonjour", prediction="bye").board)




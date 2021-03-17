from collections import namedtuple
from kami.preprocessing.transformation import Composer

class Core():
    def __init__(self, image, ground_truth_file, segmentation_model, transcription_model):
        self.image = image
        self.gt = ground_truth_file
        self.segm = segmentation_model
        self.trscm = transcription_model
        Group = namedtuple('Group', ['image', 'gt', 'segm', 'trscm'])
        self.group = Group(image=self.image,
                           gt=self.gt,
                           segm=self.segm,
                           trscm=self.trscm)


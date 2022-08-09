"""Python's bridges for C shared metrics functions
"""
import os
from ctypes import *

PATH = os.path.dirname(os.path.abspath(__file__))
METRICS_FUNCTIONS = CDLL(os.path.join(PATH, "metrics_lib.so"))


# HTR/OCR Metrics


WER = METRICS_FUNCTIONS.WordErrorRate
WER.argtypes = [c_int, c_int]
WER.restype = c_float

CER = METRICS_FUNCTIONS.CharacterErrorRate
CER.argtypes = [c_int, c_int]
CER.restype = c_float

WACC = METRICS_FUNCTIONS.WordAccuracy
WACC.argtypes = [c_float]
WACC.restype = c_float

WERHUNT = METRICS_FUNCTIONS.WordErrorRateHuntStyle
WERHUNT.argtypes = [c_float, c_float]
WERHUNT.restype = c_float


# ASR Metrics

CIP = METRICS_FUNCTIONS.CharacterInformationPreserve
CIP.argtypes = [c_int, c_int, c_int]
CIP.restype = c_float

CIL = METRICS_FUNCTIONS.CharacterInformationLost
CIL.argtypes = [c_float]
CIL.restype = c_float


MER = METRICS_FUNCTIONS.MatchErrorRate
MER.argtypes = [c_int, c_int]
MER.restype = c_float

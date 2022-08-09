"""Python's bridges for C shared metrics functions
"""
import ctypes

METRICS_FUNCTIONS = ctypes.CDLL("kami/metrics/metrics_lib.so")


# HTR/OCR Metrics

WER = METRICS_FUNCTIONS.WordErrorRate
WER.argtypes = [ctypes.c_int, ctypes.c_int]
WER.restype = ctypes.c_float

CER = METRICS_FUNCTIONS.CharacterErrorRate
CER.argtypes = [ctypes.c_int, ctypes.c_int]
CER.restype = ctypes.c_float

WACC = METRICS_FUNCTIONS.WordAccuracy
WACC.argtypes = [ctypes.c_float]
WACC.restype = ctypes.c_float

WERHUNT = METRICS_FUNCTIONS.WordErrorRateHuntStyle
WERHUNT.argtypes = [ctypes.c_float, ctypes.c_float]
WERHUNT.restype = ctypes.c_float


# ASR Metrics

CIP = METRICS_FUNCTIONS.CharacterInformationPreserve
CIP.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
CIP.restype = ctypes.c_float

CIL = METRICS_FUNCTIONS.CharacterInformationLost
CIL.argtypes = [ctypes.c_float]
CIL.restype = ctypes.c_float


MER = METRICS_FUNCTIONS.MatchErrorRate
MER.argtypes = [ctypes.c_int, ctypes.c_int]
MER.restype = ctypes.c_float
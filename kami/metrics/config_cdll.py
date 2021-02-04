"""config file to link CDLLs (C Dynamic Link Libraries - Shared Library)
To Python Kami lib

"""
# Authors : Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT

from ctypes import *
import os.path

local = os.path.abspath(os.path.dirname(__file__))

# create a file path to .so compile C file
# so_file_distance = 'so_extensions/_distance.so'
# so_file_score_text_recognition = 'so_extensions/_score_text_recognition.so'

# load cdll
_distance_dll = cdll.LoadLibrary(os.path.join(local, 'so_extensions/', "_distance.so"))
_score_text_recognition_dll = cdll.LoadLibrary(os.path.join(local, 'so_extensions/', "_score_text_recognition.so"))


# configure arg types (input) for each functions
# (See ctypes doc here : https://docs.python.org/3/library/ctypes.html)
_distance_dll.levenshtein.argtypes = [c_wchar_p, c_wchar_p]
_distance_dll.hamming.argtypes = [c_wchar_p, c_wchar_p]

_score_text_recognition_dll.wer.argtypes = [c_int, c_int]
_score_text_recognition_dll.cer.argtypes = [c_int, c_int]
_score_text_recognition_dll.wacc.argtypes = [c_int, c_int]

# configure arg types (output) for each functions
_score_text_recognition_dll.wer.restype = c_float
_score_text_recognition_dll.cer.restype = c_float
_score_text_recognition_dll.wacc.restype = c_float

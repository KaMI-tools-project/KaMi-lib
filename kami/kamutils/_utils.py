# -*- coding: utf-8 -*-

"""Common code for classes
"""
# Authors : Alix Chagué <alix.chague@inria.fr>
#           Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT

from functools import wraps
from termcolor import cprint
import time

# TODO(Luca) : Pylint
def _report_log(message, type_log="I") -> None:
    """Print a log report

    letter code to specify type of report
    ['I' > Info|'W' > Warning|'E' > Error|'S' > Success|'V' > Verbose]

    Args:
        message (str) : message to display
        type_log (str, optional) : type of message. Defaults to "I" (Info)

    Return:
        str : log in defined color

    """
    if type_log == "I":  # Info
        return print(f"[INFO    ℹ] {message}")
    elif type_log == "W":  # Warning
        return cprint(f"[WARNING ▲] {message}", "yellow")
    elif type_log == "E":  # Error
        return cprint(f"[ERROR   ⤬]  {message}", "red")
    elif type_log == "S": # Success
        return cprint(f"[SUCCESS ✓]  {message}", "green")
    elif type_log == "V": # Verbose
        return cprint(f"[DETAILS ℹ]  {message}", "blue")
    else:
        # unknown color parameter, treated as "normal" text
        return print(message)

# TODO(Luca) : documentation
def _timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        _report_log(f'Total execution : {end-start} secs')
        return result
    return wrapper


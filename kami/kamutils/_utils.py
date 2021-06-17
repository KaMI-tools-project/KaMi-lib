# -*- coding: utf-8 -*-
# Authors : Alix Chagué <alix.chague@inria.fr>
#           Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""Common code for Kami functions or classes.
"""

import time
from typing import Callable

from functools import wraps
import termcolor


__all__ = [
    "_report_log",
    "_timing"
]


def _report_log(message: str, type_log: str = "I") -> None:
    """Returns report log

    letter code to specify type of report

    'I' > Info | 'W' > Warning | 'E' > Error | 'S' > Success | 'V' > Verbose

    :Example:

    >>> _report_log("It seems your sentence is empty", "E")
    [ERROR   ⤬]  It seems your sentence is empty

    :param message: message to display in the log
    :type message: str
    :param type_log: type of message. Defaults to "I" (Info).
    :type type_log: str
    :return: None (print a log in defined color)
    :rtype: None
    """
    if type_log == "I":  # Info
        return print(f"[INFO    ℹ] {message}")
    if type_log == "W":  # Warning
        return termcolor.cprint(f"[WARNING ▲] {message}", "yellow")
    if type_log == "E":  # Error
        return termcolor.cprint(f"[ERROR   ⤬]  {message}", "red")
    if type_log == "S":  # Success
        return termcolor.cprint(f"[SUCCESS ✓]  {message}", "green")
    if type_log == "V":  # Verbose
        return termcolor.cprint(f"[DETAILS ℹ]  {message}", "blue")
    else:
        return print(message)


def _timing(function: Callable) -> Callable:
    """A simple decorator to compute execution time of any function
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        _report_log(f'Total execution : {end-start} secs')
        return result
    return wrapper

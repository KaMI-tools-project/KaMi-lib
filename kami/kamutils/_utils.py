"""Common code for classes
"""
# Authors : Alix Chagué <alix.chague@inria.fr>
# Licence : MIT

from termcolor import cprint

def report_log(message, type_log="I") -> None:
    """Print a log report

    letter code to specify type of report
    ['I' > Info|'W' > Warning|'E' > Error|'S' > Success|'V' > Verbose]

    Args:
        message (str) : message to display
        type_log (str, optional) : type of message. Defaults to "I" (Info)

    Return:
        None

    """
    if type_log == "I":  # Info
        print(message)
    elif type_log == "W":  # Warning
        cprint(message, "yellow")
    elif type_log == "E":  # Error
        cprint(message, "red")
    elif type_log == "S": # Success
        cprint(message, "green")
    elif type_log == "V":
        cprint(message, "blue")  # Verbose
    else:
        # unknown color parameter, treated as "normal" text
        print(message)




# -*- coding: utf-8 -*-
# Authors : Alix Chagué <alix.chague@inria.fr>
# Licence : MIT
"""
    The ``Parser Text`` module parse Text
    =====================================

    ...

"""

import os

from kami.kamutils._utils import (_report_log)


class _TextParser:
    """A very simple Text Parser for KaMI.

    Attributes:
        file_name   Source file name if there is one
        text        Source text
    """
    def _get_text(self) -> None:
        """Open a TXT file and load its content"""
        if self.file_name:
            with open(self.file_name, "r", encoding="utf8") as fh:
                content = fh.read()
                content = ''.join([line + "\n" for line in content.split('\n') if line.strip() != ''])
        self.text = content

    def __init__(self, source):
        """Initialize a TextParser from a path to text file or from a string.

        :param source: path to source file or plain text
        :type source: str
        """
        self.file_name = None
        self.text = None
        if isinstance(source, str) and os.path.isfile(source):
            self.file_name = source
            self._get_text()
        elif isinstance(source, str):
            if os.sep in source:
                _report_log("Provided input is considered as plain text. If you intended it to be a handled "+
                            "as a path, you may need to make sure it is correct.", "W")
            self.text = source
        else:
            _report_log("TextParser can't proceed. Verify your input: it must be a string. "+
                        "Created an empty object.", "W")
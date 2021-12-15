# -*- coding: utf-8 -*-
# Authors : Alix Chagué <alix.chague@inria.fr>
#           Lucas Terriel <lucas.terriel@inria.fr>
# Licence : MIT
"""
    The ``XML Parser`` module parse XML PAGE / XML ALTO
    ===================================================

"""

from os.path import basename, isfile
from kraken.lib import xml, exceptions
from kraken.lib.xml import logger
from kami.kamutils._utils import (_report_log)

logger.disabled = True

__all__ = [
    "_XMLParser"
]

class _XMLParser:
    """A XML Parser for KaMI (ALTO/PAGE).

    Parameters
    ----------
        :param xml_path:  path to source file or plain text
        :type xml_path: str
        :param text_direction:  principal text direction for column ordering : "horizontal-lr", "horizontal-rl", "vertical-lr", "vertical-rl".
        :type text_direction: str
        :param script:  type of script.
        :type script: str

    Attributes
    ----------
        :ivar file_path: path to source XML file.
        :param file_path: str
        :ivar filename: source XML file name.
        :param text: str
        :ivar base_bounds: segmentation information extract from XML.
        :param base_bounds: dict
        :ivar TEXT_DIRECTION: principal text direction for column ordering : "horizontal-lr", "horizontal-rl", "vertical-lr", "vertical-rl".
        :param TEXT_DIRECTION: str
        :ivar script: type of script.
        :param script: str
        :ivar list_bounds: reformat segmentation information in `base_bounds`.
        :param list_bounds: list
        :ivar sentences: ground truth sentences in source XML.
        :param sentences: list
        :ivar content: ground truth text in sourece XML.
        :param content: str
    """

    def __init__(self, xml_path : str, text_direction : str, script : str) -> None:
        self.file_path = xml_path
        self.filename = basename(self.file_path) if isfile(self.file_path) else ""
        self.base_bounds = ""
        self.TEXT_DIRECTION = text_direction
        self.SCRIPT = script
        try:
            self.base_bounds = xml.parse_xml(self.file_path)
        except exceptions.KrakenInputException as eK:
            _report_log(f"Something went wrong while parsing XML content (XMLParser expects PAGE or ALTO XML content or a .xml file) : {eK}", "W")

        self.list_bounds = self._get_list_of_boundaries()
        self.sentences = self._get_content_textlines()
        self.content = "\n".join(self._get_content_textlines())
    
    def _get_content_textlines(self):
        """Extract sentences from bounds"""
        return [line['text'] for line in self.base_bounds['lines']]
    
    def _get_list_of_boundaries(self):
        """Reformat boundaries in list of dicts"""
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

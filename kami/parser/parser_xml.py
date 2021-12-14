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



class _XMLParser:
    """A XML Parser for KaMI (ALTO/PAGE).

    """

    def __init__(self, xml_path : str, text_direction='horizontal-lr', script='default') -> None:
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
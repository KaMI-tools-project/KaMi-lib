# -*- coding: utf-8 -*-
# Authors : Alix Chagué <alix.chague@inria.fr>
# Licence : MIT
"""
    The ``Parser Page`` module parse XML PAGE
    =========================================

    inspiration from:
    https://gitlab.inria.fr/scripta/escriptorium/-/blob/master/app/apps/imports/parsers.py
    ...

"""

import os

from bs4 import BeautifulSoup

from kami.kamutils._utils import (_report_log)


def _get_page_content(page):
    """Process PageParser input variable to obtain parsed PAGE XML tree

    Example:
    >>> _get_page_content("incorrect/path/to/unexisting/file.txt")
    None

    >>> type(_get_page_content("path/to/existing/file.xml"))
    <class 'bs4.BeautifulSoup'>
    >>> type(_get_page_content(BeautifulSoup('<example/>', 'xml')))
    <class 'bs4.BeautifulSoup'>

    :param page: either a path (str) either a parsed XML Tree
    :type page: str | BeautifulSoup
    :return: Parsed XML tree
    :rtype: BeautifulSoup
    """
    page_content = None
    if isinstance(page, type(BeautifulSoup())):
        page_content = page
    elif isinstance(page, str):
        if page.endswith('.xml'):
            _report_log("Pageparser expects PAGE XML content or a .xml file.", "W")
        elif os.path.isfile(page):
            try:
                with open(page, 'r') as fh:
                    file_content = fh.read()
            except OSError as e:
                _report_log("Something went wrong while parsing source file:", "W")
                print(e)
            else:
                try:
                    page_content = BeautifulSoup(file_content, 'xml')
                except TypeError as e:
                    _report_log("Something went wrong while parsing XML content:", "W")
                    print(e)
    return page_content


def _clean_coords(baseline_tag) -> list:
    """Clean coordinates following Kraken's expectation

    Example:

    >>> _clean_coords(BeautifulSoup('<Baseline points="645,2398 1318,2387"/>'))
    [[645.0, 2398.0], [1318.0, 2387.0]]

    :param baseline_tag: <Coords> node
    :type baseline_tag: BeautifulSoup
    :return: list of points
    :rtype: list
    """
    return [list(map(lambda x: 0 if float(x) < 0 else float(x), pt.split(",")))
            for pt in baseline_tag.get("points").split(" ")]


class PageParser:
    """A PAGE XML Parser for KaMI.

    Attibutes:
        page_content    XML Tree parsed with BeautifulSoup
        _pcgts          True if XML Tree has a PcGts node
        bounds          List of bounds for Kraken, 1 bound per segment
        transcriptions  List of transcriptions, 1 string per segment
        pairs           List of pairs of bounds and transcriptions, 1 dict per pair
        source_image    Source image referred to in //Page/@imageFilename

    ---

    PageParser.bounds[1] matches PageParser.transcriptions[1] and PageParser.pairs[1]
    """
    def _get_lines(self) -> list:
        """Get TextLine elements in PAGE XML Tree"""
        return [line for line in self.page_content.find_all("TextLine")]

    def _get_bounds_and_transcriptions(self) -> None:
        """Create bounds objects (for transcription) from baseline and boxes in XML tree"""
        self.bounds = []
        self.transcriptions = []
        self.pairs = []

        for line in self._get_lines():
            try:
                baseline = _clean_coords(line.find("Baseline"))
            except AttributeError:
                # if the baseline is not good:
                baseline = None
            polygon = line.find("Coords")
            if polygon is not None:
                mask = _clean_coords(polygon)
            else:
                mask = []
            self.bounds.append({
                'lines': [{'baseline': baseline,
                           'boundary': mask,
                           'text_direction': 'horizontal-lr',  # TODO text direction can be different
                           'script': 'default'}],  # self.document.main_script.name
                'type': 'baselines',
            })

            text_equiv = line.find('Unicode')
            if text_equiv:
                self.transcriptions.append(text_equiv.text)
            else:
                self.transcriptions.append('\n')

            self.pairs.append({'bounds': self.bounds[-1], 'transcription': self.transcriptions[-1]})

    def __init__(self, page):
        """Initialize a PageParser from a path to PAGE XML file or from the content of a PAGE XML file
        parsed with BeautifulSoup.

        :param page: either a path (str) either a parsed XML Tree
        :type page: str or BeautifulSoup
        """
        self.page_content = _get_page_content(page)
        self._pcgts = None
        self.bounds = None
        self.transcriptions = None
        self.paris = None
        self.source_image = None

        # proceed only if something was parsed
        if not self.page_content:
            _report_log("PageParser can't proceed: verify your input. Created an empty object.", "W")
        else:
            if self.page_content.find('PcGts'):
                self._pcgts = True
                creator = self.page_content.find('Creator')
                if not creator and not creator.text.lower() == 'escriptorium':
                    _report_log("It seems that the file was not created with" +
                                "eScriptorium, which may cause unexpected errors.", "W")
                image = self.page_content.find('Page')
                if image and 'imageFilename' in image.attrs:
                    self.source_image = image.attrs['imageFilename']
                else:
                    _report_log("There is no <Page> node with a @imageFilename" +
                                "attribute in this XML file. It can be an issue.", "W")
                try:
                    self._get_bounds_and_transcriptions()
                except Exception as e:
                    _report_log("Something wen wrong while parsing TextLines", "E")
                    print(e)

            else:
                _report_log("Not a PAGE XML file", "E")


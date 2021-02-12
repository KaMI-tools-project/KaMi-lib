"""Collection of file parsers
"""
# Authors : Alix Chagué <alix.chague@inria.fr>
# Licence : MIT


from bs4 import BeautifulSoup

from ..kamutils._utils import report_log


XML_STANDARD = ["PcGts", "alto"] #, "TEI"]


# inspiration from
# https://gitlab.inria.fr/scripta/escriptorium/-/blob/master/app/apps/imports/parsers.py
class PagexmlParser():
    """

    """

    def get_lines(self) -> list:
        """Get TextLine elements in XML Tree"""
        # works wether with ALTO or PAGE
        return [line for line in self.content.find_all("TextLine")]

    def clean_coords(self, coordTag) -> list:
        """Clean coordinates"""
        return [
            list(map(lambda x: 0 if float(x) < 0 else float(x), pt.split(",")))
            for pt in coordTag.get("points").split(" ")
        ]

    def get_bounds(self) -> list:
        """Create bounds objects (for transcription) from baseline and boxes in XML tree"""
        bounds = []
        lines = self.get_lines()
        if self.standard == "PcGts":
            for line in lines:
                try:
                    baseline = line.find("Baseline")
                    baseline = self.clean_coords(baseline)
                except AttributeError:
                    #  to check if the baseline is good
                    baseline = None
                polygon = line.find("Coords")
                if polygon is not None:
                    mask = self.clean_coords(polygon)
                else:
                    mask = []
                bounds.append({
                    'lines': [{'baseline': baseline,
                               'boundary': mask,
                               'text_direction': 'horizontal-lr',  # text direction can be different
                               'script': 'default'}],  # self.document.main_script.name
                    'type': 'baselines',
                    # 'selfcript_detection': True
                })

        elif self.standard == "alto":  # TODO test and debug this scenario
            for line in lines:
                polygon = line.find("Shape/Polygon")
                if polygon is not None:
                    try:
                        coords = tuple(map(float, polygon.get("POINTS").split(" ")))
                        mask = tuple(zip(coords[::2], coords[1::2]))
                        baseline = line.get("BASELINE") # maybe more line.find(True, "BASELINE")["attrs"]["BASELINE"]
                        bounds.append({
                            'lines': [{'baseline': baseline,  # not sure this will work...
                                       'boundary': mask,
                                       'text_direction': 'horizontal-lr',  # text direction can be different
                                       'script': 'default'}],  # self.document.main_script.name
                            'type': 'baselines',
                            # 'selfcript_detection': True
                        })
                    except ValueError:
                        report_log(f"Invalid polygon in {self.filename}", "W")
                else:
                    box = [
                        int(line.get("HPOS")),
                        int(line.get("VPOS")),
                        int(line.get("HPOS")) + int(line.get("WIDTH")),
                        int(line.get("VPOS")) + int(line.get("HEIGHT")),
                    ]
                    # https://gitlab.inria.fr/scripta/escriptorium/-/blob/master/app/apps/core/models.py#L693
                    bounds.append({
                        'boxes': [box],
                        'text_direction': 'horizontal-lr',  # text direction can be different
                        'type': 'baselines',
                        # 'script_detection': True
                    })
                # que fait-on de mask et de box ?
            pass
        return bounds

    def get_xml_standard(self) -> str:
        """Determine which standard (ALTO or PAGE) is used in XML tree"""
        for standard in XML_STANDARD:
            found_standard = self.content.find_all(standard)
            if len(found_standard) == 1:  # TODO improve
                # we should control the schema too
                return standard
            else:
                report_log(f"Counted '{standard}' {len(found_standard)} time(s) ", "V")
        report_log("Unsupported XML format", "E")
        return False

    def parse_content(self) -> object:
        """Parse an XML tree"""
        with open(self.filename, "r") as fh:
            content = fh.read()
        return BeautifulSoup(content, "xml")

    def extract_plain_text(self) -> str:
        """Extract plain text in an XML tree"""
        plain_text = ""
        if self.standard == "PcGts":
            for line in self.content.find_all("Unicode"):
                plain_text += line.string + "\n"
        elif self.standard == "alto":
            for line in self.content.find_all("String"):
                if "CONTENT" in line.attrs:
                    plain_text += line.attrs["CONTENT"] + "\n"
        return plain_text

    def __init__(self, pagexml_file):
        self.filename = pagexml_file
        self.content = self.parse_content()
        self.standard = self.get_xml_standard()
        self.plain_text = self.extract_plain_text()
        self.bounds = self.get_bounds()  # todo



class TxtParser():
    """

    """
    def extract_plain_text(self) -> str:
        """Open a TXT file and load its content"""
        with open(self.filename, "r", encoding="utf8") as fh:
            content = fh.read()
        return content

    def __init__(self, txt_file):
        self.filename = txt_file
        self.plain_text = self.extract_plain_text()
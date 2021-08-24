# -*- coding : utf-8 -*-

from os import path
import io
import setuptools

import kami

here = path.abspath(path.dirname(__file__))

try:
    with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = u"Python package focused on HTR / OCR models evaluation and based on the Kraken transcription system."


with open("requirements.txt", encoding="utf-8") as f:
    install_requires = f.read().splitlines()


CLASSIFIERS = [
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]


setuptools.setup(
    name=kami.__title__,
    version=kami.__version__,
    author="Lucas Terriel, Alix Chagué",
    author_email="lucas.terriel@inria.fr, alix.chague@inria.fr",
    license=kami.__licence__,
    description="Python package focused on HTR / OCR models evaluation and based on the Kraken transcription system.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://gitlab.inria.fr/dh-projects/kami/kami-lib",
    project_urls={
        "Bug Tracker": "https://gitlab.inria.fr/dh-projects/kami/kami-lib/-/issues/new?issuable_template=bug_report",
    },
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
    keywords=["HTR", "OCR", "Evaluation framework", "metrics", "handwritten text recognition", "optical character recognition"],
)
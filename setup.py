# -*- coding : utf-8 -*-

import setuptools
import unittest

import kami

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except:
    long_description = u"Python package focused on HTR / OCR models evaluation and based on the Kraken transcription system."


with open("requirements.txt", encoding="utf-8") as f:
    install_requires = f.read().splitlines()


def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


CLASSIFIERS = [
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]


setuptools.setup(
    name=kami.__title__,
    version=kami.__version__,
    license=kami.__licence__,
    author="Lucas Terriel, Alix Chagué",
    author_email="lucas.terriel@inria.fr, alix.chague@inria.fr",
    description="Python package focused on HTR / OCR models evaluation and based on the Kraken transcription system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.inria.fr/dh-projects/kami/kami-lib",
    project_urls={
        "Bug Tracker": "https://gitlab.inria.fr/dh-projects/kami/kami-lib/-/issues",
    },
    classifiers=CLASSIFIERS,
    keywords=["HTR", "OCR", "Evaluation framework", "metrics", "handwritten text recognition", "optical character recognition"],
    package_dir={"": "kami"},
    packages=setuptools.find_packages(where="kami"),
    python_requires=">=3.7",
    test_suite='setup.test_suite',
    zip_safe=False,
    install_requires=install_requires
)
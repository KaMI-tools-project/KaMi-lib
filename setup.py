# -*- coding : utf-8 -*-

from os import path
import io
import setuptools
import subprocess

import kami

here = path.abspath(path.dirname(__file__))

kamilib_version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

"""
try:
    with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = u"HTR / OCR models evaluation agnostic Python package, originally based on the Kraken transcription system."
"""

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as f:
    install_requires = f.read().splitlines()


CLASSIFIERS = [
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]


setuptools.setup(
    name=kami.__title__,
    version=kamilib_version,
    author="Lucas Terriel, Alix Chagué",
    author_email="lucas.terriel@inria.fr, alix.chague@inria.fr",
    license=kami.__licence__,
    description=kami.__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KaMI-tools-project/KaMi-lib",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires='>=3.7',
    classifiers=CLASSIFIERS,
    keywords=["HTR", "OCR", "Evaluation framework", "metrics", "handwritten text recognition", "optical character recognition"],
)

# packages=setuptools.find_packages(exclude=('tests', 'env-kamilib')),
"""
This is the project specification for setuptools
"""

import os
from setuptools import setup


def read(fname):
    """
    Read a file relative the current directory and return its contents
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


AUTHORS = ["James Hetherington",
           "Raquel Alegre",
           "Roma Klapaukh",
           "Mike Jackson",
           "Rosa Filgueira"]

EMAILS = ["j.hetherington@ucl.ac.uk",
          "r.alegre@ucl.ac.uk",
          "r.klapaukh@ucl.ac.uk>",
          "michaelj@epcc.ed.ac.uk",
          "rosa.filgueira@ed.ac.uk"]

setup(
    name="iNewsRods",
    version="0.0.1",
    authors=", ".join(AUTHORS),
    author_email=", ".join(EMAILS),
    description=(
        "Harness for Apache Spark analysis of newspapers corpus"),
    license="MIT",
    keywords="digital humanities research newspapers",
    url="https://github.com/alan-turing-institute/i_newspaper_rods",
    packages=['newsrods'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Research :: Humanities",
        "License :: OSI Approved :: MIT License",
    ]
)

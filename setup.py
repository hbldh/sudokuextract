# -*- coding: utf-8 -*-
"""
:mod:`setup.py`
===============

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>
Created on 2015-11-05

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
from setuptools import setup, find_packages, Extension

import numpy
import sudokuextract

basedir = os.path.dirname(os.path.abspath(__file__))

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='sudokuextract',
    version=sudokuextract.__version__,
    author=sudokuextract.author,
    author_email=sudokuextract.author_email,
    maintainer=sudokuextract.maintainer,
    maintainer_email=sudokuextract.maintainer_email,
    url=sudokuextract.url,
    download_url=sudokuextract.download_url,
    description=sudokuextract.description,
    long_description=LONG_DESCRIPTION,
    license=sudokuextract.license,
    platforms=sudokuextract.platforms,
    keywords=sudokuextract.keywords,
    classifiers=sudokuextract.classifiers,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={
        'sudokuextract.data': ['*.gz', '*.pklz'],
    },
    install_requires=[
        'numpy>=1.10.2',
        'scipy>=0.16.1',
        'scikit-image>=0.11.3',
        'scikit-learn>=0.17'
        'matplotlib>=1.5.0',
        'pillow>=3.1.0'
    ],
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'parse-sudoku = sudokuextract.extract:main'
        ]
    },
)


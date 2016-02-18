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
import sys
from codecs import open
from setuptools import setup, find_packages

import sudokuextract

basedir = os.path.dirname(os.path.abspath(__file__))

if sys.argv[-1] == 'publish':
    os.system('python setup.py register')
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload --universal')
    sys.exit()


def read(f):
    return open(f, encoding='utf-8').read()


setup(
    name='sudokuextract',
    version=sudokuextract.__version__,
    author=sudokuextract.__author__,
    author_email=sudokuextract.__author_email__,
    maintainer=sudokuextract.__maintainer__,
    maintainer_email=sudokuextract.__maintainer_email__,
    url=sudokuextract.__url__,
    description=sudokuextract.__description__,
    long_description=read('README.rst') + '\n\n' + read('HISTORY.rst'),
    license=sudokuextract.__license__,
    platforms=sudokuextract.__platforms__,
    keywords=sudokuextract._keywords__,
    classifiers=sudokuextract.__classifiers__,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={
        'sudokuextract.data': ['*.gz', '*.pklz'],
    },
    install_requires=[
        'numpy>=1.9.2',
        'scipy>=0.15.1',
        'scikit-image>=0.11.3',
        'pillow>=3.1.0',
        'pyefd>=0.1.0'
    ],
    test_suite="tests",
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'parse-sudoku = sudokuextract.extract:main'
        ]
    },
)


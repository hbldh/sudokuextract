#!/usr/bin/env python
# -0- coding: utf-8 -0-
"""
test_images
==================

Created by: hbldh <henrik.blidh@nedomkull.com>
Created on: 2016-01-28, 20:54

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import unittest

import pytest

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from PIL import Image

from sudokuextract.extract import extract_sudoku, main
from sudokuextract.utils import predictions_to_suduko_string, download_image
from sudokuextract.ml.fit import get_default_sudokuextract_classifier

try:
    _range = xrange
except NameError:
    _range = range


def _get_img(nbr=1):
    return Image.open(_get_img_path(nbr))


def _get_img_path(nbr=1):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img{0}.jpg'.format(nbr))


def _get_parsed_img(nbr=1):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img{0}.txt'.format(nbr)), 'rt') as f:
        parsed_img = f.read().strip()
    return parsed_img


@pytest.fixture(scope="module")
def classifier():
    return get_default_sudokuextract_classifier()


def _process_an_image(image, correct_sudoku):
    predictions, sudoku, subimage = extract_sudoku(image, classifier())
    parsed_sudoku = predictions_to_suduko_string(predictions)
    assert parsed_sudoku == correct_sudoku


def test_image_1_cmd_1():
    """Test Image 1 via command line tool."""
    sys.argv = ['parse-sudoku', '-p', _get_img_path(1)]
    parsed_sudoku = main()
    correct_sudoku = _get_parsed_img(1)
    assert parsed_sudoku == correct_sudoku


def test_image_1_cmd_2():
    """Test Image 1 via command line tool."""
    sys.argv = ['parse-sudoku', '-p', _get_img_path(1), '--oneliner']
    parsed_sudoku = main()
    correct_sudoku = _get_parsed_img(1).replace('\n', '')
    assert parsed_sudoku == correct_sudoku


def test_image_2_cmd_1():
    """Test Image 1 via command line tool."""
    sys.argv = ['parse-sudoku', '-p', _get_img_path(2)]
    parsed_sudoku = main()
    correct_sudoku = _get_parsed_img(2)
    assert parsed_sudoku == correct_sudoku


def test_image_2_cmd_2():
    """Test Image 2 via command line tool."""
    sys.argv = ['parse-sudoku', '-p', _get_img_path(2), '--oneliner']
    parsed_sudoku = main()
    correct_sudoku = _get_parsed_img(2).replace('\n', '')
    assert parsed_sudoku == correct_sudoku


def test_url_1_straight():
    url = "https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/2/27/1361977880123/Sudoku2437easy.jpg"
    image = download_image(url)
    solution = ("041006029\n"
                "300790000\n"
                "009000308\n"
                "800604290\n"
                "070050060\n"
                "036108007\n"
                "403000900\n"
                "000032004\n"
                "650400730")
    _process_an_image(image, solution)


def test_url_1_via_commandline():
    url = "https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/2/27/1361977880123/Sudoku2437easy.jpg"
    sys.argv = ['parse-sudoku', '-u', url]
    parsed_sudoku = main()
    solution = ("041006029\n"
                "300790000\n"
                "009000308\n"
                "800604290\n"
                "070050060\n"
                "036108007\n"
                "403000900\n"
                "000032004\n"
                "650400730")
    assert parsed_sudoku == solution


### Parameterized tests


_, _, files = list(os.walk(os.path.dirname(__file__)))[0]
n_test_files = sum([os.path.splitext(f)[1].lower() == '.jpg' for f in files]) + 1


@pytest.mark.parametrize("nbr", _range(1, n_test_files))
def test_images(nbr):
    """Test the images located in this folder."""
    image = _get_img(nbr)
    correct_sudoku = _get_parsed_img(nbr)
    _process_an_image(image, correct_sudoku)


if os.environ.get('XANADOKU_API_TOKEN') is not None:
    import json
    _url = "https://xanadoku.herokuapp.com/getallsudokus/" + os.environ.get('XANADOKU_API_TOKEN')
    try:
        xanadoku_sudokus = json.loads(urlopen(_url).read().decode('utf-8')).get('sudokus')
    except:
        xanadoku_sudokus = []
else:
    xanadoku_sudokus = []


@pytest.mark.parametrize("sudoku_doc", xanadoku_sudokus)
def test_xanadoku_sudokus(sudoku_doc):
    if not sudoku_doc.get('verified'):
        assert True
    else:
        print(sudoku_doc.get('_id'))
        image = download_image(sudoku_doc.get('raw_image_url'))
        predictions, sudoku, subimage = extract_sudoku(image, classifier())
        parsed_sudoku = predictions_to_suduko_string(predictions, oneliner=True)
        assert parsed_sudoku == sudoku_doc.get('parsed_sudoku')


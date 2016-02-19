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

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from io import BytesIO

from PIL import Image


from sudokuextract.extract import parse_sudoku, predictions_to_suduko_string, main
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


class TestEFDClassifier(object):
    """Testing the SudokuExtract with default classifier."""
    def __init__(self):
        self.classifier = get_default_sudokuextract_classifier()

    def _print_sudokus(self, parsed_sudoku, correct_sudoku):
        print("Row comparison SudokuExtract -> Correct:\n-----------------------")
        for ser, cr in zip(parsed_sudoku.split('\n'), correct_sudoku.split('\n')):
            print("{0} =? {1}".format(ser, cr))

    def test_images(self):
        """Test a lot of images.
        """
        def _test_fcn(nbr):
            image = _get_img(nbr)
            correct_sudoku = _get_parsed_img(nbr)
            self._process_an_image(image, correct_sudoku)

        for i in _range(1, 3):
            yield _test_fcn, i

    def test_image_1_cmd_1(self):
        """Test Image 1 via command line tool."""
        sys.argv = ['parse-sudoku', '-p', _get_img_path(1)]
        parsed_sudoku = main()
        correct_sudoku = _get_parsed_img(1)
        self._print_sudokus(parsed_sudoku, correct_sudoku)
        assert parsed_sudoku == correct_sudoku

    def test_image_1_cmd_2(self):
        """Test Image 1 via command line tool."""
        sys.argv = ['parse-sudoku', '-p', _get_img_path(1), '--oneliner']
        parsed_sudoku = main()
        correct_sudoku = _get_parsed_img(1).replace('\n', '')
        self._print_sudokus(parsed_sudoku, correct_sudoku)
        assert parsed_sudoku == correct_sudoku

    def test_image_2_cmd_1(self):
        """Test Image 1 via command line tool."""
        sys.argv = ['parse-sudoku', '-p', _get_img_path(2)]
        parsed_sudoku = main()
        correct_sudoku = _get_parsed_img(2)
        self._print_sudokus(parsed_sudoku, correct_sudoku)
        assert parsed_sudoku == correct_sudoku

    def test_image_2_cmd_2(self):
        """Test Image 2 via command line tool."""
        sys.argv = ['parse-sudoku', '-p', _get_img_path(2), '--oneliner']
        parsed_sudoku = main()
        correct_sudoku = _get_parsed_img(2).replace('\n', '')
        self._print_sudokus(parsed_sudoku, correct_sudoku)
        assert parsed_sudoku == correct_sudoku

    def test_url_1_straight(self):
        url = "https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/2/27/1361977880123/Sudoku2437easy.jpg"
        image = Image.open(BytesIO(urlopen(url).read()))
        solution = ("041006029\n"
                    "300790000\n"
                    "009000308\n"
                    "800604290\n"
                    "070050060\n"
                    "036108007\n"
                    "403000900\n"
                    "000032004\n"
                    "650400730")
        self._process_an_image(image, solution)

    def test_url_1_via_commandline(self):
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
        self._print_sudokus(parsed_sudoku, solution)
        assert parsed_sudoku == solution

    def _process_an_image(self, image, correct_sudoku):
        predictions, sudoku, subimage = parse_sudoku(image, self.classifier)
        parsed_sudoku = predictions_to_suduko_string(predictions)
        self._print_sudokus(parsed_sudoku, correct_sudoku)
        assert parsed_sudoku == correct_sudoku

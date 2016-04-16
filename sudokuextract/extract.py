#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`extract`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-20

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np

from sudokuextract.exceptions import SudokuExtractError
from sudokuextract.utils import load_image, download_image, predictions_to_suduko_string
from sudokuextract.ml.fit import get_default_sudokuextract_classifier
from sudokuextract.methods import extraction_method_map, extraction_methods


def extract_sudoku(image, classifier=None, force=False):
    if classifier is None:
        classifier = get_default_sudokuextract_classifier()

    image = np.array(image.convert('L'))

    for method_name, method in extraction_methods:
        try:
            predictions, sudoku_box_images, subimage = method(image, classifier)
        except SudokuExtractError as e:
            # Try next method.
            pass
        except Exception as e:
            # Some unknown error. Raise this.
            raise
        else:
            return predictions, sudoku_box_images, subimage

    if force:
        return extraction_method_map(image, classifier, force=True, n=1)
    raise SudokuExtractError("Could not extract any Sudoku from this image.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Running SudokuExtract as a command line tool")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--path', dest='path', type=str, default=None, help="Path to an image to parse.")
    group.add_argument('-u', '--url', dest='url', type=str, default=None, help="Url to an image to parse.")
    parser.add_argument('--oneliner', action='store_true', help="Print oneliner solution.")

    args = parser.parse_args()

    if args.path is not None:
        image = load_image(args.path)
    else:
        image = download_image(args.url)

    preds, images, subimage = extract_sudoku(image)
    sudoku_string = predictions_to_suduko_string(preds, args.oneliner)
    print(sudoku_string)

if __name__ == '__main__':
    main()

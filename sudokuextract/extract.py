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

import os

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from io import BytesIO

from PIL import Image
import numpy as np

from sudokuextract.imgproc.binary import to_binary_adaptive
from sudokuextract.imgproc.blob import get_n_largest_blobs, add_border, get_extremes_of_n_largest_blobs
from sudokuextract.imgproc.lines import get_extremes
from sudokuextract.imgproc.geometry import warp_image, split_image_into_sudoku_pieces
from sudokuextract.imgproc.contour import get_contours
from sudokuextract.ml.predict import classify_efd_features


def load_image(image_path):
    return Image.open(os.path.abspath(os.path.expanduser(image_path)))


def download_image(image_url):
    r = urlopen(image_url)
    s = BytesIO(r.read())
    return Image.open(s)


def extract(image, n=10):
    img = image.convert('L')
    blobs = get_n_largest_blobs(img, n=n)
    sudoku = None
    for blob in blobs:
        try:
            c = get_contours(add_border(to_binary_adaptive(blob), size=blob.shape, border_size=1))[0]
            corner_points = get_extremes(np.fliplr(c), blob)
            warped_image = warp_image(corner_points, blob)
            sudoku = split_image_into_sudoku_pieces(to_binary_adaptive(warped_image))
        except:
            raise
        else:
            break
    return sudoku


def extraction_iterator(image, n=10):
    img = image.convert('L')
    blobs = get_n_largest_blobs(img, n=n)
    for blob in blobs:
        try:
            c = get_contours(add_border(to_binary_adaptive(blob), size=blob.shape, border_size=1))[0]
            corner_points = get_extremes(np.fliplr(c), blob)
            warped_image = warp_image(corner_points, blob)
            sudoku = split_image_into_sudoku_pieces(to_binary_adaptive(warped_image))
        except:
            pass
        else:
            yield sudoku


def extraction_iterator(image, n=10):
    img = image.convert('L')
    blobs = get_extremes_of_n_largest_blobs(img, n=n)
    for corner_points in blobs:
        try:
            warped_image = warp_image(corner_points, img)
            sudoku = split_image_into_sudoku_pieces(to_binary_adaptive(warped_image))
        except:
            pass
        else:
            yield sudoku


def parse_sudoku(image, classifier):
    for sudoku in extraction_iterator_2(image):
        pred_n_imgs = [[classify_efd_features(sudoku[k][kk], classifier) for kk in range(9)] for k in range(9)]
        preds = np.array([[pred_n_imgs[k][kk][0] for kk in range(9)] for k in range(9)])
        imgs = [[pred_n_imgs[k][kk][1] for kk in range(9)] for k in range(9)]
        if np.sum(preds > 0) >= 17:
            return preds, imgs
    raise


def predictions_to_suduko_string(predictions, oneliner=False):
    if oneliner:
        joining_char = ""
    else:
        joining_char = "\n"
    return joining_char.join(["".join([str(p) if p not in (-1, -2) else '0'
                              for p in pred_row]) for pred_row in predictions])


def main():
    import argparse
    from sudokuextract.ml.fit import get_default_sudokuextract_classifier
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

    classifier = get_default_sudokuextract_classifier()
    preds, images = parse_sudoku(image, classifier)
    sudoku_string = predictions_to_suduko_string(preds, args.oneliner)

    print(sudoku_string)
    return sudoku_string

if __name__ == '__main__':
    main()

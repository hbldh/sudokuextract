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
from sudokuextract.imgproc.binary import to_binary_adaptive
from sudokuextract.imgproc.blob import get_n_largest_blobs, add_border, get_extremes_of_n_largest_blobs, iter_blob_contours
from sudokuextract.imgproc.lines import get_extremes
from sudokuextract.imgproc import geometry
from sudokuextract.ml.predict import classify_sudoku
from sudokuextract.utils import load_image, download_image, predictions_to_suduko_string


def _extraction_iterator_v05(image, n=10):
    img = image.convert('L')
    blobs = get_n_largest_blobs(img, n=n)
    for blob in blobs:
        try:
            c = geometry.get_contours(add_border(to_binary_adaptive(blob), size=blob.shape, border_size=1))[0]
            corner_points = get_extremes(np.fliplr(c), blob)
            warped_image = geometry.warp_image(corner_points, blob)
            bin_image = to_binary_adaptive(warped_image)
            sudoku = geometry.split_image_into_sudoku_pieces_adaptive_global(bin_image)
        except:
            pass
        else:
            yield sudoku, bin_image


def _extraction_iterator_v06(image, n=10):
    img = image.convert('L')
    # If the image is too small, then double its scale until big enough.
    while max(img.size) < 500:
        img = img.resize(np.array(img.size) * 2)
    for corner_points in get_extremes_of_n_largest_blobs(img, n=n):
        try:
            warped_image = warp_image(corner_points, img)
            bin_image = to_binary_adaptive(warped_image)
            sudoku = split_image_into_sudoku_pieces(bin_image)
        except:
            pass
        else:
            yield sudoku, bin_image


def _extraction_iterator(image, use_local_thresholding=False):
    img = image.convert('L')
    # If the image is too small, then double its scale until big enough.
    while max(img.size) < 1000:
        img = img.resize(np.array(img.size) * 2)
    for edges in iter_blob_contours(img):
        try:
            warped_image = geometry.warp_image_by_interp_borders(edges, img)
            if use_local_thresholding:
                sudoku = geometry.split_image_into_sudoku_pieces_otsu_local(warped_image)
            else:
                sudoku = geometry.split_image_into_sudoku_pieces_adaptive_global(warped_image)
        except Exception as e:
            pass
        else:
            yield sudoku, warped_image


def parse_sudoku(image, classifier, use_local_thresholding=False):
    for sudoku, subimage in _extraction_iterator(image, use_local_thresholding):
        try:
            pred_n_imgs = classify_sudoku(sudoku, classifier, False)
            preds = np.array([[pred_n_imgs[k][kk][0] for kk in range(9)] for k in range(9)])
            imgs = [[pred_n_imgs[k][kk][1] for kk in range(9)] for k in range(9)]
            #if np.sum(preds > 0) >= 17:
            return preds, imgs, subimage
        except Exception as e:
            pass
    raise SudokuExtractError("Could not extract any Sudoku from this image.")


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
    preds, images, subimage = parse_sudoku(image, classifier)
    sudoku_string = predictions_to_suduko_string(preds, args.oneliner)

    print(sudoku_string)
    return sudoku_string

if __name__ == '__main__':
    main()

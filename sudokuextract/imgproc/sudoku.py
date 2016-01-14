#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`sudoku`
==================

.. module:: sudoku
    :platform: Unix, Windows
    :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@swedwise.com>

Created on 2016-01-14, 09:54

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from operator import itemgetter

from matplotlib import cm
import matplotlib.pyplot as plt

from scipy import ndimage as ndi
from skimage.feature import canny
from skimage.color import label2rgb
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from sudokuextract.imgproc.contour import get_contours
from skimage.measure import label
from skimage.measure import regionprops
import matplotlib.patches as mpatches
from skimage.morphology import binary_dilation

def is_sudoku(image):

    plt.imshow(image, cmap=cm.gray)
    plt.show()

    edges = canny(image, sigma=0.1)
    fill_img = ndi.binary_fill_holes(edges)
    edges = canny(fill_img)
    label_image = label(edges)

    boxes = []
    for region in regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        # skip small images
        if region.area < 100:
            continue
        boxes.append(region.bbox)
    if len(boxes) < 9:
        return False

    # Extract the 9 largest bounding boxes.
    boxes = sorted(boxes, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]), reverse=True)[:9]

    def _sort_fcn(x):
        mid_point = (x[3] + x[1]) / 2, (x[2] + x[0]) / 2
        return mid_point[0] + mid_point[1] * 5
    grid = sorted(boxes, key=_sort_fcn)

    # Now we have 9 boxes hopefully corresponding to the 9 grids.

    for box in grid:
        x_min, y_min, x_max, y_max = box
        subimg = image[x_min:x_max + 1, y_min:y_max+1]
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(16, 6))
        ax0.imshow(image, cmap=cm.gray)
        ax1.imshow(subimg, cmap=cm.gray)
        plt.show()

    return True

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`geometry`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-15

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np
from skimage.transform import warp, ProjectiveTransform


def warp_image(corner_points, image):
    """Given corner points of a Sudoku, warps original selection to a square image.

    :param corner_points:
    :type: corner_points: list
    :param image:
    :type image:
    :return:
    :rtype:

    """
    # Clarify by storing in named variables.
    top_left, top_right, bottom_left, bottom_right = np.array(corner_points)

    top_edge = np.linalg.norm(top_right - top_left)
    bottom_edge = np.linalg.norm(bottom_right - bottom_left)
    left_edge = np.linalg.norm(top_left - bottom_left)
    right_edge = np.linalg.norm(top_right - bottom_right)

    L = int(np.ceil(max([top_edge, bottom_edge, left_edge, right_edge])))
    src = np.array([top_left, top_right, bottom_left, bottom_right])
    dst = np.array([[0, 0], [L - 1, 0], [0, L - 1], [L - 1, L - 1]])

    tr = ProjectiveTransform()
    tr.estimate(dst, src)
    
    return warp(image, tr, output_shape=(L, L))


def split_image_into_sudoku_pieces(image):
    L = image.shape[0]
    d = L // 9
    output = [[image[k*d:(k+1)*d, kk*d:(kk+1)*d] for kk in range(9)] for k in range(9)]

    return output

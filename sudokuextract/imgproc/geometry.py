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

from operator import attrgetter

import numpy as np
from skimage.morphology import binary_closing, binary_erosion, binary_opening, disk
from skimage.transform import warp, ProjectiveTransform
from skimage.measure import find_contours

from sudokuextract.imgproc.binary import to_binary_otsu, to_binary_adaptive


def warp_image_by_interp_borders(edges, image):
    left_edge, top_edge, right_edge, bottom_edge = edges

    left_edge = left_edge[::-1, :]
    bottom_edge = bottom_edge[::-1, :]

    def _mapping_fcn(points):
        map_x = (points[:, 0] / float(points[-1, 0]))
        map_y = (points[:, 1] / float(points[-1, 1]))

        top_mapping = np.array(np.round(map_x * (len(top_edge) - 1)), 'int')
        bottom_mapping = np.array(np.round(map_x * (len(bottom_edge) - 1)), 'int')
        left_mapping = np.array(np.round(map_y * (len(left_edge) - 1)), 'int')
        right_mapping = np.array(np.round(map_y * (len(right_edge) - 1)), 'int')

        map_x = np.array([map_x, map_x]).T
        map_y = np.array([map_y, map_y]).T

        p1s = (left_edge[left_mapping, :] * (1 - map_x)) + (right_edge[right_mapping, :] * map_x)
        p2s = (top_edge[top_mapping, :] * (1 - map_y)) + (bottom_edge[bottom_mapping, :] * map_y)

        return (p1s + p2s) / 2

    d_top_edge = np.linalg.norm(top_edge[0, :] - top_edge[-1, :])
    d_bottom_edge = np.linalg.norm(bottom_edge[0, :] - bottom_edge[-1, :])
    d_left_edge = np.linalg.norm(left_edge[0, :] - left_edge[-1, :])
    d_right_edge = np.linalg.norm(right_edge[0, :] - right_edge[-1, :])

    d = int(np.ceil(max([d_top_edge, d_bottom_edge, d_left_edge, d_right_edge])))
    wi = warp(image, _mapping_fcn, output_shape=(d, d))

    return wi


def split_image_into_sudoku_pieces_adaptive_global(image, otsu_local=False):
    L = image.shape[0]
    d = int(np.ceil(L / 9))
    dd = d // 6
    output = []
    if not otsu_local:
        image = to_binary_adaptive(image)
    for k in range(9):
        this_row = []
        start_row_i = max([k * d - dd, 0])
        stop_row_i = min([(k + 1) * d + dd, L])
        for kk in range(9):
            start_col_i = max([kk * d - dd, 0])
            stop_col_i = min([(kk + 1) * d + dd, L])
            i = image[start_row_i:stop_row_i, start_col_i:stop_col_i].copy()
            if otsu_local:
                i = to_binary_otsu(i)
            i = binary_opening(i)
            i = to_binary_otsu(i)
            this_row.append(i)
        output.append(this_row)
    return output


def get_contours(img, contour_param=0.8):
    # Find contours
    contours = find_contours(img, contour_param)
    # Sort with largest first.
    contours.sort(key=attrgetter('size'), reverse=True)
    return contours

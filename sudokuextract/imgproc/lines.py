#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`lines`
==================

.. module:: lines
    :platform: Unix, Windows
    :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2016-01-14, 13:56

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np
from skimage.transform import hough_line, hough_line_peaks

from sudokuextract.imgproc.binary import to_binary_adaptive


def get_lines(image):
    bimg = -to_binary_adaptive(image)

    h, theta, d = hough_line(bimg)
    row1, col1 = image.shape
    line_defs = []
    for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
        m = -1 / np.tan(angle)
        c = dist / np.sin(angle)
        line_defs.append(((0, col1), (m, c)))
    return line_defs


def get_intersections(lines, image):
    intersections = []
    for i, ((x0, x1), line_1) in enumerate(lines):
        for j, (_, line_2) in enumerate(lines):
            if i == j:
                continue
            if np.abs((line_1[0] - line_2[0])) < 1e-16:
                continue

            a, c = line_1
            b, d = line_2

            x = (d - c) / (a - b)
            y = -(((-a) * x) - c)

            if x < -20 or x > (image.shape[1] + 20):
                continue
            if y < -20 or y > (image.shape[0] + 20):
                continue

            intersections.append((x, y))
    return intersections


def get_extremes(points, image):
    top_left = sorted(points, key=lambda x: np.linalg.norm(np.array(x)))[0]
    top_right = sorted(points, key=lambda x: np.linalg.norm(np.array(x) - [image.shape[1], 0]))[0]
    bottom_left = sorted(points, key=lambda x: np.linalg.norm(np.array(x) - [0, image.shape[0]]))[0]
    bottom_right = sorted(points, key=lambda x: np.linalg.norm(np.array(x) - [image.shape[1], image.shape[0]]))[0]

    return top_left, top_right, bottom_left, bottom_right

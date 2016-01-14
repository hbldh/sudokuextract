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
from skimage.filters import gaussian_filter, threshold_adaptive
from skimage.transform import hough_line, hough_line_peaks


def get_lines(image):
    bimg = gaussian_filter(image, sigma=1.0)
    bimg = threshold_adaptive(bimg, 20, offset=2/255)
    bimg = -bimg

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
    #import matplotlib.pyplot as plt
    #plt.imshow(image, plt.cm.gray)
    for i, ((x0, x1), line_1) in enumerate(lines):
        #plt.plot((x0, x1), (line_1[0] * x0 + line_1[1], line_1[0] * x1 + line_1[1]), 'r')
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
    # plt.xlim((x0, x1))
    # plt.ylim((image.shape[0], 0))
    # for p in intersections:
    #     plt.plot(p[0], p[1], 'g+')
    # plt.show()
    return intersections


def get_extremes(points, image):

    top_left = sorted(points, key=lambda x: np.linalg.norm(np.array(x)))[0]
    top_right = sorted(points, key=lambda x: np.linalg.norm(np.array(x) - [image.shape[1], 0]))[0]
    bottom_left = sorted(points, key=lambda x: np.linalg.norm(np.array(x) - [0, image.shape[0]]))[0]
    bottom_right = sorted(points, key=lambda x: np.linalg.norm(np.array(x) - [image.shape[1], image.shape[0]]))[0]

    # import matplotlib.pyplot as plt
    # plt.imshow(image, plt.cm.gray)
    # plt.plot(top_left[0], top_left[1], 'ro')
    # plt.plot(top_right[0], top_right[1], 'ro')
    # plt.plot(bottom_left[0], bottom_left[1], 'ro')
    # plt.plot(bottom_right[0], bottom_right[1], 'ro')
    #
    # plt.show()

    return top_left, top_right, bottom_left, bottom_right

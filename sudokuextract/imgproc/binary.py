#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`binary`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-26

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np
from skimage.transform import resize
from skimage.filters import threshold_otsu
from skimage.morphology import skeletonize
from skimage.filters import gaussian_filter, threshold_adaptive


def to_binary_otsu(img, invert=False):
    if img.max() == img.min():
        return np.array(img, 'uint8')
    else:
        t = threshold_otsu(img)
    img[img <= t] = 255 if invert else 0
    img[img > t] = 0 if invert else 255
    return np.array(img, 'uint8')


def to_binary_adaptive(img):
    bimg = gaussian_filter(img, sigma=1.0)
    bimg = threshold_adaptive(bimg, 20, offset=2 / 255)
    bimg = np.array(bimg, 'uint8') * 255
    return bimg


def add_border(img, size=(28, 28), border_size=0, background_value=255):
    img = resize(img, (size[0] - border_size * 2,
                       size[1] - border_size * 2))
    img = np.array(img * 255, 'uint8')

    output_img = np.ones(size, 'uint8') * background_value
    if border_size == 0:
        output_img[:, :] = img
    else:
        output_img[border_size:-border_size, border_size:-border_size] = img
    return output_img

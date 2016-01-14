#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`hbldh`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-22

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np

from sudokuextract.imgproc.contour import get_contours
from sudokuextract.imgproc.efd import elliptical_fourier_descriptors, normalize_efd


def extract_efd_features(image, n=20):
    contours = get_contours(image)
    if len(contours) == 0:
        return np.zeros((4*n))[3:]
    efd = elliptical_fourier_descriptors(contours[0], n=n, normalize=True)

    return efd.flatten()[3:]

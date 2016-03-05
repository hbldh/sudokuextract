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

from pyefd import elliptic_fourier_descriptors

from sudokuextract.imgproc.geometry import get_contours


def extract_efd_features(image, n=10):
    contours = get_contours(image)
    if len(contours) == 0:
        return np.zeros((4*n))[3:]
    efd = elliptic_fourier_descriptors(contours[0], order=n, normalize=True)

    return efd.flatten()[3:]

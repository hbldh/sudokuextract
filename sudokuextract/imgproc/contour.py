#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`contour`
==================

.. module:: contour
    :platform: Unix, Windows
    :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@swedwise.com>

Created on 2016-01-14, 09:49

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from operator import attrgetter
from skimage.filters import threshold_adaptive
from skimage import measure


def get_contours(img, contour_param=0.8):
    # Find contours
    contours = measure.find_contours(img, contour_param)
    contours.sort(key=attrgetter('size'), reverse=True)
    return contours

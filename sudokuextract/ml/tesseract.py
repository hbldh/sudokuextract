#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`knn`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-16

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os

import numpy as np
from PIL import Image
from skimage.transform import resize
from skimage.filters import threshold_otsu

try:
    import pytesseract
except ImportError:
    pytesseract = None
    print("pytesseract was not installed on this system. Returning 0...")


def classify_tesseract(image):
    if pytesseract is None:
        return 0
    img = resize(image, (200, 200))
    t = threshold_otsu(image)
    img[img < t] = 0
    img[img >= t] = 255
    img = np.array(img * 255, 'uint8')

    img = Image.fromarray(img)
    tmp_file_path = os.path.expanduser("~/img.jpg")
    with open(tmp_file_path, "w") as f:
        img.save(f)
    s = pytesseract.image_to_string(img, config="-psm 9 digits").strip()
    os.remove(tmp_file_path)
    print("Parsed text: {0}".format(s))
    return s

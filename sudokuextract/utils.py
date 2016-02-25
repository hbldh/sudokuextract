#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`utils`
=======================

.. moduleauthor:: hbldh <henrik.blidh@swedwise.com>
Created on 2016-02-19, 13:44

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from io import BytesIO
import os
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from PIL import Image


def load_image(image_path):
    return Image.open(os.path.abspath(os.path.expanduser(image_path)))


def download_image(image_url):
    return Image.open(BytesIO(urlopen(image_url).read()))


def predictions_to_suduko_string(predictions, oneliner=False):
    if oneliner:
        joining_char = ""
    else:
        joining_char = "\n"
    return joining_char.join(["".join([str(p) if p not in (-1, -2) else '0'
                              for p in pred_row]) for pred_row in predictions])

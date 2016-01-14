#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkg_resources import resource_filename

from PIL import Image


def img1():
    return Image.open(resource_filename('sudokuextract.data', 'img1.jpg'))

def img2():
    return Image.open(resource_filename('sudokuextract.data', 'img2.jpg'))


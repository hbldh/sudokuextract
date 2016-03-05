#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`run`
==================

.. module:: run
    :platform: Unix, Windows
    :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2016-01-14, 09:10

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


import matplotlib.pyplot as plt

from sudokuextract.extract import extract_sudoku
from sudokuextract.ml import fit
from sudokuextract.utils import load_image, download_image, predictions_to_suduko_string

try:
    _range = xrange
except NameError:
    _range = range

image_url = "https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/2/27/1361977880123/Sudoku2437easy.jpg"
the_image = download_image(image_url)

#the_image = load_image('~/Documents/SudokuExtract_Train/img18.jpg')
#the_image = the_image.rotate(-90)

classifier = fit.get_default_sudokuextract_classifier()
preds, sudoku, subimage = extract_sudoku(the_image, classifier, force=True)

ax = plt.subplot2grid((9, 9+9), (0, 0), colspan=9, rowspan=9)
ax.imshow(subimage, plt.cm.gray)
ax.axis('off')

for k in _range(len(sudoku)):
    for kk in _range(len(sudoku[k])):
        ax = plt.subplot2grid((9, 9 + 9), (k, 9+kk))
        ax.imshow(sudoku[k][kk], plt.cm.gray)
        ax.set_title(str(preds[k, kk]))
        ax.axis('off')

plt.show()





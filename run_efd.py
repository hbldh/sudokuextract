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

from sudokuextract.extract import extract_sudoku
from sudokuextract.ml import fit
from sudokuextract.utils import download_image, load_image

from sudokuextract import data
#images, labels, X, y = data.create_mnist_dataset()
#data.save_training_data(X, y, data_source='mnist')
#images, labels, X, y = data.create_data_set_from_images('~/Documents/SudokuExtract_Train')
#data.save_training_data(X, y, data_source='se')

#data.fetch_all_xanadoku_images('~/Documents/SudokuExtract_Test', 'bjornbar')

#image_url = "https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/2/27/1361977880123/Sudoku2437easy.jpg"
#the_image = download_image(image_url)

the_image = load_image('~/Documents/SudokuExtract_Test/56d9aad9ae834500099af4da.jpg')
the_image = load_image('~/Documents/SudokuExtract_Test/56e006a63e921a0009d40071.jpg')
the_image = load_image('~/Documents/SudokuExtract_Test/56e0053e3e921a0009d40070.jpg')
#the_image = the_image.rotate(-90)

classifier = fit.get_default_sudokuextract_classifier()
preds, sudoku, subimage = extract_sudoku(the_image, classifier, force=True)

import matplotlib.pyplot as plt
ax = plt.subplot2grid((9, 9+9), (0, 0), colspan=9, rowspan=9)
ax.imshow(subimage, plt.cm.gray)
ax.axis('off')

for k in range(len(sudoku)):
    for kk in range(len(sudoku[k])):
        ax = plt.subplot2grid((9, 9 + 9), (k, 9+kk))
        ax.imshow(sudoku[k][kk], plt.cm.gray)
        ax.set_title(str(preds[k, kk]))
        ax.axis('off')
plt.show()





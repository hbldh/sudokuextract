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

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from sudokuextract.extract import parse_sudoku
from sudokuextract.ml import fit

try:
    _range = xrange
except NameError:
    _range = range

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from io import BytesIO

from PIL import Image

#from sudokuextract.data import create_data_set_from_images
#create_data_set_from_images(path_to_data_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sudokuextract/data'))

image_url = "https://static-secure.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/2/27/1361977880123/Sudoku2437easy.jpg"
r = urlopen(image_url)
s = BytesIO(r.read())
the_image = Image.open(s)

#classifier = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=5), n_estimators=200)
#classifier = RandomForestClassifier(n_estimators=100)
#classifier = KNeighborsClassifier()
#classifier = fit.fit_sudokuextract_classifier(classifier)
classifier = fit.get_default_sudokuextract_classifier()

preds, sudoku = parse_sudoku(the_image, classifier)

ax = plt.subplot2grid((9, 9+9), (0, 0), colspan=9, rowspan=9)
ax.imshow(the_image, plt.cm.gray)
ax.axis('off')

for k in _range(len(sudoku)):
    for kk in _range(len(sudoku[k])):
        ax = plt.subplot2grid((9, 9 + 9), (k, 9+kk))
        ax.imshow(sudoku[k][kk], plt.cm.gray)
        ax.set_title(str(preds[k, kk]))
        ax.axis('off')

plt.show()





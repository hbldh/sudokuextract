#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from sudokuextract.imgproc.blob import get_centered_blob
from sudokuextract.ml.features import extract_efd_features


def classify_sudoku(sudoku, classifier):
    return [[classify_efd_features(sudoku[k][kk], classifier) for kk in range(9)] for k in range(9)]


def classify_efd_features(image, classifier):
    img = get_centered_blob(image)
    if img is None:
        return -1, image
    X = extract_efd_features(img)
    prediction = classifier.predict(X.reshape((1, len(X))))[0]

    return prediction, img

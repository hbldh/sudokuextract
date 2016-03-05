#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from sudokuextract.imgproc.blob import get_centered_blob
from sudokuextract.ml.features import extract_efd_features


def classify_sudoku(sudoku, classifier, apply_filtering=False):
    if not apply_filtering:
        return [[classify_efd_features(sudoku[k][kk], classifier) for kk in range(9)] for k in range(9)]
    blobs = []
    ms = []
    for k in range(len(sudoku)):
        blobs.append([])
        for kk in range(len(sudoku[k])):
            blob = get_centered_blob(sudoku[k][kk])
            if blob is None:
                blobs[k].append((blob, 0.0))
            else:
                m = blob.mean()

                ms.append(m)
                blobs[k].append((blob, m))

    mean_median = np.median(ms)
    mean_std = np.std(ms)

    out = []
    for k in range(len(blobs)):
        out.append([])
        for kk in range(len(blobs[k])):
            if blobs[k][kk][0] is not None:
                if blobs[k][kk][1] > (mean_median + 1.96*mean_std):
                    out[k].append((-1, sudoku[k][kk]))
                elif blobs[k][kk][1] < (mean_median - 1.96*mean_std):
                    out[k].append((-1, sudoku[k][kk]))
                else:
                    X = extract_efd_features(blobs[k][kk][0])
                    prediction = classifier.predict(X.reshape((1, len(X))))[0]
                    out[k].append((prediction, blobs[k][kk][0]))
            else:
                out[k].append((-1, sudoku[k][kk]))
    return out


def classify_efd_features(image, classifier):
    img = get_centered_blob(image)
    if img is None:
        return -1, image
    X = extract_efd_features(img)
    prediction = classifier.predict(X.reshape((1, len(X))))[0]

    return prediction, img

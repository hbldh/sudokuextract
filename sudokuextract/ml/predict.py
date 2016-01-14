#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sudokuextract.imgproc.blob import get_centered_blob
from sudokuextract.ml.features import extract_efd_features


def classify_efd_features(image, classifier):
    img = get_centered_blob(image)
    if img is None:
        return -1, image
    X = extract_efd_features(img)
    prediction = classifier.predict(X.reshape((1, len(X))))[0]

    return prediction, img


def classify_template_matching(image, classifier):
    img = get_centered_blob(image)
    if img is None:
        return -1, image
    prediction = classifier.predict(img.reshape((1, 28*28)))[0]

    return prediction, img

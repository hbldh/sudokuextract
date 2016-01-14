#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`rf`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-20

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import itertools
from pkg_resources import resource_filename, resource_exists
try:
    import cPickle as pickle
except ImportError:
    import pickle
import gzip

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from sudokuextract.data import get_sudokuextract_data, get_mnist_data
from sudokuextract.ml.features import extract_efd_features
from sudokuextract.imgproc.blob import blobify

try:
    _range = xrange
except NameError:
    _range = range


def fit_sudokuextract_classifier(classifier):
    print("Fetch SudokuExtract data...")
    images, y = get_sudokuextract_data(flat_images=False)
    print("Pre-blobify:  Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))
    _, mask = blobify(images)
    images = list(itertools.compress(images, mask))
    y = y[mask]

    print("Extract features...")
    images, mask = blobify(images)
    y = y[mask]
    X = np.array([extract_efd_features(img) for img in images])

    print("Train classifier on SudokuExtract data...")
    print("Post-blobify: Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))
    classifier.fit(X, y)

    print("Completed training.")
    return classifier


def fit_mnist_classifier(classifier):
    print("Fetch MNIST data...")
    images, y = get_mnist_data(flat_images=False)
    zeros_mask = y != 0
    images = itertools.compress(images, zeros_mask)
    y = y[zeros_mask]

    print("Extract features...")
    X = np.array([np.array(extract_efd_features(img)) for img in images])

    print("Train classifier on MNIST data...")
    print("Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))
    classifier.fit(X, y)

    print("Completed training.")
    return classifier


def fit_combined_classifier(classifier):
    print("Fetch MNIST and SudokuExtract data...")
    images1, y1 = get_sudokuextract_data(flat_images=False)
    images2, y2 = get_mnist_data(flat_images=False)
    zeros_mask = y2 != 0
    images2 = itertools.compress(images2, zeros_mask)
    y2 = y2[zeros_mask]
    images = images1 + list(images2)
    y = np.concatenate((y1, y2))
    _, mask = blobify(images)
    images = list(itertools.compress(images, mask))
    y = y[mask]

    print("Extract features...")
    X = np.array([extract_efd_features(img) for img in images])

    print("Train classifier on MNIST data...")
    print("Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))
    classifier.fit(X, y)

    print("Completed training.")
    return classifier


def get_default_mnist_classifier():
    print("Fetch MNIST data...")
    images, y = get_mnist_data(flat_images=False)
    images, mask = blobify(images)
    y = y[mask]
    X = np.array([x.flatten() for x in images])

    print("Train classifier on MNIST data...")
    print("Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))
    classifier = KNeighborsClassifier()
    classifier.fit(X, y)

    print("Completed training.")
    return classifier


def get_default_sudokuextract_classifier():
    fname = resource_filename('sudokuextract.data', "sudokuextract_classifier.pklz")
    if resource_exists('sudokuextract.data', "sudokuextract_classifier.pklz"):
        f = gzip.open(fname, 'rb')
        classifier = pickle.load(f)
        f.close()
    else:
        classifier = KNeighborsClassifier()
        classifier = fit_sudokuextract_classifier(classifier)
        f = gzip.open(fname, 'wb')
        pickle.dump(classifier, f)
        f.close()

    return classifier

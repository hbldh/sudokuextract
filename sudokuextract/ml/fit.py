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

import sys
import itertools
from pkg_resources import resource_filename, resource_exists
try:
    import cPickle as pickle
except ImportError:
    import pickle
import gzip

import numpy as np
try:
    from sklearn.neighbors import KNeighborsClassifier
    _use_sklearn = True
except ImportError:
    from sudokuextract.ml.knn import KNeighborsClassifier
    _use_sklearn = False

from sudokuextract.data import get_sudokuextract_data, get_mnist_data

try:
    _range = xrange
except NameError:
    _range = range


def fit_sudokuextract_classifier(classifier):
    print("Fetch SudokuExtract data...")
    X, y = get_sudokuextract_data()

    print("Train classifier on SudokuExtract data...")
    print("Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))
    classifier.fit(X, y)

    print("Completed training.")
    return classifier


def fit_combined_classifier(classifier):
    print("Fetch data...")
    X1, y1 = get_sudokuextract_data()
    X2, y2 = get_mnist_data()
    X = np.concatenate([X1, X2], axis=0)
    y = np.concatenate([y1, y2])

    print("Train classifier on SudokuExtract and MNIST data...")
    print("Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))
    classifier.fit(X, y)

    print("Completed training.")
    return classifier


def get_default_sudokuextract_classifier():
    if _use_sklearn:
        return _load_sklearn_default_classifier()
    else:
        return _load_sudokuextract_default_classifier()


def _load_sklearn_default_classifier():
    if sys.version_info[0] == 2:
        file_name = "sklearn_classifier_py2.pklz"
        protocol = 2
    else:
        file_name = "sklearn_classifier_py3.pklz"
        protocol = 3

    file_path = resource_filename('sudokuextract.data', file_name)
    if resource_exists('sudokuextract.data', file_name):
        f = gzip.open(file_path, 'rb')
        classifier = pickle.load(f)
        f.close()
    else:
        classifier = KNeighborsClassifier(n_neighbors=10)
        classifier = fit_combined_classifier(classifier)
        f = gzip.open(file_path, 'wb')
        pickle.dump(classifier, f, protocol=protocol)
        f.close()

    return classifier


def _load_sudokuextract_default_classifier():
    file_name = "sudokuextract_classifier.pklz"
    protocol = 2

    file_path = resource_filename('sudokuextract.data', file_name)
    if resource_exists('sudokuextract.data', file_name):
        f = gzip.open(file_path, 'rb')
        classifier_json = pickle.load(f)
        classifier = KNeighborsClassifier(classifier_json.get('n_neighbors'),
                                          classifier_json.get('weights'),
                                          classifier_json.get('metric'),
                                          classifier_json.get('p'))
        classifier.fit(np.array(classifier_json.get('data')),
                       np.array(classifier_json.get('labels')))
        f.close()
    else:
        classifier = KNeighborsClassifier(n_neighbors=10)
        classifier = fit_combined_classifier(classifier)
        f = gzip.open(file_path, 'wb')
        pickle.dump(classifier.to_json(), f, protocol=protocol)
        f.close()
    return classifier

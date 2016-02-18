#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`knn`
==========

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-02-18

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np
from scipy.stats import mode


class KNeighborsClassifier(object):
    """Classifier implementing the k-nearest neighbors.

    Read more at e.g. `Wikipedia <http://en.wikipedia.org/wiki/K-nearest_neighbor_algorithm`_

    Note that this classifier borrows heavily of the structure and documentation
    of the one in scikit-learn!

    Parameters
    ----------
    n_neighbors : int, optional (default = 5)
        Number of neighbors to use by default for :meth:`k_neighbors` queries.

    weights : str
        weight function used in prediction.  Possible values:

        - 'uniform' : uniform weights.  All points in each neighborhood
          are weighted equally.
        - 'distance' : weight points by the inverse of their distance.
          in this case, closer neighbors of a query point will have a
          greater influence than neighbors which are further away.

        Uniform weights are used by default.

    metric : string or DistanceMetric object (default = 'minkowski')
        the distance metric to use for the tree.  The default metric is
        minkowski, and with p=2 is equivalent to the standard Euclidean
        metric.

    p : integer, optional (default = 2)
        Power parameter for the Minkowski metric. When p = 1, this is
        equivalent to using manhattan_distance (l1), and euclidean_distance
        (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.

    Examples
    --------
    >>> X = [[0], [1], [2], [3]]
    >>> y = [0, 0, 1, 1]
    >>> from sudokuextract.ml.knn import KNeighborsClassifier
    >>> neigh = KNeighborsClassifier(n_neighbors=3)
    >>> neigh.fit(X, y) # doctest: +ELLIPSIS
    KNeighborsClassifier(...)
    >>> print(neigh.predict([[1.1]]))
    [0]

    """

    def __init__(self, n_neighbors=5, weights='uniform', metric='minkowski', p=2):

        self.n_neighbors = int(n_neighbors)
        self.weights = str(weights)
        self.metric = str(metric)
        self.p = int(p)

        self._data = None
        self._labels = None
        self._classes = []
        self._is_fitted = False

    def to_json(self):
        return {
            'n_neighbors': self.n_neighbors,
            'weights': self.weights,
            'metric': self.metric,
            'p': self.p,
            'data': self._data.tolist(),
            'labels': self._labels.tolist()
        }

    def fit(self, X, y):
        """Fit the model using X as training data and y as target values"""

        self._data = X
        self._classes = np.unique(y)
        self._labels = y
        self._is_fitted = True

    def predict(self, X):
        """Predict the class labels for the provided data

        Parameters
        ----------
        X : array-like, shape (n_query, n_features).
            Test samples.

        Returns
        -------
        y : array of shape [n_samples]
            Class labels for each data sample.

        """
        # TODO: Make classification of multiple samples a bit more effective...
        if X.ndim > 1 and X.shape[1] != 1:
            out = []
            for x in X:
                out += self.predict(x)
            return out
        X = X.flatten()

        if self.metric == 'minkowski':
            dists = np.sum(np.abs(self._data - X) ** self.p, axis=1)
        else:
            # TODO: Implement other metrics.
            raise ValueError("Only Minkowski distance metric implemented...")

        argument = np.argsort(dists)
        labels = self._labels[argument[:self.n_neighbors]]

        if self.weights == 'distance':
            weights = 1 / dists[argument[:self.n_neighbors]]
            out = np.zeros((len(self._classes), ), 'float')
            for i, c in enumerate(self._classes):
               out[i] = np.sum(weights[labels == c])
            out /= np.sum(out)
            y_pred = self._labels[np.argmax(out)]
        else:
            y_pred, _ = mode(labels)

        return y_pred.tolist()



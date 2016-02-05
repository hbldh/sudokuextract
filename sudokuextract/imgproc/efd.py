#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`efd`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-30

A Python implementation of the method described in [1]_ for
calculating Fourier coefficients for characterizing
closed contours.

References:
-----------

.. [1] F. P. Kuhl and C. R. Giardina, “Elliptic Fourier Features of a
   Closed Contour," Computer Vision, Graphics and Image Processing,
       Vol. 18, pp. 236-258, 1982.

.. [2] Oivind Due Trier, Anil K. Jain and Torfinn Taxt, “Feature Extraction
   Methods for Character Recognition - A Survey”, Pattern Recognition
   Vol. 29, No.4, pp. 641-662 (1996)

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np

try:
    _range = xrange
except NameError:
    _range = range


def elliptical_fourier_descriptors(contour, n=10, normalize=False):
    """Calculate elliptical Fourier descriptors for a contour.

    :param contour: A contour array of size [M x 2].
    :type contour: :py:class:`numpy.ndarray`
    :param n: The order of Fourier coefficients to calculate.
    :type n: int
    :param normalize: If the coefficients should be normalized
                      as is described in [1]_ and [2]_.
    :type normalize: bool
    :return: A [n x 4] array of Fourier coefficients.
    :rtype: :py:class:`numpy.ndarray`

    """
    dxy = np.diff(contour, axis=0)
    dt = np.sqrt((dxy ** 2).sum(axis=1))
    t = np.cumsum(dt)
    T = t[-1]

    phi = np.concatenate([([0., ]), (2 * np.pi * t) / T])

    coeffs = np.zeros((n, 4))
    for i in _range(1, n + 1):
        const = T / (2 * i * i * np.pi * np.pi)
        phi_n = phi * i
        d_cos_phi_n = np.cos(phi_n[1:]) - np.cos(phi_n[:-1])
        d_sin_phi_n = np.sin(phi_n[1:]) - np.sin(phi_n[:-1])
        a_n = const * np.sum((dxy[:, 0] / dt) * d_cos_phi_n)
        b_n = const * np.sum((dxy[:, 0] / dt) * d_sin_phi_n)
        c_n = const * np.sum((dxy[:, 1] / dt) * d_cos_phi_n)
        d_n = const * np.sum((dxy[:, 1] / dt) * d_sin_phi_n)
        coeffs[i - 1, :] = a_n, b_n, c_n, d_n

    if normalize:
        coeffs = normalize_efd(coeffs)

    return coeffs


def normalize_efd(coeffs, rotation_invariant=True, size_invariant=True):
    """Normalizes an array of Fourier coefficients.

    See details in [1]_ or [2]_.

    :param coeffs: A [n x 4] Fourier coefficient array.
    :type coeffs: :py:class:`numpy.ndarray`
    :return: The normalized [n x 4] Fourier coefficient array.
    :rtype: :py:class:`numpy.ndarray`

    """
    # Make the coefficients have a zero phase shift from
    # the first major axis. Theta_1 is that shift angle.
    theta_1 = 0.5 * np.arctan2(
        2 * ((coeffs[0, 0] * coeffs[0, 1]) + (coeffs[0, 2] * coeffs[0, 3])),
        ((coeffs[0, 0] ** 2) - (coeffs[0, 1] ** 2) + (coeffs[0, 2] ** 2) - (coeffs[0, 3] ** 2)))
    # Rotate all coefficients by theta_1.
    for n in _range(1, coeffs.shape[0] + 1):
        coeffs[n - 1, :] = np.dot(
            np.array([[coeffs[n - 1, 0], coeffs[n - 1, 1]],
                      [coeffs[n - 1, 2], coeffs[n - 1, 3]]]),
            np.array([[np.cos(n * theta_1), -np.sin(n * theta_1)],
                      [np.sin(n * theta_1), np.cos(n * theta_1)]])).flatten()

    if rotation_invariant:
        # Make the coefficients rotation invariant by rotating so that
        # the semi-major axis is parallel to the x-axis.
        psi_1 = np.arctan2(coeffs[0, 2], coeffs[0, 0])
        psi_rotation_matrix = np.array([[np.cos(psi_1), np.sin(psi_1)],
                                        [-np.sin(psi_1), np.cos(psi_1)]])
        # Rotate all coefficients by -psi_1.
        for n in _range(1, coeffs.shape[0] + 1):
            coeffs[n - 1, :] = psi_rotation_matrix.dot(
                np.array([[coeffs[n - 1, 0], coeffs[n - 1, 1]],
                          [coeffs[n - 1, 2], coeffs[n - 1, 3]]])).flatten()

    if size_invariant:
        # Obtain size-invariance by normalizing.
        coeffs /= np.abs(coeffs[0, 0])

    return coeffs


def plot_efd(contour, coeffs, locus=(0., 0.), n=300):
    """Plot a [2 x (n/2)] grid of successive truncations of the series.

    :param coeffs:  [n x 4] Fourier coefficient array.
    :type coeffs: :py:class:`numpy.ndarray`
    :param locus: The A_0 and C_0 elliptic locus in [1]_ and [2]_.
    :type locus: list, tuple or :py:class:`numpy.ndarray`
    :param n: Number of points to use for plotting of Fourier series.
    :type n: int

    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Cannot plot: matplotlib was not installed.")
        return

    N = coeffs.shape[0]
    t = np.linspace(0, 1.0, n)
    xt = np.ones((n,)) * locus[0]
    yt = np.ones((n,)) * locus[1]

    ax = plt.subplot2grid((3, N // 2), (0, 0), colspan=N//2)
    ax.imshow(contour, plt.cm.gray)
    for n in _range(coeffs.shape[0]):
        xt += (coeffs[n, 0] * np.cos(2 * (n + 1) * np.pi * t)) + \
              (coeffs[n, 1] * np.sin(2 * (n + 1) * np.pi * t))
        yt += (coeffs[n, 2] * np.cos(2 * (n + 1) * np.pi * t)) + \
              (coeffs[n, 3] * np.sin(2 * (n + 1) * np.pi * t))
        ax = plt.subplot2grid((3, N // 2), (n // (N // 2) + 1, n % (N // 2)))
        ax.set_title(str(n + 1))
        ax.plot(yt, -xt, 'r')

    plt.show()

if __name__ == '__main__':
    import pkg_resources
    from PIL import Image
    from sudokuextract.imgproc.blob import get_centered_blob
    from sudokuextract.imgproc.contour import get_contours

    file_name = pkg_resources.resource_filename("sudokuextract.data.train", "138_3.jpg")
    image = np.array(Image.open(file_name).convert('L'))
    blob = get_centered_blob(image, border_size=1)
    contour = get_contours(blob)[0]

    efd = elliptical_fourier_descriptors(contour, normalize=True)

    plot_efd(image, efd)

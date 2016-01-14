#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`blob`
==================

.. module:: blob
    :platform: Unix, Windows
    :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2016-01-14, 11:45

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from operator import itemgetter

import numpy as np
from scipy import ndimage as ndi
from skimage.filters import gaussian_filter, threshold_adaptive
from skimage.measure import label
from skimage.measure import regionprops

from sudokuextract.imgproc.binary import to_binary, add_border


def get_n_largest_blobs(image, n=5):
    if max(image.size) < 2000:
        size = (500, 500)
    else:
        size = (1000, 1000)

    img = np.array(image.resize(size))
    bimg = gaussian_filter(img, sigma=1.0)
    bimg = threshold_adaptive(bimg, 20, offset=2/255)
    bimg = -bimg

    bimg = ndi.binary_fill_holes(bimg)
    label_image = label(bimg, background=False)
    label_image += 1
    blobs = []
    for region in regionprops(label_image):
        # skip small images
        if region.area < int(np.prod(size) * 0.05):
            continue
        blobs.append((region.filled_area, region.bbox))

    blobs.sort(key=itemgetter(0))
    return [img[b[0]:b[2], b[1]:b[3]] for sol, b in blobs[:n]]


def blobify(images, flat_images=False):
    output_data = []
    mask = []
    for d in images:
        if d.shape == (28, 28):
            blob = get_centered_blob(d)
        else:
            blob = get_centered_blob(d.reshape((28, 28)))

        if blob is not None:
            if flat_images:
                output_data.append(blob.flatten())
            else:
                output_data.append(blob)
            mask.append(True)
        else:
            mask.append(False)

    if flat_images:
        output_data = np.array(output_data)
    return output_data, np.array(mask)


def _get_most_centered_blob(image):
    # Label the binary image sent into connected black resp. white areas.
    label_image = label(image)
    blobs = []

    if len(np.unique(label_image)) == 1:
        return image

    # Create intensity image.
    i_img = 255 - image
    i_img[i_img == 255] = 1

    for region in regionprops(label_image, i_img):
        # Skip to small regions.
        if region.area < (np.prod(image.shape) * 0.030):
            continue

        # Skip all regions that are white.
        if region.max_intensity < 0.9:
            continue

        # Extract bounding box.
        a_min, b_min, a_max, b_max = region.bbox
        a_dist = a_max - a_min
        b_dist = b_max - b_min

        # If the bounding box is larger than half of the image, check
        # whether or not the region's relative filled area is smaller than 0.5
        if (a_dist * b_dist) > (np.prod(image.shape) * 0.5):
            if (region.solidity / (a_dist * b_dist)) < 0.5:
                continue

        # Make bounding box square, centered with respect to the largest side.
        if a_dist < b_dist:
            a_mid = (a_min + a_max) // 2
            a_max = a_mid + int(np.ceil(b_dist / 2))
            a_min = a_mid - int(np.ceil(b_dist / 2))
            blob_image = np.zeros((a_max - a_min, b_max - b_min), 'uint8')
            start_point = blob_image.shape[0] // 2 - region.image.shape[0] // 2
            blob_image[start_point:start_point + region.image.shape[0], :] = region.image
            if any(np.array((a_min, b_min - 1, a_max, b_max + 1)) < 0):
                continue
        else:
            b_mid = (b_min + b_max) // 2
            b_max = b_mid + int(np.ceil(a_dist // 2))
            b_min = b_mid - int(np.ceil(a_dist // 2))
            blob_image = np.zeros((a_max - a_min, b_max - b_min), 'uint8')
            start_point = blob_image.shape[1] // 2 - region.image.shape[1] // 2
            blob_image[:, start_point:start_point + region.image.shape[1]] = region.image * 255
            if any(np.array((a_min - 1, b_min, a_max + 1, b_max)) < 0):
                continue
        blob_image = 255 - blob_image

        # Calculate the distance of the blob intensity centroid to the image center.
        wc_dist = np.linalg.norm(np.array(image.shape)/2 - region.weighted_centroid)

        # If the new bounding box is outside the image, skip it.
        if any(np.array((a_min, b_min, a_max, b_max)) < 0):
            continue

        # Potential blob.
        blobs.append((wc_dist, blob_image))

    blobs.sort(key=itemgetter(0))
    if len(blobs) == 0:
        return None
    b = [b for sol, b in blobs]
    if len(b[0]) == 0:
        return None
    return b[0]


def get_centered_blob(img, border_size=1):
    img = to_binary(img)
    blob = _get_most_centered_blob(img)
    if blob is None:
        return None
    blob_img = add_border(blob, (28, 28), border_size=border_size)
    blob_img = to_binary(blob_img)

    return blob_img

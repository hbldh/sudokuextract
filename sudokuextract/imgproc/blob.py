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

from operator import itemgetter, attrgetter

import numpy as np
from scipy import ndimage as ndi
from skimage.filters import gaussian_filter, threshold_adaptive
from skimage.measure import label
from skimage.measure import regionprops
from skimage.transform import resize
from skimage.morphology import binary_dilation

from sudokuextract.exceptions import SudokuExtractError
from sudokuextract.imgproc.binary import to_binary_otsu, add_border
from sudokuextract.imgproc.geometry import get_contours


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
        blobs.append((region.area, region.bbox))

    blobs.sort(key=itemgetter(0))
    return [img[b[0]:b[2], b[1]:b[3]] for sol, b in blobs[:n]]


def get_extremes_of_n_largest_blobs(image, n=5):
    original_shape = image.size
    if max(image.size) < 2000:
        size = (500, 500)
        y_scale = original_shape[0] / 500
        x_scale = original_shape[1] / 500
    else:
        size = (1000, 1000)
        y_scale = original_shape[0] / 1000
        x_scale = original_shape[1] / 1000

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
        coords = get_contours(add_border(label_image == region.label,
                                         size=label_image.shape,
                                         border_size=1,
                                         background_value=False))[0]
        coords = np.fliplr(coords)

        top_left = sorted(coords, key=lambda x: np.linalg.norm(np.array(x)))[0]
        top_right = sorted(coords, key=lambda x: np.linalg.norm(np.array(x) - [img.shape[1], 0]))[0]
        bottom_left = sorted(coords, key=lambda x: np.linalg.norm(np.array(x) - [0, img.shape[0]]))[0]
        bottom_right = sorted(coords, key=lambda x: np.linalg.norm(np.array(x) - [img.shape[1], img.shape[0]]))[0]

        blobs.append((region.filled_area, (top_left, top_right, bottom_left, bottom_right)))

    blobs.sort(key=itemgetter(0))
    output = []
    for blob in blobs[:n]:
        output.append([(int(x[0] * y_scale), int(x[1]*x_scale)) for x in blob[1]])
    return output


def iter_blob_contours(image):
    original_shape = image.size
    if max(image.size) < 2000:
        size = (500, 500)
        y_scale = original_shape[0] / 500
        x_scale = original_shape[1] / 500
    else:
        size = (1000, 1000)
        y_scale = original_shape[0] / 1000
        x_scale = original_shape[1] / 1000

    img = np.array(image.resize(size))
    bimg = gaussian_filter(img, sigma=1.0)
    bimg = threshold_adaptive(bimg, 20, offset=2/255)
    bimg = -bimg
    bimg = ndi.binary_fill_holes(bimg)
    label_image = label(bimg, background=False)
    label_image += 1

    regions = regionprops(label_image)
    regions.sort(key=attrgetter('area'), reverse=True)

    for region in regions:
        try:
            coords = get_contours(add_border(label_image == region.label,
                                             size=label_image.shape,
                                             border_size=1,
                                             background_value=False))[0]
            if np.linalg.norm(coords[0, :] - coords[-1, :]) > 1e-10:
                raise SudokuExtractError("Not a closed contour.")
            else:
                coords = np.fliplr(coords[:-1, :])

            top_left = sorted(coords, key=lambda x: np.linalg.norm(np.array(x)))[0]
            top_right = sorted(coords, key=lambda x: np.linalg.norm(np.array(x) - [img.shape[1], 0]))[0]
            bottom_left = sorted(coords, key=lambda x: np.linalg.norm(np.array(x) - [0, img.shape[0]]))[0]
            bottom_right = sorted(coords, key=lambda x: np.linalg.norm(np.array(x) - [img.shape[1], img.shape[0]]))[0]

            tl_i = np.argmax((coords == top_left).sum(axis=1))
            tr_i = np.argmax((coords == top_right).sum(axis=1))
            bl_i = np.argmax((coords == bottom_left).sum(axis=1))
            br_i = np.argmax((coords == bottom_right).sum(axis=1))

            coords[:, 0] *= y_scale
            coords[:, 1] *= x_scale

            if tl_i > bl_i:
                left_edge = coords[bl_i:tl_i + 1, :]
            else:
                coords_end_of_array = coords[bl_i:, :]
                coords_start_of_array = coords[:tl_i + 1]
                left_edge = np.concatenate([coords_end_of_array, coords_start_of_array], axis=0)

            if tr_i > tl_i:
                top_edge = coords[tl_i:tr_i + 1, :]
            else:
                coords_end_of_array = coords[tl_i:, :]
                coords_start_of_array = coords[:tr_i + 1]
                top_edge = np.concatenate([coords_end_of_array, coords_start_of_array], axis=0)

            if br_i > tr_i:
                right_edge = coords[tr_i:br_i + 1, :]
            else:
                coords_end_of_array = coords[tr_i:, :]
                coords_start_of_array = coords[:br_i + 1]
                right_edge = np.concatenate([coords_end_of_array, coords_start_of_array], axis=0)

            if bl_i > br_i:
                bottom_edge = coords[br_i:bl_i + 1, :]
            else:
                coords_end_of_array = coords[br_i:, :]
                coords_start_of_array = coords[:bl_i + 1]
                bottom_edge = np.concatenate([coords_end_of_array, coords_start_of_array], axis=0)

            yield left_edge, top_edge, right_edge, bottom_edge
        except Exception:
            pass
    raise SudokuExtractError("No suitable blob could be found.")


def blobify(images):
    output_data = []
    mask = []
    for d in images:
        blob = get_centered_blob(d)

        if blob is not None:
            output_data.append(blob)
            mask.append(True)
        else:
            mask.append(False)

    return output_data, np.array(mask)


def _get_most_centered_blob(image):
    # Label the binary image sent into connected black resp. white areas.
    label_image = label(image)
    blobs = []

    # If only one region, skip this image.
    if len(np.unique(label_image)) == 1:
        return None

    # Create intensity image.
    i_img = 255 - image
    i_img[i_img == 255] = 1

    for region in regionprops(label_image, i_img):
        # Test 1: If the region is too small to be interesting: skip it.
        if region.area < (np.prod(image.shape) * 0.015):
            continue

        # Test 2: If the region a white one: skip it.
        if region.max_intensity < 0.9:
            continue

        # Extract bounding box.
        a_min, b_min, a_max, b_max = region.bbox
        a_dist = a_max - a_min
        b_dist = b_max - b_min

        # Removed test 2.5 on disproportionate x to y dimensions.
        # if (np.min([a_dist, b_dist]) / np.max([a_dist, b_dist])) < 0.1:
        #     continue

        # Test 3: If the bounding box is larger than half of the image, check
        # whether or not the region's relative filled area is smaller than 0.5.
        # If so: skip it!
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
            blob_image[start_point:start_point + region.image.shape[0], :] = region.image.copy()
            if any(np.array((a_min, b_min - 1, a_max, b_max + 1)) < 0):
                continue
        else:
            try:
                b_mid = (b_min + b_max) // 2
                b_max = b_mid + int(np.ceil(a_dist / 2))
                b_min = b_mid - int(np.ceil(a_dist / 2))
                blob_image = np.zeros((a_max - a_min, b_max - b_min), 'uint8')
                start_point = blob_image.shape[1] // 2 - region.image.shape[1] // 2
                blob_image[:, start_point:start_point + region.image.shape[1]] = region.image.copy() * 255
                if any(np.array((a_min - 1, b_min, a_max + 1, b_max)) < 0):
                    continue
            except Exception as e:
                pass

        # Invert image to regain the original black/white status.
        blob_image = 255 - blob_image

        # Calculate the distance of the blob intensity centroid to the image center.
        wc_dist = np.linalg.norm(np.array(image.shape)/2 - region.weighted_centroid)

        # Test 4: If the blob is too off-center, skip it.
        if wc_dist > (image.shape[0] // 3):
            continue

        # Test 5: If the new bounding box is outside the image, skip it.
        if any(np.array((a_min, b_min, a_max, b_max)) < 0):
            continue

        # Potential blob.
        blobs.append((wc_dist, blob_image))

    blobs.sort(key=itemgetter(0))
    if len(blobs) == 0:
        return None
    blobs = [b for sol, b in blobs]

    if len(blobs[0]) == 0:
        return None
    for blob in blobs:
        m = blob.mean()
        # Test 6: If mean value of image is too white, it is probably only captured noise: skip it.
        if m > 230.0:
            continue
        # Test 7: If mean value of image is too black, it is probably only captured noise: skip it.
        elif m < 20.0:
            continue
        else:
            return blob
    return None


def get_centered_blob(img, border_size=1):
    img = to_binary_otsu(img)
    blob = _get_most_centered_blob(img)
    if blob is None:
        blob = _get_most_centered_blob(to_binary_otsu(binary_dilation(img)))
        if blob is None:
            return None
    blob_img = add_border(blob, (28, 28), border_size=border_size)
    blob_img = to_binary_otsu(blob_img)

    return blob_img

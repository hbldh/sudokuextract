#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`run`
==================

.. module:: run
    :platform: Unix, Windows
    :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@swedwise.com>

Created on 2016-01-14, 09:10

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np
import matplotlib.pyplot as plt

from skimage.filters import gaussian_filter, threshold_adaptive, threshold_otsu

from skimage import exposure
from skimage.morphology import disk
from skimage.filters import rank

from sudokuextract.data import img1, img2
from sudokuextract.imgproc.contour import get_contours
from sudokuextract.imgproc.sudoku import is_sudoku

img_one = img1().convert('L')#.resize((500, 500))
img_two = img2().convert('L').resize((500, 500))

img = np.array(img_one)

# Adaptive threshold
#img = exposure.equalize_hist(img)
binary_img = threshold_adaptive(img, block_size=40, offset=10)
# Get contours
contours = get_contours(binary_img)

sudokus = []
for c in contours:
    x_min, x_max = int(min(c[:, 0])), int(max(c[:, 0]))
    y_min, y_max = int(min(c[:, 1])), int(max(c[:, 1]))
    subimg = binary_img[x_min:x_max + 1, y_min:y_max+1]
    if is_sudoku(subimg):
       sudokus.append(subimg)

fig = plt.figure()
ax1 = plt.subplot(2, 2, 1, adjustable='box-forced')
ax2 = plt.subplot(2, 2, 2, sharex=ax1, sharey=ax1, adjustable='box-forced')
ax3 = plt.subplot(2, 2, 3, sharex=ax1, sharey=ax1, adjustable='box-forced')
ax4 = plt.subplot(2, 2, 4, sharex=ax1, sharey=ax1, adjustable='box-forced')

ax1.imshow(img, cmap=plt.cm.gray)
ax1.set_title('Original')
ax1.axis('off')

ax2.imshow(binary_img, cmap=plt.cm.gray)
ax2.set_title('Thresholded')
ax2.axis('off')




# ax4.imshow(image_label_overlay)
# for region in regionprops(label_image):
#
#     # skip small images
#     if region.area < 5000:
#         continue
#
#     # draw rectangle around segmented coins
#     minr, minc, maxr, maxc = region.bbox
#     rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
#                               fill=False, edgecolor='red', linewidth=2)
#     ax4.add_patch(rect)

plt.show()

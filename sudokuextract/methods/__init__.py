#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .corners import extraction_method_corners
from .map import extraction_method_map

extraction_methods = [
    lambda image, classifier: extraction_method_corners(
        image, classifier, use_local_thresholding=False, n=3),
    lambda image, classifier: extraction_method_corners(
        image, classifier, use_local_thresholding=True, n=3),
    lambda image, classifier: extraction_method_map(
        image, classifier, use_local_thresholding=False, n=3),
    lambda image, classifier: extraction_method_map(
        image, classifier, use_local_thresholding=True, n=3),
    lambda image, classifier: extraction_method_map(
        image, classifier, use_local_thresholding=False, apply_gaussian=True, n=3),
    lambda image, classifier: extraction_method_map(
        image, classifier, use_local_thresholding=True, apply_gaussian=True, n=3),
]


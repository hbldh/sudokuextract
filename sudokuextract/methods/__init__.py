#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .corners import extraction_method_corners
from .map import extraction_method_map

N = 1

extraction_methods = [
    ("Corners, local", lambda image, classifier: extraction_method_corners(
        image, classifier, use_local_thresholding=True, n=N)),
    ("Map, local", lambda image, classifier: extraction_method_map(
        image, classifier, use_local_thresholding=True, n=N)),
    ("Corners, adaptive", lambda image, classifier: extraction_method_corners(
        image, classifier, use_local_thresholding=False, n=N)),
    ("Map, adaptive", lambda image, classifier: extraction_method_map(
        image, classifier, use_local_thresholding=False, n=N)),
    ("Map, adaptive, Gaussian", lambda image, classifier: extraction_method_map(
        image, classifier, use_local_thresholding=False, apply_gaussian=True, n=N)),
    ("Corners, adaptive, Gaussian", lambda image, classifier: extraction_method_corners(
        image, classifier, use_local_thresholding=False, apply_gaussian=True, n=N)),
    ("Map, local, Gaussian", lambda image, classifier: extraction_method_map(
        image, classifier, use_local_thresholding=True, apply_gaussian=True, n=N)),
    ("Corners, adaptive, Gaussian", lambda image, classifier: extraction_method_corners(
        image, classifier, use_local_thresholding=True, apply_gaussian=True, n=N)),
]


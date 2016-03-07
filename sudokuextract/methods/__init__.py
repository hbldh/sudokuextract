#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from .corners import extraction_method_corners
from .map import extraction_method_map

N = 1

extraction_methods = [
    ("Corners, local", partial(extraction_method_corners, use_local_thresholding=True, n=N)),
    ("Map, local", partial(extraction_method_map, use_local_thresholding=True, n=N)),
    ("Corners, adaptive", partial(extraction_method_corners, use_local_thresholding=False, n=N)),
    ("Map, adaptive", partial(extraction_method_map, use_local_thresholding=False, n=N)),
    ("Map, adaptive, Gaussian", partial(extraction_method_map, use_local_thresholding=False, apply_gaussian=True, n=N)),
    ("Corners, adaptive, Gaussian", partial(extraction_method_corners, use_local_thresholding=False, apply_gaussian=True, n=N)),
    ("Map, local, Gaussian", partial(extraction_method_map, use_local_thresholding=True, apply_gaussian=True, n=N)),
    ("Corners, adaptive, Gaussian", partial(extraction_method_corners, use_local_thresholding=True, apply_gaussian=True, n=N)),
]


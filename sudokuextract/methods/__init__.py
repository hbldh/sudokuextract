#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from .map import extraction_method_map

N = 2

extraction_methods = [
    ("Map, local", partial(extraction_method_map, use_local_thresholding=True, n=N)),
    ("Map, adaptive", partial(extraction_method_map, use_local_thresholding=False, n=N)),
    ("Map, adaptive, Gaussian", partial(extraction_method_map, use_local_thresholding=False, apply_gaussian=True, n=N)),
    ("Map, local, Gaussian", partial(extraction_method_map, use_local_thresholding=True, apply_gaussian=True, n=N)),
]


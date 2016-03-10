# -*- coding: utf-8 -*-
"""Release data for the SudokuExtract project."""

# -----------------------------------------------------------------------------
#  Copyright (c) 2015, Nedomkull Mathematical Modeling AB.
# -----------------------------------------------------------------------------

__author__ = 'Henrik Blidh'
__author_email__ = 'henrik.blidh@nedomkull.com'
__maintainer__ = 'Henrik Blidh'
__maintainer_email__ = 'henrik.blidh@nedomkull.com'
__license__ = 'MIT'
__description__ = "Library for extracting Sudokus from images using scikit-image"
__url__ = 'https://github.com/hbldh/sudokuextract'
__platforms__ = 'any'
_keywords__ = ['Image Processing', 'Sudoku']
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development',
    'Topic :: Scientific/Engineering',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]


# Version information.  An empty _version_extra corresponds to a full
# release.  'dev' as a _version_extra string means this is a development
# version.
_version_major = 0
_version_minor = 8
_version_patch = 4
# _version_extra = '.dev2'
# _version_extra = 'rc1'
_version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor, _version_patch]

__version__ = '.'.join(map(str, _ver))
if _version_extra:
    __version__ += _version_extra

version = __version__  # backwards compatibility name
version_info = (_version_major, _version_minor, _version_patch, _version_extra)

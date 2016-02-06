# -*- coding: utf-8 -*-
"""Release data for the SudokuExtract project."""

# -----------------------------------------------------------------------------
#  Copyright (c) 2015, Nedomkull Mathematical Modeling AB.
# -----------------------------------------------------------------------------

author = 'Henrik Blidh'
author_email = 'henrik.blidh@nedomkull.com'
maintainer = 'Henrik Blidh'
maintainer_email = 'henrik.blidh@nedomkull.com'
license = 'MIT'
description = "Library for extracting Sudokus from images using scikit-image"
url = 'https://bitbucket.org/nedomkull/sudokuextract'
download_url = 'https://bitbucket.org/nedomkull/sudokuextract'
platforms = ['Linux', 'Mac OSX', 'Windows XP/Vista/7/8']
keywords = ['Image Processing', 'Sudoku']
classifiers = [
                  'Development Status :: 3 - Alpha',
                  'Intended Audience :: Science/Research',
                  'Intended Audience :: Developers',
                  'License :: MIT',
                  'Topic :: Software Development',
                  'Topic :: Scientific/Engineering',
                  'Operating System :: Microsoft :: Windows',
                  'Operating System :: POSIX',
                  'Operating System :: Unix',
                  'Operating System :: MacOS',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 2',
                  'Programming Language :: Python :: 2.6',
                  'Programming Language :: Python :: 2.7',
                  'Programming Language :: Python :: 3',
                  'Programming Language :: Python :: 3.3',
                  'Programming Language :: Python :: 3.4',
                  'Programming Language :: Python :: 3.5',
              ],


# Version information.  An empty _version_extra corresponds to a full
# release.  'dev' as a _version_extra string means this is a development
# version.
_version_major = 0
_version_minor = 3
_version_patch = 0
#_version_extra = '.dev1'
_version_extra = 'b1'
# _version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor, _version_patch]

__version__ = '.'.join(map(str, _ver))
if _version_extra:
    __version__ += _version_extra

version = __version__  # backwards compatibility name
version_info = (_version_major, _version_minor, _version_patch, _version_extra)

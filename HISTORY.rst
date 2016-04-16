v0.8.6 (2016-04-16)
===================
- Changed the main function of `sudokuextract.extract` to print and
  not return anything.

v0.8.5 (2016-03-10)
===================
- Replace ndi.binary_fill_holes with a binary_erosion and increased number of blobs to test to 2.

v0.8.4 (2016-03-10)
===================
- New classifiers.
- New data with additional data of 1:s.

v0.8.3 (2016-03-09)
===================
- Disabled the Corners parsing solution again.
- Warping image now creates a much smaller image to prevent memory issues.
- This also increased speed with a factor of at least 4.
- ``apply_gaussian`` now applies a Gaussian on entire image first.
- Testing can now use a tar-file of images that can be downloaded from the web.
- Also removed lambda functions in favour of ``functools.partial``.

v0.8.2 (2016-03-07)
===================
- Restricted scikit-image version to < 0.12.

v0.8.1 (2016-03-06)
===================
- New classifiers with both SudokuExtract and MNIST data.
- New data.
- MNIST data stored separately from SudokuExtract data.
- Number of Nearest Neighbours increased to 10 due to larger training data.
- Several small bugfixes for new features added in v0.8.0.

v0.8.0 (2016-03-05)
===================
- New classifiers with MNIST data.
- New multi-attempt approach to Sudoku parsing.
- Using DLXSudoku to attempt classification of correct parsing of Sudoku.
- Removed a lot of deprecated code.

v0.7.0 (2016-02-26)
===================
- Two different extraction methods:
    * Local thresholding
    * Adaptive thresholding for entire image
- Refactored extensively and updated classifiers.

v0.6.1 (2016-02-20)
===================
- Patch for tests in Python 3.

v0.6.0 (2016-02-19)
===================
- Simplified blob extraction.
- Added adaptive block_size for ``to_binary_adaptive``.
- Added tests that fetch Sudokus from Xanadoku.

v0.5.0 (2016-02-18)
===================
- Removed hard dependency on scikit-learn.
- Included an own K-Nearest-Neighbors classifier as default.

v0.4.0 (2016-02-17)
===================
- Initial release on PyPI


SudokuExtract
=============

.. image:: https://travis-ci.org/hbldh/sudokuextract.svg?branch=master
    :target: https://travis-ci.org/hbldh/sudokuextract
.. image:: http://img.shields.io/pypi/v/sudokuextract.svg
    :target: https://pypi.python.org/pypi/sudokuextract/
.. image:: http://img.shields.io/pypi/dm/sudokuextract.svg
    :target: https://pypi.python.org/pypi/sudokuextract/
.. image:: http://img.shields.io/pypi/l/sudokuextract.svg
    :target: https://pypi.python.org/pypi/sudokuextract/
.. image:: https://coveralls.io/repos/github/hbldh/sudokuextract/badge.svg?branch=master
    :target: https://coveralls.io/github/hbldh/sudokuextract?branch=master

Library for extracting Sudokus from images using `scikit-image <http://scikit-image.org/>`_.

Requirements
------------

* ``numpy>=1.9.2``
* ``scipy>=0.15.1``
* ``scikit-image<0.12.0``
* ``Pillow>=3.1.0``
* ``pyefd>=0.1.2``
* ``dlxsudoku>=0.10.0``

Usage
-----

Install via `pip`::

    $ pip install sudokuextract

SudokuExtract is a tool for parsing Sudokus from images, this primarily
to be able to send it forward to some kind of solver. It applies some
image analysis on the input image and then uses a K-Nearest Neighbours
classifier to determine which digits that are present in which box.

``SudokuExtract`` can be used as a command line tool::

    parse-sudoku -p /path/to/sudoku_image.jpg

which prints the parsed Sudoku in the terminal. In can also be called
with an url to an image::

    parse-sudoku -u http://www.domain.com/sudoku.jpg

It can also be used as a regular Python package::

    In [1]: from sudokuextract.extract import extract_sudoku, load_image, predictions_to_suduko_string

    In [2]: img = load_image('/path/to/sudoku_image.jpg')

    In [3]: predictions, sudoku_box_images, whole_sudoku_image = extract_sudoku(img)

    In [4]: print(predictions_to_suduko_string(predictions))
    800603001
    057401630
    000000000
    006109800
    400000007
    001805400
    000000000
    072504310
    900302004

There are possibilities of using a classifier of your own creation when
predicting digits; see the documentation for more details.

Testing
-------

Run tests with `pytest <http://pytest.org/>`_::

    $ py.test tests.py


Documentation
-------------

TBD.

References
----------

This library includes classifiers trained with data from the MNIST dataset
(This data is also included in SudokuExtract).

.. _1:

\[1\] `LeCun et al. (1999): The MNIST Dataset Of Handwritten Digits <http://yann.lecun.com/exdb/mnist/>`_

The current parsing strategy for the `sudokuextract` package is
inspired by this blog entry:

.. _2:

\[2\] `AI: SuDoKu Grabber with OpenCV <http://aishack.in/tutorials/sudoku-grabber-opencv-plot/>`_

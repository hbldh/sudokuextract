#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import struct
import gzip
import itertools
from pkg_resources import resource_filename, resource_exists

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    _range = xrange
except NameError:
    _range = range

import numpy as np
from PIL import Image

from sudokuextract.methods.map import _extraction_iterator_map
from sudokuextract.ml.features import extract_efd_features
from sudokuextract.imgproc.blob import blobify
from sudokuextract.utils import download_image

_url_to_mnist_train_data = "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"
_url_to_mnist_train_labels = "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"


def _toS32(bits):
    return struct.unpack_from(">i", bits)[0]


def get_mnist_raw_data():
    X, y = _mnist_raw_data(), _mnist_raw_labels()
    for k in _range(len(X)):
        X[k] = 255 - X[k]

    return X, y


def _mnist_raw_data():
    fname = resource_filename('sudokuextract.data', "train-images-idx3-ubyte.gz")
    if resource_exists('sudokuextract.data', "train-images-idx3-ubyte.gz"):
        f = gzip.open(fname, mode='rb')
        data = f.read()
        f.close()
    else:
        sio = StringIO(urlopen(_url_to_mnist_train_data).read())
        sio.seek(0)
        f = gzip.GzipFile(fileobj=sio, mode='rb')
        data = f.read()
        f.close()
        try:
            sio.seek(0)
            with open(fname, 'wb') as f:
                f.write(sio.read())
        except:
            pass

    correct_magic_number = 2051
    magic_number = _toS32(data[:4])
    if magic_number != correct_magic_number:
        raise ValueError("Error parsing images file. Read magic number {0} != {1}!".format(
            magic_number, correct_magic_number))
    n_images = _toS32(data[4:8])
    n_rows = _toS32(data[8:12])
    n_cols = _toS32(data[12:16])
    images = np.fromstring(data[16:], 'uint8').reshape(n_images, n_rows*n_cols)

    return [imrow.reshape(28, 28) for imrow in images]


def _mnist_raw_labels():
    fname = resource_filename('sudokuextract.data', "train-labels-idx1-ubyte.gz")
    if resource_exists('sudokuextract.data', "train-labels-idx1-ubyte.gz"):
        f = gzip.open(fname, mode='rb')
        data = f.read()
        f.close()
    else:
        sio = StringIO(urlopen(_url_to_mnist_train_labels).read())
        sio.seek(0)
        f = gzip.GzipFile(fileobj=sio, mode='rb')
        data = f.read()
        f.close()
        try:
            sio.seek(0)
            with open(fname, 'wb') as f:
                f.write(sio.read())
        except:
            pass

    correct_magic_number = 2049
    magic_number = _toS32(data[:4])
    if magic_number != correct_magic_number:
        raise ValueError("Error parsing labels file. Read magic number {0} != {1}!".format(
            magic_number, correct_magic_number))
    n_labels = _toS32(data[4:8])
    return np.fromstring(data[8:], 'uint8')


def get_sudokuextract_data():
    return _sudokuextract_data(), _sudokuextract_labels()


def _sudokuextract_data():
    fname = resource_filename('sudokuextract.data', "se-train-data.gz")
    if resource_exists('sudokuextract.data', "se-train-data.gz"):
        f = gzip.open(fname, mode='rb')
        data = np.load(f)
        f.close()
    else:
        raise IOError("SudokuExtract Training data file was not present!")

    return data


def _sudokuextract_labels():
    fname = resource_filename('sudokuextract.data', "se-train-labels.gz")
    if resource_exists('sudokuextract.data', "se-train-labels.gz"):
        f = gzip.open(fname, mode='rb')
        data = np.load(f)
        f.close()
    else:
        raise IOError("SudokuExtract Training labels file was not present!")

    return data


def get_mnist_data():
    return _mnist_data(), _mnist_labels()


def _mnist_data():
    fname = resource_filename('sudokuextract.data', "mnist-train-data.gz")
    if resource_exists('sudokuextract.data', "mnist-train-data.gz"):
        f = gzip.open(fname, mode='rb')
        data = np.load(f)
        f.close()
    else:
        raise IOError("MNIST Training data file was not present!")

    return data


def _mnist_labels():
    fname = resource_filename('sudokuextract.data', "mnist-train-labels.gz")
    if resource_exists('sudokuextract.data', "mnist-train-labels.gz"):
        f = gzip.open(fname, mode='rb')
        data = np.load(f)
        f.close()
    else:
        raise IOError("MNIST Training labels file was not present!")

    return data


def create_data_set_from_images(path_to_data_dir):

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("This method requires matplotlib installed...")
        return

    images = []
    labels = []
    path_to_data_dir = os.path.abspath(os.path.expanduser(path_to_data_dir))
    _, _, files = next(os.walk(path_to_data_dir))
    for f in files:
        file_name, file_ext = os.path.splitext(f)
        if file_ext in ('.jpg', '.png', '.bmp') and "{0}.txt".format(file_name) in files:
            # The current file is an image and it has a corresponding text file as reference.
            # Use it as data.
            print("Handling {0}...".format(f))
            image = Image.open(os.path.join(path_to_data_dir, f))
            with open(os.path.join(path_to_data_dir, "{0}.txt".format(file_name)), 'rt') as f:
                parsed_img = f.read().strip().split('\n')
            for sudoku, subimage in _extraction_iterator_map(image):
                for k in range(len(sudoku)):
                    for kk in range(len(sudoku[k])):
                        ax = plt.subplot2grid((9, 9), (k, kk))
                        ax.imshow(sudoku[k][kk], plt.cm.gray)
                        ax.set_title(str(parsed_img[k][kk]))
                        ax.axis('off')
                plt.show()
                ok = raw_input("Is this OK (y/N/a)? ")
                if ok == 'y':
                    for k in range(len(sudoku)):
                        for kk in range(len(sudoku[k])):
                            images.append(sudoku[k][kk].copy())
                            labels.append(int(parsed_img[k][kk]))
                    break
                if ok == 'a':
                    break
            for sudoku, subimage in _extraction_iterator_map(image, use_local_thresholding=True):
                for k in range(len(sudoku)):
                    for kk in range(len(sudoku[k])):
                        ax = plt.subplot2grid((9, 9), (k, kk))
                        ax.imshow(sudoku[k][kk], plt.cm.gray)
                        ax.set_title(str(parsed_img[k][kk]))
                        ax.axis('off')
                plt.show()
                ok = raw_input("Is this OK (y/N/a)? ")
                if ok == 'y':
                    for k in range(len(sudoku)):
                        for kk in range(len(sudoku[k])):
                            images.append(sudoku[k][kk].copy())
                            labels.append(int(parsed_img[k][kk]))
                    break
                if ok == 'a':
                    break

    try:
        os.makedirs(os.path.expanduser('~/sudokuextract'))
    except:
        pass

    try:
        for i, (img, lbl) in enumerate(zip(images, labels)):
            img = Image.fromarray(img, 'L')
            with open(os.path.expanduser('~/sudokuextract/{1}_{0:04d}.jpg'.format(i+1, lbl)), 'w') as f:
                img.save(f)
    except Exception as e:
        print(e)

    print("Pre-blobify:  Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(labels))]))
    y = np.array(labels, 'int8')
    images, mask = blobify(images)
    y = y[mask]
    print("Post-blobify:  Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))

    print("Extract features...")
    X = np.array([extract_efd_features(img) for img in images])

    return images, labels, X, y


def create_mnist_dataset():
    images, labels = get_mnist_raw_data()
    mask = labels != 0
    print("Pre-zero removal:  Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(labels))]))
    images = list(itertools.compress(images, mask))
    labels = labels[mask]

    images = images[3::20]
    labels = labels[3::20]

    print("Pre-blobify:  Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(labels))]))
    y = np.array(labels, 'int8')
    images, mask = blobify(images)
    y = y[mask]
    print("Post-blobify:  Label / N : {0}".format([(v, c) for v, c in zip(_range(10), np.bincount(y))]))

    print("Extract features...")
    X = np.array([extract_efd_features(img) for img in images])

    try:
        os.makedirs(os.path.expanduser('~/sudokuextract'))
    except:
        pass

    try:
        for i, (img, lbl) in enumerate(zip(images, labels)):
            img = Image.fromarray(img, 'L')
            with open(os.path.expanduser('~/sudokuextract/{1}_{0:04d}.jpg'.format(i + 1, lbl)), 'w') as f:
                img.save(f)
    except Exception as e:
        print(e)

    return images, labels, X, y


def save_training_data(X, y, data_source='se'):
    _save_data('train', X, y, data_source)


def save_test_data(X, y, data_source='se'):
    _save_data('test', X, y, data_source)


def _save_data(which, X, y, data_source):
    if data_source.lower() == 'mnist':
        data_source = 'mnist'
    else:
        data_source = 'se'

    if X.shape[0] != len(y):
        raise TypeError("Length of data samples ({0}) was not identical "
                        "to length of labels ({1})".format(X.shape[0], len(y)))

    # Convert to numpy array.
    if not isinstance(X, np.ndarray):
        X = np.array(X)
    if not isinstance(y, np.ndarray):
        y = np.array(y)

    # Write feature_data
    fname = resource_filename('sudokuextract.data', "{0}-{1}-data.gz".format(data_source, which))
    with gzip.GzipFile(fname, mode='wb') as f:
        np.save(f, X)

    # Write labels
    fname = resource_filename('sudokuextract.data', "{0}-{1}-labels.gz".format(data_source, which))
    with gzip.GzipFile(fname, mode='wb') as f:
        np.save(f, y)


def fetch_all_xanadoku_images(folder_to_store_in, api_token):
    import json
    doc = json.loads(urlopen("https://xanadoku.herokuapp.com/getallsudokus/{0}".format(
        api_token)).read().decode('utf8'))
    for d in doc.get('sudokus'):
        if not d.get('verified'):
            continue
        print("Saving {0}...".format(d.get('_id')))
        img = download_image(d.get('raw_image_url'))
        with open(os.path.join(os.path.abspath(os.path.expanduser(
                folder_to_store_in)), d.get('_id') + '.jpg'), 'w') as f:
            img.save(f)
        with open(os.path.join(os.path.abspath(os.path.expanduser(
                folder_to_store_in)), d.get('_id') + '.txt'), 'w') as f:
            f.writelines([d.get('parsed_sudoku')[i:i+9] + '\n' for i in range(0, len(d.get('parsed_sudoku')), 9)])


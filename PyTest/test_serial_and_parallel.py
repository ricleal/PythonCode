# pylint: disable=redefined-outer-name, pointless-string-statement

import pytest

'''
Run as:
pytest-3 -vs test_serial_and_parallel.py
Or a single test:
pytest-3 -vs test_serial_and_parallel.py::test_parallel
'''


@pytest.fixture
def data():
    return range(20)


def square(x):
    return x**2


def test_serial(data):
    res = [square(d) for d in data]
    assert res == [0,   1,   4,   9,  16,  25,  36,  49,  64,  81, 100, 121,
                   144, 169, 196, 225, 256, 289, 324, 361]


def test_parallel(data):
    import multiprocessing
    with multiprocessing.Pool(processes=2) as pool:
        res = pool.map(square, data)

    assert res == [0,   1,   4,   9,  16,  25,  36,  49,  64,  81, 100, 121,
                   144, 169, 196, 225, 256, 289, 324, 361]

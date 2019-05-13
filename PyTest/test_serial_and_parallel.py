# pylint: disable=redefined-outer-name, pointless-string-statement, unused-argument

import pytest

'''
Run as:
pytest-3 -vs test_serial_and_parallel.py
Or a single test:
pytest-3 -vs test_serial_and_parallel.py::test_parallel
'''


@pytest.fixture(autouse=True)
def setup_and_teardown():
    '''
    By declaring your fixture with autouse=True, it will be automatically
    invoked for each test function defined in the same module.
    '''
    # Code that will run before your test, for example:
    print("\n** Before the test!")

    # A test function will be run at this point
    yield

    # Code that will run after your test, for example:
    print("\n** After the test!")


@pytest.fixture
def data():
    return range(20)


def square(x):
    return x**2


def test_serial(data, setup_and_teardown):
    res = [square(d) for d in data]
    assert res == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81,
                   100, 121, 144, 169, 196, 225, 256, 289, 324, 361]


def test_parallel(data, setup_and_teardown):
    import multiprocessing
    with multiprocessing.Pool(processes=2) as pool:
        res = pool.map(square, data)

    assert res == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81,
                   100, 121, 144, 169, 196, 225, 256, 289, 324, 361]


from my_module import MyClass
import pytest

'''
Run with `-b` to see the IDs:
pytest -v PyTest/test_parametrize.py
'''


testdata = [
    (1, 2), (3, 4), (10, 11),
    pytest.param(5, 5, marks=pytest.mark.xfail)
]


@pytest.mark.parametrize("input_arg, expected", testdata,
                         ids=["add1", "add3", "add10", "fail"])
def test_add10(input_arg, expected):
    assert MyClass.add1(input_arg) == expected

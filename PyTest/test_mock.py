
from my_module import MyClass
import pytest
#from pytest_mock import mocker


@pytest.fixture
def my_class():
    return MyClass()


def test_long_function(my_class, mocker):
    mocker.patch.object(my_class, 'long_function')
    my_class.long_function.return_value = False
    assert not my_class.long_function(1)


def test_get_content(my_class, mocker):
    mocker.patch.object(my_class, 'get_content')
    my_class.get_content.return_value = dict(ok=True, status_code=200)
    url = "this.doesnt.exist.url"
    ret = my_class.get_content(url)
    my_class.get_content.assert_called_with(url)
    assert ret['ok']
    assert ret['status_code'] == 200

import requests
import time


'''
# run as:
pytest -vs test_mock.py
'''


class MyClass():

    def long_function(self, attr_a):
        print(attr_a)
        time.sleep(2)
        return False

    def get_content(url):
        response = requests.get(url)
        return dict(ok=response.ok, status_code=response.status_code)

    @staticmethod
    def add1(x):
        return x+1

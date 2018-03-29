from __future__ import print_function


class MyClass(object):

    p = None

    def __init__(self, p):
        self._p = p

    def __repr__(self):
        return "MyClass.p = {}".format(self._p)

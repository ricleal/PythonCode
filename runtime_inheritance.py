from pprint import pprint

class Base1(object):

    def hello(self):
        print('Hello from Base1')

class Base2(object):
    def ola(self):
        print('Ola da Base2')

class Dummy(object):
    def __init__(self):
        print('Creating instance of {}'.format(self.__class__.__name__))
    def f():
        print('FF')
    @classmethod
    def classmethod(cls, otherclass):
        #cls.__bases__ = (otherclass,) + cls.__bases__
        cls = type('Dummy', (otherclass,), dict(Dummy.__dict__))




b1 = Base1()
d = Dummy()

Dummy.classmethod(Base1)
d1 = Dummy()
d1.hello()
d.hello()

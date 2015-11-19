#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage of Meta class
RegistryMeta keeps track of the inherited classes
Base can work as factory.
'''

import abc

# I could inherited from (type) as well...
class RegistryMeta(abc.ABCMeta):
    # we use __init__ rather than __new__ here because we want
    # to modify attributes of the class *after* they have been
    # created

    def __init__(cls, name, bases, dct):
        print "Init for RegistryMeta: %s" % name
        if not hasattr(cls, 'registry'):
            # this is the base class.  Create an empty registry
            cls.registry = {}
        else:
            # this is a derived class.  Add cls to the registry
            interface_id = name.lower()
            cls.registry[interface_id] = cls
        super(RegistryMeta, cls).__init__(name, bases, dct)


class Base(object):
    __metaclass__ = RegistryMeta

    def __init__(self):
        print "Some Super initialisation..."

    @abc.abstractmethod
    def func(self):
        pass


class ChildA(Base):

    def __init__(self):
        #super(ChildA, self).__init__()
        Base.__init__(self)
        print 'Init for Category A'

    def func(self):
        print 'func for Category A'


class ChildB(Base):

    def __init__(self):
        #super(ChildB, self).__init__()
        Base.__init__(self)
        print 'Init for Category B'

    def func(self):
        print 'func for Category B'


if __name__ == '__main__':
    print 'Start...'
    print Base.registry
    a1 = ChildA()
    a1.func()
    a2 = Base.registry['childa']()
    a2.func()
    ##
    b1 = ChildB()
    b1.func()
    b2 = Base.registry['childb']()
    b2.func()
    print 'End!'

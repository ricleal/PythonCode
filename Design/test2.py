#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Sort of factory with manual registration.

Registrar dictionary has pairs <name,class>

'''

import abc

class Base(object):
    __metaclass__  = abc.ABCMeta

    def __init__(self):
        print "Some Super initialisation..."

    @abc.abstractmethod
    def func(self):
         pass


class ChildA(Base):

    def __init__(self):
        super(ChildA, self).__init__()
        print 'Init for Category A'

    def func(self):
        print 'func for Category A'

class ChildB(Base):

    def __init__(self):
        super(ChildB, self).__init__()
        print 'Init for Category B'

    def func(self):
        print 'func for Category B'

# Manual registration
Registrar = {'a': ChildA, 'b': ChildB}


if __name__ == '__main__':
    '''
    Output:
    Some Super initialisation...
    Init for Category A
    func for Category A
    Some Super initialisation...
    Init for Category B
    func for Category B
    '''
    a = Registrar['a']()
    a.func()

    b = Registrar['b']()
    b.func()

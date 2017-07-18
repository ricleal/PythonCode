#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Sort of factory with Auto registration through a register decorator

'''


import abc

# Auto registry
registry = {}

def register( cls ):
   registry[cls.__name__] = cls
   return cls


class Base(object):
    __metaclass__  = abc.ABCMeta

    def __init__(self):
        print "Some Super initialisation..."

    @abc.abstractmethod
    def func(self):
         pass


@register
class ChildA(Base):

    def __init__(self):
        #super(ChildA, self).__init__()
        Base.__init__(self)
        print 'Init for Category A'

    def func(self):
        print 'func for Category A'
@register
class ChildB(Base):

    def __init__(self):
        #super(ChildB, self).__init__()
        Base.__init__(self)
        print 'Init for Category B'

    def func(self):
        print 'func for Category B'


if __name__ == '__main__':
    '''
    Output:
    Start...
    Some Super initialisation...
    Init for Category A
    func for Category A
    Some Super initialisation...
    Init for Category B
    func for Category B
    End!
    '''
    print 'Start...'
    a = registry['ChildA']()
    a.func()
    b = registry['ChildB']()
    b.func()
    print 'End!'

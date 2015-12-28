'''
Created on Aug 5, 2013

@author: leal
'''

import inspect
from pprint import pprint

var_global = 10

class C():
    '''
    classdocs
    '''
    var_class = None

    def __init__(self):
        '''
        Constructor
        '''
        self.var_init = 0

    def print_class_attributes(self):
        attrs = dir(self)
        print attrs

    def print_class_variables(self):
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        pairs = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        pprint(pairs)


if __name__ == '__main__':
    c = C()
    c.print_class_attributes()
    c.print_class_variables()

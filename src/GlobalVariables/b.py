'''
Created on Aug 5, 2013

@author: leal
'''

import a;

myb = None

class B():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        global myb
        myb = a.mya
    
    def __str__(self):
        myb

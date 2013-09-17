'''
Created on Aug 5, 2013

@author: leal
'''

import a
import b

if __name__ == '__main__':
    thisa = a.A(11)
    print a.mya
    
    thisb = b.B()
    print b.myb
    a.mya = 2
    print b.myb
    b.myb = 3
    print a.mya
    print b.myb
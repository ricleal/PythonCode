'''
Created on Sep 12, 2013

@author: leal
'''

class C(object):
    def __init__(self):
        self._p = 10
    
    @property
    def p(self):
        return self._p
    
    @p.setter
    def p(self, val):
        self._p = val
    
    @p.deleter
    def p(self):  
        del self._p

if __name__ == '__main__':
    c = C()
    print c.p
    c.p = 20
    print c.p
    del c.p
    try:
        print c.p
    except:
        print "Property p does not exist!"
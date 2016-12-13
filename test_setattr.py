'''
Created on Aug 25, 2016

@author: rhf
'''
from pprint import pprint 

class T(object):
    def __init__(self):            
        pass
                               

if __name__ == '__main__':
    t = T()
    setattr(t, "a1", 123)
    setattr(t, "a2", 123)
    setattr(t, "a3", {"x" : 123})
    pprint(t.a3)
    t.a3.update({"y" : 123})
    #pprint(dir(t))
    pprint(t.a3)
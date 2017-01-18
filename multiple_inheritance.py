'''
Created on Jan 9, 2017

@author: rhf
'''

class A1(object):
    def __init__(self, *args, **kwargs):
        print("A1")
    
class A2(object):
    def __init__(self, *args, **kwargs):
        print("A2")
    
class B(A1,A2):
    def __init__(self, *args, **kwargs):
        print("Super")
        super(B, self).__init__(*args, **kwargs)
        print("A1:")
        A1.__init__(self,*args, **kwargs)
        print("A2:")
        A2.__init__(self,*args, **kwargs)

    

if __name__ == '__main__':
    b = B()
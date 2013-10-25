'''
Created on Jul 17, 2012

@author: leal
'''

class Dummy(object):
    '''
    classdocs
    '''


    def __init__(self,name):
        '''
        Constructor
        '''
        self.name = name
    
    def getName(self):
        return self.name
    
    def fib(self,n):
        '''
        Fibonacci numbers 
        '''
        
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n-1) + self.fib(n-2)
    
    def factorial(self,n):
        return reduce(lambda x,y:x*y,range(1,n+1))
    

if __name__ == "__main__":
    d = Dummy('Dummy Class')
    print 'Class name: ', d.getName()
    print 'Fibonacci of 10 = ', d.fib(10)
    print 'Factorial 10 = ', d.factorial(10)
    
    
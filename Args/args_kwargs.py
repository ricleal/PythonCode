# -*- coding: utf-8 -*-

'''

*args and **kwargs example

use *args when you're not sure how many arguments might be passed to your function

**kwargs allows you to handle named arguments that you have not defined in advance

'''

# Let's define the args for testing
args = [4,5,6]
kwargs = {'a':5,'b':10,'c':15}

##

def print_args(*args):
    '''
    Function that receives args and print args
    '''
    for arg in args:
        print "Arg:", arg

print_args(1,2,3)
print_args('a','b','c')
print_args(*args)
print 80*'*'

def print_kwargs(**kwargs):
    '''
    Function that receives kwargs and print kwargs
    '''
    for key, value in kwargs.items():
        print "KwArg:", key, "=", value

print_kwargs(a=1,b=2,c=3)
print_kwargs(**kwargs)
print 80*'*'

def print_args_kwargs(*args, **kwargs):
    '''
    Function that receives args and kwargs and print args and kwargs
    '''
    for arg in args:
        print "Arg:", arg
    for key, value in kwargs.items():
        print "KwArg:", key, "=", value

print_args_kwargs(1,2,a=3,b=4)
print_args_kwargs(*args,**kwargs)

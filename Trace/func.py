from __future__ import print_function
import sys


def trace_func(frame, event, arg):
    '''Prints a function call, arguments and return value.

    Use as:
    -------

    sys.settrace(trace_func)
    my_func(1,2)
    sys.settrace(None)

    '''

    if event == "call":
        print("{0}(".format(frame.f_code.co_name), end="")
        for i in range(frame.f_code.co_argcount):
            name = frame.f_code.co_varnames[i]
            print("{0}={1}, ".format(name, frame.f_locals[name]), end="")
        print(")\n")

    elif event == "return":
        if arg is not None:
            print("Return: {} -> {}".format(frame.f_code.co_name, arg))
    return trace_func


def my_func(a, b, c=4, d=5):
    print("*** Function called: {}".format([a, b, c, d]))
    return "puff"


sys.settrace(trace_func)
my_func(1, 2)
sys.settrace(None)

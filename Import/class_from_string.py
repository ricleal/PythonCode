from __future__ import print_function

import importlib


m = importlib.import_module('module.package')
MyClass = getattr(m, "MyClass")

m = MyClass(1)
print(m)

# OR:


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

MyClass = import_from("module.package", "MyClass")

m = MyClass(2)
print(m)
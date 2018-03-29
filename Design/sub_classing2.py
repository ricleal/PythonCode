class MyClass(object):
     def __new__(cls, x, y, z):
         print("constructing instance with arguments:")
         print("    ", cls, x, y, z)
         instance = super().__new__(cls, x, y, z)
         return instance
     def __init__(self, a, b, c):
         print("initializing instance with arguments:")
         print("    ", self, a, b, c)
         self.a = a
         self.b = b
         self.c = c

inst = MyClass(23, 42, 'spam')
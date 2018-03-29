
def call_subclass(some_function):

    def wrapper(*args, **kwargs):
        v = args[0]  # self
        this_class = globals()[type(v).__name__]
        for subclass in this_class.__subclasses__():
            v.__class__ = subclass
            method_to_call = getattr(v, some_function.__name__)
            method_to_call(*tuple(args[1:]), **kwargs)
            return
        some_function(*args, **kwargs)

    return wrapper


class Base(object):

    def __init__(self):
        print("Base init")

    @call_subclass
    def method(self):
        print("Base method")


class A(Base):

    def __init__(self):
        print("A init")

    def method(self):
        print("A method")


b = Base()
b.method()


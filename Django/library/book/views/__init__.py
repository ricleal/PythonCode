from django.views.generic.list import ListView
from django.utils import timezone
from django.utils.decorators import classonlymethod

def import_from(module, name):
    '''
    MyClass = import_from("module.package", "MyClass")
    object = MyClass()
    '''
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def generic_list(request, *args, **kwargs):
    argument = kwargs['argument']

    Class = import_from("book.views." + argument + ".views", "ListView")

    print("******* {}".format(Class))
    print("* This class args: {}".format(args))
    print("* This class kwargs: {}".format(kwargs))
    view = Class.as_view()(request, *args, **kwargs)
    return view
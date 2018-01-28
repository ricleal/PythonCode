from pprint import pformat

'''
Run as:
python3 object_view.py -v
'''

class DictAsObj(object):
    '''
    >>> DictAsObj({'a': 1, 'b': 2})
    {'a': 1, 'b': 2}

    >>> DictAsObj(a=1, b=2)
    {'a': 1, 'b': 2}
    '''
    def __init__(self, *args, **kwargs):
        d = dict(*args, **kwargs)
        self.__dict__ = d

    def __repr__(self):
        return "{}".format(pformat(self.__dict__))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
import os

from abc import ABC
from pprint import pformat, pprint


class Catalog(ABC):
    '''
    The main methods to be defined in the subclasses are here.
    '''

    def __new__(cls, *args, **kwargs):
        '''
        This allows to great subclasses from this base class,
        given a facility name

        The Catalog should be constructed like this:
        cat = Catalog(Facility)
        Where facility is the name of the classes below
        '''
        facility = kwargs.get('facility')
        technique = kwargs.get('technique')
        instrument = kwargs.get('instrument')


        for subclass in Catalog.subclasses(Catalog):
            if str(subclass.__name__) == facility:
                return super(cls, subclass).__new__(subclass)
        raise Exception('Facility not supported!')

    @staticmethod
    def subclasses(root):
        '''
        level_order_tree_traversal
        '''
        out = []
        q = []
        q.append(root)
        while q:
            v = q.pop(0)
            out.append(v)
            for child in v.__subclasses__():
                q.append(child)
        return out


class SNS(Catalog):
    '''
    '''
    
    def __init__(self, facility, *args, **kwargs):
        '''
        '''
        print("Init SNS")


class SNSSANS(SNS):
    '''
    '''
    
    def __init__(self, facility, *args, **kwargs):
        '''
        '''
        print("Init SNS SANS")


class SNSSANSEQSANS(SNSSANS):
    '''
    '''
    
    def __init__(self, facility, *args, **kwargs):
        '''
        '''
        print("Init SNS SANS EQSANS")


class HFIR(Catalog):
    '''
    '''
    
    def __init__(self, facility, *args, **kwargs):
        '''
        '''
        print("Init HFIR")


class HFIRSANS(HFIR):
    '''
    '''
    
    def __init__(self, facility, *args, **kwargs):
        '''
        '''
        print("Init HFIR SANS")


class HFIRSANSGPSANS(HFIRSANS):
    '''
    '''
    
    def __init__(self, facility, *args, **kwargs):
        '''
        '''
        print("Init HFIR SANS GPSANS")




    

def main():
    pprint(Catalog.subclasses(Catalog))
    sns = Catalog("SNS")
    hfir = Catalog("HFIR")
    hfir_sans = Catalog("HFIRSANS")
    
    
if __name__ == '__main__':
    main()
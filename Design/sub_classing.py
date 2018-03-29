import os

from abc import ABC
from pprint import pformat, pprint


# class CatalogMeta(type):
#     '''
#     Metaclass for the catalog
#     '''
#     def __call__(cls, *args, **kwargs):
#         '''
#         Deletes the arguments in the __new__ call
#         So the __init__ doesn't need them
#         '''
#         obj = cls.__new__(cls, *args, **kwargs)
#         _ = kwargs.pop("facility", None)
#         _ = kwargs.pop("technique", None)
#         _ = kwargs.pop("instrument", None)
#         obj.__init__(*args, **kwargs)
#         return obj

class Catalog(ABC):
    '''
    The main methods to be defined in the subclasses are here.
    '''

    # __metaclass__ = CatalogMeta

    def __new__(cls, facility, technique='', instrument='', *args, **kwargs):
        '''
        This allows to great subclasses from this base class,
        given:
        - facility name
        - technique name
        - instrument name
        See in the database for every instrument the valid
        - instrument.facility.name
        - instrument.name
        - instrument.technique

        The Catalog should be constructed like these examples:
        sns = Catalog("SNS")
        hfir = Catalog("HFIR")
        hfir_sans = Catalog("HFIR", "SANS")
        hfir_sans = Catalog(facility="HFIR", technique="SANS")
        
        '''

        # Get the subclasses of Catalog
        subclasses = Catalog.subclasses(Catalog)
        # To get first the very subclasses (more specific)
        subclasses.reverse()

        for subclass in subclasses:
            if str(subclass.__name__) == facility+technique+instrument:
                return super(cls, subclass).__new__(subclass)
            elif str(subclass.__name__) == facility+technique:
                return super(cls, subclass).__new__(subclass)
            elif str(subclass.__name__) == facility:
                return super(cls, subclass).__new__(subclass)
        raise Exception('Facility not supported: {}!'.format(facility+technique+instrument))

    @staticmethod
    def subclasses(root):
        '''
        This function performs a:
        level_order_tree_traversal
        (Google to know what this is)
        on the hierarchy tree of classes.
        @return a list with all the classes types 
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
    
    def __init__(self, p, *args, **kwargs):
        '''
        '''
        print("Init SNS")


class SNSSANS(SNS):
    '''
    '''
    
    def __init__(self, p, *args, **kwargs):
        '''
        '''
        print("Init SNS SANS")


class SNSSANSEQSANS(SNSSANS):
    '''
    '''
    
    def __init__(self, p, *args, **kwargs):
        '''
        '''
        print("Init SNS SANS EQSANS")


class HFIR(Catalog):
    '''
    '''
    
    def __init__(self, p, *args, **kwargs):
        '''
        '''
        print("Init HFIR")


class HFIRSANS(HFIR):
    '''
    '''
    
    def __init__(self, p, *args, **kwargs):
        '''
        '''
        print("Init HFIR SANS")


class HFIRSANSGPSANS(HFIRSANS):
    '''
    '''
    
    def __init__(self, p, *args, **kwargs):
        '''
        '''
        print("Init HFIR SANS GPSANS")




    

def main():
    print("All classes:")
    pprint(Catalog.subclasses(Catalog))
    print(80*"*")
    sns = Catalog(facility="SNS", p="required ini argument")
    # hfir = Catalog("required ini argument", "HFIR")
    hfir_sans = Catalog(facility="HFIR", technique="SANS", p="required ini argument")
    hfir_sans_gpsasn = Catalog(facility="HFIR", technique="SANS", instrument="GPSANS", p="required ini argument")
    
    
if __name__ == '__main__':
    main()
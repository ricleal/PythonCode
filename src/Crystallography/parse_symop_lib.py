#! /usr/bin/env python

import sys
import shlex
import ast

from collections import defaultdict

'''
SymOp.lib structure:

5 4 2 C2 PG2 MONOCLINIC 'C 1 2 1' 
  X,Y, Z 
 -X,Y,-Z 
 1/2+X,1/2+Y,Z 
 1/2-X,1/2+Y,-Z


<sg number> <number of sym operations> <?> <?> <point group> <crystal system> <long name>
< ... operations ...>


'''

FILENAME="symop.lib"


class SymOp():
    def __init__(self,filename=None):
        if filename is None:
            filename= FILENAME
        
        # Every dict will be initilsed as an empty list
        self.space_groups = defaultdict(list)
        self.point_groups = defaultdict(list)
    
        self._parse(filename)
    
    def _parse(self, filename):
        with open(FILENAME) as f:
            for line in f:
                if not line.startswith(' '):
                    #head
                    tokens = shlex.split(line)
                    if tokens[4] in self.point_groups:
                        parse_pg = False
                    else:
                         parse_pg = True
                else:
                    #body
                    self.space_groups[tokens[3]].append(line.strip())
                    if parse_pg:
                        self.point_groups[tokens[4]].append(line.strip())
    
    def sg(self,key):
        '''
        Return space group sysmmetry operations
        '''
        return self.space_groups[key]
    
    def pg(self,key):
        '''
        Return Point group equivalent reflections symetry operations
        
        A monoclinic crystal, has the Laue symmetry of 2/m. The equivalent coordinates, assuming a b-unique axis, 
        are given as (x, y, z), (-x, y, -z), (-x, -y, -z), and (x, -y, z). Thus the intensities of the (h k l), (h k l), (h k l), and (h k l)
        lattice points should have equivalent values. Note that this also means that the intensities of the (h k l), (h k l), (h k l), and (h k l) 
        should also be equivalent to each other but are not necessarily equivalent to (h k l), etc.
        '''
        return self.point_groups[key]
    

def equivalent_reflections(hkl,pg):
    '''
    '''
    h,k,l = hkl

    symop = SymOp()
    ops = symop.pg("PG222")
    
    eq_reflections = []
    
    for op in ops:
        op = op.replace('X','%s'%h)
        op = op.replace('Y','%s'%k)
        op = op.replace('Z','%s'%l)
        eq_reflections.append(ast.literal_eval( op ))
    
    return eq_reflections

def test():
    import pprint
    symop = SymOp()

    print symop.sg("P212121")
    print symop.pg("PG222")
    
    
    print equivalent_reflections((2,4,7),"PG222")
if __name__ == '__main__':
    test()  
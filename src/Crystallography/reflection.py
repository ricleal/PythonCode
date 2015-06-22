#! /usr/bin/env python

import sys
import shlex
import csv
import ast
import numpy as np
import os

FILENAME=os.path.join(os.path.dirname(os.path.realpath(__file__)), "reflection_conditions.csv")



class Reflections():
    def __init__(self,filename=None):
        if filename is None:
            filename= FILENAME
        
        self._parse(filename)
    
    def _parse(self, filename):
        self.reflections_by_space_group_number = {}
        self.reflections_by_space_group_name = {}
        with open(FILENAME) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for line in csv_reader:
                if not line[0].startswith("#"):
                    self.reflections_by_space_group_number[line[0]]=line[2]
                    self.reflections_by_space_group_name[line[1]]=line[2]
                    
    
    def __getitem__(self, attr):
        try :
            return self.reflections_by_space_group_number[attr]
        except:
            try:
                sg = attr.upper()
                return self.reflections_by_space_group_name[sg]
            except:
                return None

class SpaceGroup():
    def __init__(self, space_group):
        
        ref = Reflections()
        
        self.space_group = space_group
        
        reflection_conditions = ref[space_group] # "[[2,0,0],[0,2,0],[0,0,2]]"
        self.reflection_conditions = ast.literal_eval(reflection_conditions)
        
        print  self.reflection_conditions
        
    def _are_there_refection_conditions(self):
        """
        Are there refection conditions for this space group
        """
        return np.any(np.array(self.reflection_conditions) != 0)

    def _index_of_the_nonzero_reflection(self, reflection):
        """
        if two index of a reflection are 0 return the index of the non zero
        reflection :: [h,k,l]
        Eg: [0,2,0] returns 1
        """
        assert len(reflection) == 3
        if reflection[0] == 0 and reflection[1] == 0:
            return 2
        elif reflection[0] == 0 and reflection[2] == 0:
            return 1
        elif reflection[1] == 0 and reflection[2] == 0:
            return 0
        else:
            return None
        

    def is_valid_reflection(self, reflection):
        """
        reflection :: [h,k,l]
        A reflection is valid if it's not a systematic absence
        """
        index_of_the_nonzero_reflection = self._index_of_the_nonzero_reflection(reflection)
        if self._are_there_refection_conditions() and index_of_the_nonzero_reflection is not None:
            for c in self.reflection_conditions:
                index_of_the_nonzero_reflection_condition = self._index_of_the_nonzero_reflection(c)
                if index_of_the_nonzero_reflection_condition == index_of_the_nonzero_reflection:
                    if reflection[index_of_the_nonzero_reflection] % c[index_of_the_nonzero_reflection_condition] == 0:
                        return False
        return True
                
                
    
    
def test():
    from unittest2 import *
    import pprint
    ref = Reflections()
    
    pprint.pprint(ref.reflections_by_space_group_number)
    pprint.pprint(ref.reflections_by_space_group_name)
    print ref["P212121"]
    pprint.pprint(ref.reflections_by_space_group_name["P212121"])
    
    ##
    
    sg = SpaceGroup("P2")
    assert sg._are_there_refection_conditions() == False
    
    sg = SpaceGroup("p21")
    assert sg._are_there_refection_conditions() == True
    assert sg.is_valid_reflection([1,2,4]) == True
    assert sg.is_valid_reflection([0,2,0]) == False
    assert sg.is_valid_reflection([0,8,0]) == False
    assert sg.is_valid_reflection([1,-8,0]) == True
    assert sg.is_valid_reflection([0,-10,0]) == False
    
    sg = SpaceGroup("p212121")
    assert sg.is_valid_reflection([1,2,4]) == True
    assert sg.is_valid_reflection([0,2,0]) == False
    assert sg.is_valid_reflection([0,8,0]) == False
    assert sg.is_valid_reflection([1,-8,0]) == True
    assert sg.is_valid_reflection([0,-10,0]) == False
    assert sg.is_valid_reflection([6,0,0]) == False
    assert sg.is_valid_reflection([0,0,5]) == True
    assert sg.is_valid_reflection([12,0,0]) == False
    
if __name__ == '__main__':
    test()  
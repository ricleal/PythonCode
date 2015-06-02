#! /usr/bin/env python

import sys
import shlex

FILENAME="symop.lib"


class SymOp():
    def __init__(self,filename=None):
        if filename is None:
            filename= FILENAME
        
        self.space_groups = self._parse(filename)
    
    def _parse(self, filename):
        space_groups = {}
        with open(FILENAME) as f:
            for line in f:
                if not line.startswith(' '):
                    #head
                    tokens = shlex.split(line)
                    space_groups[tokens[3]] = []
                else:
                    #body
                    space_groups[tokens[3]].append(line.strip())
        return space_groups
    
    def __getitem__(self, attr):
         return self.space_groups[attr]

def test():
    import pprint
    symop = SymOp()
    
    pprint.pprint(symop.space_groups)
    pprint.pprint(symop["P212121"])

if __name__ == '__main__':
    test()  
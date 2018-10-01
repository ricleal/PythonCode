#!/usr/bin/env python
from __future__ import print_function

import sys
import h5py
from glob import glob


def parse(filename):
    try:
        f = h5py.File(filename, "r")
        for item in f.values():
            if isinstance(item, h5py.Group) and item.name.startswith("/entry"):
                print(item.name)
    except IOError:
        pass


if __name__ == '__main__':
    for filename in glob(sys.argv[1]):
        print(filename)
        parse(filename)

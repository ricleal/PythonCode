#!/usr/bin/env python3

import h5py
from glob import glob
import sys
import os


def display(path):
    files = glob(path)

    for f in files:
        hf = h5py.File(f, 'r')
        entry = hf['entry']
        total_counts = entry['total_counts']
        run_number = entry['run_number']
        sample_name = entry['sample']['name']
        print(
            os.path.basename(f),
            run_number.value[0].decode("utf-8"),
            total_counts.value[0],
            sample_name.value[0].decode("utf-8"),
        )


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("""
        Usage: {} <input directory>
        E.g.: python3 print_parameter.py "/SNS/EQSANS/IPTS-21070/nexus/*.h5"
""".format(sys.argv[0]))
    else:
        display(sys.argv[1])

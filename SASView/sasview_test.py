'''
Test using SASView in analysis.sns.gov

'''

# Path in Analysis
sasview_directory = '/usr/lib/python2.7/site-packages/sasview-4.1-py2.7-linux-x86_64.egg'

file_path = "/SNS/EQSANS/IPTS-19737/shared/92409_Iqxy.dat"

import sys
import os

sys.path.append(sasview_directory)
from sas.sascalc.dataloader.readers.red2d_reader import Reader
from sas.sascalc.dataloader.manipulations import Sectorcut, SectorQ

def main():
    
    r = Reader()
    data = r.read(file_path)



if __name__ == "__main__":
    main()


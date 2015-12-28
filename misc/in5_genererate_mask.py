#!/usr/bin/python

'''
@author: Ricardo Leal
'''

import sys

## Global variables
pixelsToRemoveTop=7
pixelsToRemoveBottom=8
numberOfTubes=384
numberOfPixelsPerTube=256
firstPixelDetectorID=1

def init():
    print """<?xml version="1.0"?>
<detector-masking>
    <group>
        <detids>"""

def finalise():
    print """
    </detids>
    </group>
</detector-masking>
"""

def printMasketPixels():
    thisPixel = firstPixelDetectorID;
    for i in range(numberOfTubes):
        for j in range(numberOfPixelsPerTube):
            if j < pixelsToRemoveBottom or j >= numberOfPixelsPerTube - pixelsToRemoveTop :
                sys.stdout.write('%d'%thisPixel)
                if thisPixel != numberOfTubes * numberOfPixelsPerTube -1  + firstPixelDetectorID:
                    sys.stdout.write(',')
            thisPixel+=1;


    



if __name__ == "__main__":
    init()
    printMasketPixels()
    finalise()
    

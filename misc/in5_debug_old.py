#!/usr/bin/python

'''
@author: Ricardo Leal
'''

import nxs
import numpy as np
import argparse
import sys

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

""" CONSTS """

distanceSampleDetector = 4
wavelength = 5
ei = 3.27148
channelWidth = 14.6349  # microsec
pixelSize = 0.011479 # meters

""" Calculates CONSTS : Don't edit """

# m/s
neutronSpeed = 6.626E-034 / (1.675E-027 * wavelength * 0.0000000001)



def peakdet(v, delta, x=None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    
    Returns two arrays
    
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %      
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.
    
    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.
    
    """
    maxtab = []
    mintab = []
       
    if x is None:
        x = np.arange(len(v))
    
    # v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not np.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN
    
    lookformax = True
    
    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True
 
    return np.array(maxtab), np.array(mintab)

def epp(v):
    'Return Max EPP'
    maximaPeaks, minimaPeaks = peakdet(v, delta=5, x=None);
    if len(maximaPeaks) > 0 :
        maxArr = np.max(maximaPeaks, 0)
        return maxArr[0]
    else :
        return np.NaN
    
# http://docs.enthought.com/mayavi/mayavi/mlab_case_studies.html#mlab-case-studies

def readData(filePath='/home/leal/Documents/Mantid/IN5/094460.nxs'):
    f = nxs.open(filePath)
    f.opengroup('entry0')
    f.opengroup('data')
    f.opendata('data')
    a = f.getdata()
    f.closedata()
    f.closegroup()
    f.closegroup()
    f.close()
    # a.shape
    # Out[15]: (384, 256, 512)
    return a


def getSpectraEPPsForTube(data, tubeNr):
    """
    Reduce one dimension of the 3D array
    """
    
    thisTube = data[tubeNr, :, :]
    numberOfPixelsInTheTube = thisTube.shape[0];
    eppsForThisTube = np.zeros(numberOfPixelsInTheTube);
    for y in range(numberOfPixelsInTheTube):
        thisSpectrum = thisTube[y, :]
        thisEpp = epp(thisSpectrum)
        eppsForThisTube[y] = thisEpp;
    
    return eppsForThisTube

def getTofBins(pos, numberOfChannels):
    # v = d/t
    print 'EPP=', pos,
    t = distanceSampleDetector / neutronSpeed * 1e6
    print 't=', t
    bins = np.zeros(numberOfChannels)
    for i in range(numberOfChannels):
        bins[i] = t + channelWidth * (i - pos);
    
    return bins



    

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Debug IN5 tof')
    parser.add_argument('-f', '--file', help='Nexus file to parse', required=True)
    args = vars(parser.parse_args())

    data = readData(args['file']);
    print 'Shape of the parsed data:', 'X:', data.shape[0], 'Y:', data.shape[1], 'Z:', data.shape[2]
    
    eppsForThisTube = getSpectraEPPsForTube(data, 100)
    print 'eppsForThisTube', eppsForThisTube.shape
    
    timeBins = getTofBins(eppsForThisTube[len(eppsForThisTube) / 2], data.shape[2])
    print 'timeBins.shape: ', timeBins.shape
    print 'timeBins: ',timeBins
    #
    
    # get EPPs in time
    eppsInTime = np.zeros(len(eppsForThisTube));
    for idx,e in enumerate(eppsForThisTube):
        if not np.isnan(e):
            eppsInTime[idx] = timeBins[int(e)]
        else :
            eppsInTime[idx] = np.NAN

    print 'eppsInTime.shape: ', eppsInTime.shape
    print 'eppsInTime: ',eppsInTime
                
    # Plot time differences
    deltaEppsInTime = np.array([])
    eppInTime = eppsInTime[len(eppsForThisTube)/2]
    for i in eppsInTime :
        if not np.isnan(i):
            deltaEppsInTime = np.append(deltaEppsInTime, i-eppInTime)
        else :
            deltaEppsInTime = np.append(deltaEppsInTime,np.NAN)
    
    print 'deltaEppsInTime.shape: ', deltaEppsInTime.shape
    print 'deltaEppsInTime: ',deltaEppsInTime
    
    plt.plot(range(len(deltaEppsInTime)), deltaEppsInTime,'o', label='DeltaTof')
    
    #
    distanceInTime = np.zeros(len(deltaEppsInTime));
    pos = len(deltaEppsInTime)/2
    
    for i in range(len(deltaEppsInTime)):
        thisDistance = np.sqrt( distanceSampleDetector*distanceSampleDetector +  ((i - pos)*pixelSize*(i - pos)*pixelSize) );
        t = thisDistance / neutronSpeed * 1e6
        distanceInTime[i] = t
    
    deltaDistanceInTime = distanceInTime - distanceInTime[pos]
    
    plt.plot(range(len(deltaDistanceInTime)), deltaDistanceInTime,'-', label='deltaDistanceInTime')
    

    
    
        
    
    # plot(timeBins, eppsForThisTube)
    # plot(eppsForThisTube)
    plt.show()

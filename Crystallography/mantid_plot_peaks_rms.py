#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""

Run this in Mantid plot!


"""


import sys
sys.path.append('/opt/mantidnightly/bin')

sys.path.append('/SNS/users/rhf/git/PythonCode/src/Crystallography')
from reflection import SpaceGroup

import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from mantid.simpleapi import *
from mantid.api import *
from mantid.kernel import V3D


run = 3848
unit_cell = [74.0274,     74.2437 ,    99.9710  ,   90   ,  90   , 120]
space_group = ""
num_peaks_to_find_for_reference = 3000
num_peaks_to_find_for_indexing = 300
max_d  = 110

# run = 3870
# unit_cell = [41.5, 63.37, 122.37, 90, 90, 90]
# space_group = ""
# num_peaks_to_find_for_reference = 3000
# num_peaks_to_find_for_indexing = 300
# max_d  = 130

# run = 4090
# unit_cell = [36.5, 58.3, 63.6, 90, 90, 90]
# space_group = "P212121"
# num_peaks_to_find_for_reference = 1000
# num_peaks_to_find_for_indexing = 300
# max_d  = 70


run_str = str(run)

# For finding peaks
#min_d = 30.0
distance_threshold = 0.9 * 2*math.pi / max_d # 0.043
density_threshold_factor = 10


# Indexing
tolerance = 0.15

event_ws_prefix = 'event_ws_'
mde_ws_prefix = 'mde_ws_'
peaks_ws_prefix = 'peaks_ws_'
peaks_found_ws_prefix = 'peaks_found_ws_'
peaks_indexed_ws_prefix = 'peaks_indexed_ws_'
peaks_predicted_ws_prefix = 'peaks_predicted_ws_'

peaks_ws_merged = None

event_ws_name = event_ws_prefix + run_str
mde_ws_name = mde_ws_prefix + run_str
peaks_ws_name = peaks_ws_prefix + run_str
peaks_found_ws_name = peaks_found_ws_prefix + run_str
peaks_indexed_ws_name = peaks_indexed_ws_prefix + run_str
peaks_predicted_ws_name = peaks_predicted_ws_prefix + run_str

LoadEventNexus(
    #Filename='/SNS/MANDI/IPTS-12697/0/4089/NeXus/MANDI_4089_event.nxs',
    Filename='MANDI_'+run_str,
    OutputWorkspace=event_ws_name,
    FilterByTofMin=14800,
    FilterByTofMax=31000
    )

ConvertToMD(
    InputWorkspace=event_ws_name,
    OutputWorkspace=mde_ws_name,
    QDimensions='Q3D',
    dEAnalysisMode='Elastic',
    QConversionScales='Q in A^-1',
    LorentzCorrection='1',
    MinValues='-3,-3,-3', #Q values
    MaxValues='3,3,3', #Q values
    SplitInto='2',
    SplitThreshold='50',
    MaxRecursionDepth='11',
    )

FindPeaksMD(
    InputWorkspace=mde_ws_name,
    OutputWorkspace=peaks_ws_name,
    MaxPeaks=num_peaks_to_find_for_reference,
    PeakDistanceThreshold=distance_threshold,
    DensityThresholdFactor=density_threshold_factor
    )

CloneWorkspace(InputWorkspace=peaks_ws_name, OutputWorkspace=peaks_found_ws_name )

FindUBUsingLatticeParameters(
    PeaksWorkspace=peaks_ws_name,
    a=unit_cell[0],
    b=unit_cell[1],
    c=unit_cell[2],
    alpha=unit_cell[3],
    beta=unit_cell[4],
    gamma=unit_cell[5],
    NumInitial=num_peaks_to_find_for_reference,
    Tolerance=tolerance,
    )

IndexPeaks(PeaksWorkspace=peaks_ws_name, Tolerance=tolerance)

CloneWorkspace(InputWorkspace=peaks_ws_name, OutputWorkspace=peaks_indexed_ws_name )

########

DeleteWorkspace(peaks_ws_name)


FindPeaksMD(
    InputWorkspace=mde_ws_name,
    OutputWorkspace=peaks_ws_name,
    MaxPeaks=num_peaks_to_find_for_indexing,
    PeakDistanceThreshold=distance_threshold,
    DensityThresholdFactor=density_threshold_factor
    )

FindUBUsingLatticeParameters(
    PeaksWorkspace=peaks_ws_name,
    a=unit_cell[0],
    b=unit_cell[1],
    c=unit_cell[2],
    alpha=unit_cell[3],
    beta=unit_cell[4],
    gamma=unit_cell[5],
    NumInitial=num_peaks_to_find_for_indexing,
    Tolerance=tolerance,
    )

PredictPeaks(
    InputWorkspace=peaks_ws_name,
    OutputWorkspace=peaks_ws_name,
    WavelengthMin=2.0,
    WavelengthMax=4.0,
    MinDSpacing=2.0,
    MaxDSpacing=20.0,
    ReflectionCondition='Primitive',
    )

CloneWorkspace(InputWorkspace=peaks_ws_name, OutputWorkspace=peaks_predicted_ws_name )

########################

def v3d_to_list(v):
    return np.array([v.X(),v.Y(),v.Z()])

def v3d_list_to_numpy_array(arr):
    out = np.empty( [len(arr), 3], dtype=np.float64)
    for idx,v in enumerate(arr):
        out[idx] = v3d_to_list(v)
    return out

def dist(x,y):
    return np.sqrt(np.sum( ((x-y)**2), axis=1))

def get_closest_point_index(coord_vector, coord_value):
    distances = dist(coord_vector,coord_value)
    index_of_min_distance = np.argmin(distances)
    return index_of_min_distance, distances[index_of_min_distance]

def get_collumn_from_peak_ws(peak_ws, column_name):
    peak_ws_column_v3d =  peak_ws.column(column_name)
    peak_ws_column = v3d_list_to_numpy_array(peak_ws_column_v3d)
    return peak_ws_column

def remove_systematic_absences(peak_ws):
    initial_length = peak_ws.getNumberPeaks()
    sg = SpaceGroup(space_group)
    i = 0;
    while True:
        try:
            p = peak_ws.getPeak(i)
        except:
            break
        reflection = [int(p.getH()),int(p.getK()),int(p.getL())]
        
        if not sg.is_valid_reflection(reflection):
            peak_ws.removePeak(i)
        else: # valid!
            i+=1;
    
    print "Removed %d peaks from inital %d peaks."%(initial_length - peak_ws.getNumberPeaks(), initial_length)

peaks_predicted_qsample_collumn = get_collumn_from_peak_ws(mtd[peaks_predicted_ws_name], 'QSample')

distances_vector = np.empty([mtd[peaks_found_ws_name].getNumberPeaks()], dtype=np.float64)

if space_group:
    remove_systematic_absences(mtd[peaks_predicted_ws_name]) # predicted (already indexed!) peaks

i = 0;
while True:
    try:
        p_found = mtd[peaks_found_ws_name].getPeak(i)
    except:
        break
    p_found_qsample_value_v3d = p_found.getQSampleFrame()
    p_found_qsample_value = v3d_to_list(p_found_qsample_value_v3d)
    closest_point_index, distance = get_closest_point_index(peaks_predicted_qsample_collumn, p_found_qsample_value)
    distances_vector[i] = distance
    i+=1;


## Use in Mantid Plot:

##
bin_count_collumn = mtd[peaks_found_ws_name].column('BinCount')
gui_cmd(plt.figure)
gui_cmd(plt.plot, bin_count_collumn, distances_vector, 'y.')
gui_cmd(plt.xlabel, 'BinCount')
gui_cmd(plt.ylabel, 'Distance (QSample)')
gui_cmd(plt.show)


##
d_spacing_collumn = mtd[peaks_found_ws_name].column('DSpacing')
gui_cmd(plt.figure)
gui_cmd(plt.plot, d_spacing_collumn, distances_vector, 'bo')
gui_cmd(plt.xlabel, 'DSpacing')
gui_cmd(plt.ylabel, 'Distance (QSample)')
gui_cmd(plt.show)

##
tof_collumn = mtd[peaks_found_ws_name].column('TOF')
gui_cmd(plt.figure)
gui_cmd(plt.plot, tof_collumn, distances_vector, 'rx')
gui_cmd(plt.xlabel, 'TOF')
gui_cmd(plt.ylabel, 'Distance (QSample)')
gui_cmd(plt.show)

##
d_spacing_collumn = mtd[peaks_found_ws_name].column('DSpacing')
distances_vector_rms = np.sqrt(1-np.square(distances_vector))
gui_cmd(plt.figure)
gui_cmd(plt.plot, d_spacing_collumn, distances_vector_rms, 'g.')
gui_cmd(plt.xlabel, 'DSpacing')
gui_cmd(plt.ylabel, 'RMSD (QSample)')
gui_cmd(plt.show)



## 
markers = matplotlib.lines.Line2D.markers.keys()
markers.remove('None')
markers.remove('')
markers.remove(' ')
markers.remove(None)
colors = list("bgrcmyk")

det_id_collumn = mtd[peaks_found_ws_name].column('DetID')
det_id_collumn = np.array(det_id_collumn)
bankname_collumn = mtd[peaks_found_ws_name].column('BankName')
bankname_collumn = np.array(bankname_collumn)

gui_cmd(plt.figure)
for idx,bankname in  enumerate( np.unique(bankname_collumn) ):
    x = det_id_collumn[ (bankname_collumn == bankname) ]
    y = distances_vector[ (bankname_collumn == bankname) ]
    marker, color = markers[idx % len(markers)], colors[idx % len(colors)]
    gui_cmd(plt.scatter, x,y,c=color, marker=marker,label = bankname)

gui_cmd(plt.xlabel, "DetId")
gui_cmd(plt.ylabel, 'Distance (QSample)')
gui_cmd(plt.legend)
gui_cmd(plt.show)

############3

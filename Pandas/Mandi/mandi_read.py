import numpy as np
import pandas as pd
from timeit import timeit

@timeit
def spherical(xyz):
    ptsnew = np.zeros(xyz.shape)

    xy = xyz[:,0]**2 + xyz[:,1]**2
    ptsnew[:,0] = np.sqrt(xy + xyz[:,2]**2)
    ptsnew[:,1] = np.arctan2(np.sqrt(xy), xyz[:,2]) # for elevation angle defined from Z-axis down
    #ptsnew[:,4] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    ptsnew[:,2] = np.arctan2(xyz[:,1], xyz[:,0])
    return ptsnew

df = pd.read_hdf('mandi.hdf', 'mandi')


xyz = df.as_matrix(['x', 'y', 'z'])
rtp = spherical(xyz)

df2 = pd.DataFrame(rtp, columns=('r', 't', 'p'))
result = pd.concat([df, df2], axis=1)

print "New data frame headers:", result.columns.values

result.to_hdf('mandi_2.hdf', 'mandi')

print "DF Saved!"




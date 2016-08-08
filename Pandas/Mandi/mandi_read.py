from __future__ import print_function

import numpy as np
import pandas as pd
import time


def spherical(xyz):
    ptsnew = np.zeros(xyz.shape)
    xy = xyz[:,0]**2 + xyz[:,1]**2
    ptsnew[:,0] = np.sqrt(xy + xyz[:,2]**2)
    ptsnew[:,1] = np.arctan2(np.sqrt(xy), xyz[:,2]) # for elevation angle defined from Z-axis down
    #ptsnew[:,1] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    ptsnew[:,2] = np.arctan2(xyz[:,1], xyz[:,0])
    return ptsnew

df = pd.read_hdf('/tmp/mandi.hdf', 'mandi')
print("Data frame headers:{}".format(df.columns.values))

xyz = df.as_matrix(['x', 'y', 'z'])

ts = time.time()
rtp = spherical(xyz)
te = time.time()
print("Cartesian to Sperical took {:2.3f} seconds".format(te-ts))

df2 = pd.DataFrame(rtp, columns=('r', 't', 'p'))
result = pd.concat([df, df2], axis=1)

print("NEW Data frame headers:{}".format(result.columns.values))


# Reshape and Indexing example: get x,y,z for bank1
ts = time.time()
df_tmp =  df[df['bank_name'] == 'bank1']
shape_i = len(np.unique(df_tmp[['i']].values))
shape_j = len(np.unique(df_tmp[['j']].values))
xyz = df_tmp[['x','y','z']].values
xyz_2d = xyz.reshape(shape_i, shape_j, 3)
print("XYZ for Pixel: xyz_2d[128,128] = {}".format(xyz_2d[128,128]))
te = time.time()
print("Reshape and Indexing took {:2.3f} seconds".format(te-ts))

result.to_hdf('/tmp/mandi_2.hdf', 'mandi')

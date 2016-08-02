import pandas as pd
import numpy as np
size_x = 256
size_y = 192
dim_x = 0.004
dim_y = 0.0055
z = 10
offset_x = -0.384
offset_y = -0.704

## 2D image in 1D
iv, jv = np.mgrid[0:size_x, 0:size_y]
iv = iv.ravel()
jv = jv.ravel()

# x,y,z real coordinates vectors
xv = offset_x + iv*dim_x
yv = offset_y + jv*dim_y
zv = np.full_like(xv,z)

# Concatenate all of them
allv = np.column_stack((iv, jv, xv,yv,zv))

df = pd.DataFrame(data = allv, columns=['i', 'j', 'x', 'y', 'z'])
# Set a multi index
df.set_index(['i','j'], inplace=True)

# Accessing for example origin
df.loc[0,0].values

df.to_hdf("/tmp/test.h5", "/entry")

df2 = pd.read_hdf("/tmp/test.h5", "/entry")

assert(np.array_equal(df.loc[0,0].values,df2.loc[0,0].values))

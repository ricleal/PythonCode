import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from collections import OrderedDict
'''

Converts 2D mumpy array into pandas Dataframe and back into a 2D array


Matrix ij convention
i is Row
j is column

2 detectors

name,i,j,x,y,z,values,errors
'''

# Det1
#
# Shape of detector
n_rows, n_cols = shape = (2, 5)  # pos 0 rows, pos 1 columns
total_size = n_rows * n_cols

value = np.arange(total_size).reshape(n_rows, n_cols)
error = np.sqrt(value)
rows_v, cols_v = np.meshgrid(range(n_rows), range(n_cols), indexing='ij')
# Simulate x,y,values
x_v, y_v = np.meshgrid(np.random.rand(n_rows), np.random.rand(n_cols), indexing='ij')

det1 = OrderedDict({'name': np.full(total_size, 'det1', dtype=np.dtype('S4')),
     'i': rows_v.ravel(),  # i = rows
     'j': cols_v.ravel(),  # j = coluns
     'x': x_v.ravel(),
     'y': y_v.ravel(),
     'value': value.ravel(),
     'error': error.ravel(),
     })

df1 = pd.DataFrame(det1)

#
# Det2
#

# Shape of detectors
n_rows, n_cols = shape = (3, 4)  # pos 0 rows, pos 1 columns
total_size = n_rows * n_cols

value = np.arange(total_size).reshape(n_rows, n_cols)
error = np.sqrt(value)
rows_v, cols_v = np.meshgrid(range(n_rows), range(n_cols), indexing='ij')
# Simulate x,y,values
x_v, y_v = np.meshgrid(np.random.rand(n_rows), np.random.rand(n_cols), indexing='ij')

det2 = OrderedDict({'name': np.full(total_size, 'det2', dtype=np.dtype('S4')),
     'i': rows_v.ravel(),  # i = rows
     'j': cols_v.ravel(),  # j = coluns
     'x': x_v.ravel(),
     'y': y_v.ravel(),
     'value': value.ravel(),
     'error': error.ravel(),
     })


df2 = pd.DataFrame(det2)

df = df1.append(df2, ignore_index=True)
print("---- DataFrame ----")
print(df)


pivot = df[df.name == "det1".encode('utf-8')].pivot(index='i', columns='j', values='value')
print("---- DataFrame Pivot Det1 ----")
print(pivot)

pivot = df[df.name == "det2".encode('utf-8')].pivot(index='i', columns='j', values='value')
print("---- DataFrame Pivot Det2 ----")
print(pivot)

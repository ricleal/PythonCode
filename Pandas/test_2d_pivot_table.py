import pandas as pd
import numpy as np

'''

Converts 2D mumpy array into pandas Dataframe and back into a 2D array

Matrix ij convention
i is Row
j is column
'''

n_rows, n_cols = shape = (2, 5)  # pos 0 rows, pos 1 columns
data = np.arange(10).reshape(n_rows, n_cols)
print("---- Data ----")
print(data)
assert(data[1, 0] == 5)

rows_v, cols_v = np.meshgrid(range(n_rows), range(n_cols), indexing='ij')
d = {'i': rows_v.ravel(),  # i = rows
     'j': cols_v.ravel(),  # j = coluns
     'value': data.ravel(),
     }

df = pd.DataFrame(d)
print("---- DataFrame ----")
print(df)

pivot = df.pivot(index='i', columns='j', values='value')
print("---- DataFrame Pivot ----")
print(pivot)
assert(pivot.loc[1][0] == 5)

print("---- DataFrame Pivot as 2D array ----")
print(pivot.values)
assert(data[1, 0] == pivot.values[1, 0])

print("---- DataFrame as 2D array----")
df = df.set_index(['i', 'j'])
assert(df.loc[1, 0].value == 5)

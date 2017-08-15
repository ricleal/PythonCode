import pandas as pd

d = {
    'city': pd.Series(['k', 'k', 'c', 'c'],),
    'zip': pd.Series([123, 123, 345, 345],),
    'clicks': pd.Series([1, 2, 3, 4],),
    }

df = pd.DataFrame(d)

# In [12]: df
# Out[12]: 
#   city  clicks  zip
# 0    k       1  123
# 1    k       2  123
# 2    c       3  345
# 3    c       4  345


df2 = df.groupby(['city','zip'])['clicks'].sum().reset_index()

# In [11]: df2
# Out[11]: 
#   city  zip  clicks
# 0    c  345       7
# 1    k  123       3


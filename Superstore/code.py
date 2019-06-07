import numpy as np
import pandas as pd

'''
See: https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b
'''

df = pd.read_csv('orders.csv', delimiter=',')

print(df.describe())

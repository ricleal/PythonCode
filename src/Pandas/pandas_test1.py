import pandas as pd
import matplotlib.pyplot as plt

#
# Auto
#

auto = pd.read_csv('../SeaBorn/data/auto.csv')
print auto.describe()

# histogram
auto.weight.hist()

plt.figure()
plt.scatter(auto.year,auto.weight)


plt.show()
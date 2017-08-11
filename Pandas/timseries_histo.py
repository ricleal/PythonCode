import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


#
# Let's simulate some TOF data
#
N = 100000

# freq='N' : N nanoseconds
sample_time = pd.date_range('1/1/2016', freq='100N', periods=N)
# tof from 100us to 10000us
tof_min = pd.Timedelta(100, unit='us')
tof_max = pd.Timedelta(10000, unit='us')
tof = np.random.randint(tof_min.value, high=tof_max.value, size=(1,N), dtype=np.int64)
tof_timeseries = pd.TimedeltaIndex(tof.flatten(), unit="ns")
detector_time = sample_time + tof_timeseries


detector_pos_ij = np.random.randint(0, high=128, size=(2,N)) # detectors : 4x4
detector_numbers = np.random.randint(0, high=2, size=(1,N)) # 2 detectors

columns = np.concatenate( (detector_pos_ij, detector_numbers) )

# I'm ignoring the times and just using tof
df = pd.DataFrame(columns.T, index=tof_timeseries, columns=['i', 'j', 'detector'])

# Make t as timestamp rather than int
# df['t']  = pd.to_datetime(df['t'], unit='ns')

# unique
# df.groupby(['i','j','detector']).size()

# Resample (rebinning?) from 100us to 1000 us
# df.groupby([pd.TimeGrouper('1000us'),'i','j','detector']).size()

# plot counts in 1st detector
# first detector
#pivot = df[df.detector==1].groupby(['i','j']).size().unstack('j').fillna(0)


pivot = df[df.detector==1 & df.index >= '100us' & df.index <= '1000us']].groupby(['i','j']).size().unstack('j').fillna(0)

plt.imshow(pivot.values)
plt.colorbar()
plt.show()


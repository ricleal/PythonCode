#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import pandas as pd
import h5py
import re

from datetime import datetime

# f = h5py.File("/SNS/MANDI/IPTS-8776/0/5800/NeXus/MANDI_5800_event.nxs", "r")
f = h5py.File("/Users/rhf/MANDI_5800_event.nxs", "r")


event_banks = [item for item in f["entry"].values() if isinstance(item, h5py.Group) and item.name.endswith("events")]

df = pd.DataFrame()

for bank in event_banks[:2]: # For debug use event_banks[-1:]

    #
    # index is event id, value is pixel_id
    event_pixel_id = bank["event_id"].value

    #
    # create tmp df with the pixel_id inside
    df_tmp = pd.DataFrame(
        data = event_pixel_id,
        columns = ['pixel_id']
    )

    #
    # Get the Pixels position 256x256 = 65536
    pixel_ids = bank["pixel_id"].value
    # flatten pixel_ids and get respective indices
    XX,YY = np.meshgrid(np.arange(pixel_ids.shape[1]),np.arange(pixel_ids.shape[0]))
    # 2d array of the format: pixel_id, i, j
    pixel_id_and_indices = np.vstack((pixel_ids.ravel(),XX.ravel(),YY.ravel())).T

    # tmp df for detector info
    df_tmp2 = pd.DataFrame(
        data=pixel_id_and_indices,
        columns=['pixel_id', 'i', 'j'],
    )
    # Left join
    df_tmp = pd.merge(left=df_tmp,right=df_tmp2, how='left', left_on='pixel_id', right_on='pixel_id')
    # remove the pixel_id (we don't need it amy more)
    df_tmp = df_tmp.drop('pixel_id', 1)

    #
    # index is event id, value time
    event_time_offset = bank["event_time_offset"].value
    df_tmp['time_offset'] = event_time_offset


    # Length pulses != events
    #
    # index is pulse id, value is event_id
    pulse_event_index = bank["event_index"].value
    pulse_event_index_step = np.diff(pulse_event_index) # difference between the current and previous
    pulse_event_index_step = np.insert(pulse_event_index_step,0,0) # Insert 0 in the beggining
    #
    # index is pulse id, value pulse 0 time
    pulse_time_zero = bank["event_time_zero"].value
    pulse_time_zero_with_event = pulse_time_zero[pulse_event_index_step>0] # only where there is a count
    pulse_event_index_with_event = pulse_event_index[pulse_event_index_step>0]

    df_tmp2 = pd.DataFrame(
        data= np.column_stack((pulse_event_index_with_event,pulse_time_zero_with_event)),
        columns=['event_id', 'time_zero'],
    )
    df_tmp2.event_id = df_tmp2.event_id.astype(np.int64)
    # Left join
    df_tmp = pd.merge(left=df_tmp,right=df_tmp2, how='left',  left_index = True, right_on='event_id')
    df_tmp = df_tmp.fillna(method='bfill') # fill nans with the value from the next cell



    #
    # get the bank number
    pattern = re.compile(r"/entry/bank(\d+)_events")
    match = pattern.match(bank.name)
    bank_number = int(match.group(1))

    #
    # Bank Number
    bank_number_array = np.array([bank_number]*len(df_tmp))
    df_tmp['bank_id'] = bank_number_array

    # Append to the final table
    df = df.append(df_tmp, ignore_index = True)

#
# Convert TOF number to time_delta
# SLOW!
df['time_offset'] = pd.to_timedelta(df['time_offset'],  unit="us")

# SLOW
1103776 rows × 6 columns

# Just to make sure start and end times makes sense
start_date = np.datetime64(f['entry']['start_time'].value[0])
print(start_date)
end_time = np.datetime64(f['entry']['end_time'].value[0])
print(end_time)

# SLOW
df['time_zero'] = pd.to_timedelta(df.time_zero, unit='s') + start_date
df = df.set_index('time_zero')

# We don't need event id
df = df.drop('event_id', 1)


# TOF Range
df.time_offset.min(),df.time_offset.max()


# Select a date range
df.loc['2016-07-15 09:00:00.0':'2016-07-15 10:00:00.0']

see how many neutrons every pixel
df.groupby(["bank_id","i","j"]).count()

# Rebining by tof bin 1000us
df.groupby(['bank_id','i','j']).time_offset.resample('1000us').count()


#
# TODO HERE
#

df.resample("100us").sum()

#Selection:
df.ix['1970-01-01 00:00:00.023490000':'1970-01-01 00:00:00.023494974']

df.resample("100us")

counts = df.groupby(["bank_number", "pixel_id"]).count()

counts = df.groupby(pd.Grouper(freq='100us'))["bank_number", "pixel_id"]


df.groupby(pd.Grouper(freq='100us')).apply(lambda x: x.groupby(["bank_number", "pixel_id"]).sum())

df.groupby(df.index)["bank_number", "pixel_id"].nunique()

df["conc"] = df.apply(lambda x: x["bank_id"]*100000+x["pixel_d"])
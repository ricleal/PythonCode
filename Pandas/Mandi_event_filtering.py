#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import pandas as pd
import h5py
import re

from datetime import datetime

f = h5py.File("/SNS/MANDI/IPTS-8776/0/5800/NeXus/MANDI_5800_event.nxs", "r")


event_banks = [item for item in f["entry"].values() if isinstance(item, h5py.Group) and item.name.endswith("events")]

columns = ["bank_number", "pixel_id"]
df = pd.DataFrame()

for bank in event_banks:
    # get the bank number
    pattern = re.compile(r"/entry/bank(\d+)_events")
    match = pattern.match(bank.name)
    bank_number = int(match.group(1))

    # # Pixels: 65536
    # pixel_ids = bank["pixel_id"].value
    # # flatten pixel_ids and get respective indices
    # XX,YY = np.meshgrid(np.arange(pixel_ids.shape[1]),np.arange(pixel_ids.shape[0]))
    # pixel_id_and_indices = np.vstack((pixel_ids.ravel(),XX.ravel(),YY.ravel())).T
    
    # index is event id, value is pixel_id
    # len 587581
    event_id = bank["event_id"].value
    # index is event id, value time
    # len 587581
    time = bank["event_time_offset"].value
    
    bank_name = np.array([bank_number]*len(time))
    data = np.array([bank_name, event_id]).T
    df_tmp = pd.DataFrame(data, index=time, columns=columns)
    df = df.append(df_tmp, ignore_index = True)

df.index = pd.to_timedelta(df.index, unit="us")

#Selection:
df.ix['1970-01-01 00:00:00.023490000':'1970-01-01 00:00:00.023494974']

df.resample("100us")

counts = df.groupby(["bank_number", "pixel_id"]).count()

counts = df.groupby(pd.Grouper(freq='100us'))["bank_number", "pixel_id"]


df.groupby(pd.Grouper(freq='100us')).apply(lambda x: x.groupby(["bank_number", "pixel_id"]).sum())

df.groupby(df.index)["bank_number", "pixel_id"].nunique()

df["conc"] = df.apply(lambda x: x["bank_id"]*100000+x["pixel_d"])
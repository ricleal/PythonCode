#!/usr/bin/env python
from __future__ import print_function

MANTID_BIN_FOLDER_PATH = "/home/rhf/git/mantid/Build/bin"
MANDI_FILE_PATH = "/SNS/MANDI/IPTS-17357/0/5848/NeXus/MANDI_5848_histo.nxs"

import sys
sys.path.append(MANTID_BIN_FOLDER_PATH)
from mantid.simpleapi import *
import pandas as pd

ws = Load(MANDI_FILE_PATH)
instrument = ws.getInstrument()

data = []
for i in range(60):
    bank_name = "bank%s" % (i)
    bank = instrument.getComponentByName(bank_name)
    if bank is not None:
        for j in range(bank.nelements()):
            for k in range(bank[j].nelements()):
                pixel = bank[j][k]
                x = pixel.getPos().X()
                y = pixel.getPos().Y()
                z = pixel.getPos().Z()
                name = pixel.getName()
                data.append([name, bank_name, j, k, x, y, z])

df = pd.DataFrame(data, columns=('name', 'bank_name', 'i', 'j', 'x', 'y', 'z'))
df.to_hdf('/tmp/mandi.hdf', 'mandi')

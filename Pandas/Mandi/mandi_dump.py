import sys
sys.path.append("/SNS/users/rhf/git/mantid/Build/bin")
import pandas as pd

from mantid.simpleapi import *



ws = Load("/SNS/MANDI/IPTS-17357/0/5848/NeXus/MANDI_5848_histo.nxs")
instrument = ws.getInstrument()

data = []
for i in range(60):
	bank_name = "bank%s"%(i)
	print "Getting component %s"%(bank_name)
	bank = instrument.getComponentByName(bank_name)
	if bank is not None:
		for j in range(bank.nelements()):
			for k in range(bank[j].nelements()):
				pixel = bank[j][k]
				x = pixel.getPos().X()
				y = pixel.getPos().Y()
				z = pixel.getPos().Z()
				name = pixel.getName()
				data.append([name,x,y,z])


df = pd.DataFrame(data, columns=('name', 'x', 'y', 'z'))

df.to_hdf('mandi.hdf', 'mandi')
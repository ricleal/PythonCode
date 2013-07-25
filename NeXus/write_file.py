#!/usr/bin/python

'''
Writes a nexus test file (see main below)

This is the simplest format for a TOF instrument

@author: ricardo.leal@ill.fr

Requisites:

- Nexus format library, including python wrappers (nxs): 
http://download.nexusformat.org/doc/html/installation.html

'''

import nxs
import numpy
import datetime

def createsSimpleNexusFile(filename) :

	# creates an HDF5 nexus file (w5 = hdf5)
	nf = nxs.open(filename, "w5") 

	# /entry0
	nf.makegroup("entry0","NXentry")
	nf.opengroup("entry0")

	# /entry0/instrument
	nf.makegroup("instrument","NXinstrument")
	nf.opengroup("instrument")

	# /entry0/instrument/name
	nf.makedata("name",'char',[6])
	nf.opendata("name")
	nf.putdata("TOFTOF")
	nf.closedata()
	nf.closegroup()

	# /entry0/title
	title = "This is the title of the experiment"
	nf.makedata("title",'char',[len(title)])
	nf.opendata("title")
	nf.putdata(title)
	nf.closedata()

	# /entry0/start_time
	now = datetime.datetime.now()
	nowStr = now.strftime('%Y-%m-%dT%H:%M:%S')
	nf.makedata("start_time",'char',[len(nowStr)])
	nf.opendata("start_time")
	nf.putdata(nowStr)
	nf.closedata()


	# /entry0/data
	nf.makegroup("data","NXdata")
	nf.opengroup("data")

	# /entry0/data/data
	data = numpy.arange(5000,dtype='int32').reshape((50,1,100)) # x=number of tubes,y=assuming each tube a single pixel,z=number of time channels
	nf.compmakedata("data",data.dtype,data.shape,'lzw') # compressed data
	nf.opendata('data')
	nf.putattr("signal",1)
	nf.putattr("axes","theta,time_binning")
	nf.putdata(data)
	nf.closedata()

	# /entry0/data/theta
	theta = numpy.arange(50,dtype='float32')
	nf.makedata('theta',theta.dtype,theta.shape) # Non compressed
	nf.opendata('theta')
	nf.putattr("axis",1)
	nf.putattr("units","degree")
	nf.putdata(theta)
	nf.closedata()

	# /entry0/data/time_binning
	time_binning = numpy.arange(100,dtype='float32')
	nf.makedata('time_binning',time_binning.dtype,time_binning.shape) # Non compressed
	nf.opendata('time_binning')
	nf.putattr("axis",2)
	nf.putattr("units","us")
	nf.putdata(time_binning)
	nf.closedata()

	# close /entry/data
	nf.closegroup()

	# /entry0/data/wavelength
	nf.makedata("wavelength",'float32',[1])
	nf.opendata("wavelength")
	nf.putdata(5.12)
	nf.closedata()

	# close file
	nf.close()
	print "Nexus file created:", filename

if __name__ == '__main__':
     createsSimpleNexusFile("/tmp/test.nxs") 
    
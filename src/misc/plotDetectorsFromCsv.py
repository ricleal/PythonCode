'''
Created on Dec 13, 2012

@author: leal

Plot csv files in:

/home/leal/Documents/Mantid/IN5/Detectors

Header:

Index    Spectrum No    Detector ID(s)    R    Theta    Phi    Monitor

'''

import csv
import matplotlib.pyplot as plt


#filename = '/home/leal/Documents/Mantid/IN5/Detectors/after_noheader.csv'

filename = '/home/leal/Documents/Mantid/IN5/Detectors/before_noheader.csv'


def getColumn(filename, column):
    results = csv.reader(open(filename), delimiter=",")
    return [result[column] for result in results]

def plot1():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    dets = getColumn(filename,2)
    r = getColumn(filename,3)
    theta = getColumn(filename,4)
    phi = getColumn(filename,5)
    
    ax.plot(dets,theta,'.',label='theta')
    ax.plot(dets,phi,'x',label='phi')
    
    ax2.plot(dets,r,',',label='r',alpha=0.2)
    
    ax.set_xlabel('Det ID')
    ax.set_ylabel('Angle (degrees)')
    ax2.set_ylabel('meters')
    
    ax.legend(loc= 'upper left')
    ax2.legend(loc= 'upper right')
    
    plt.savefig('in5.png', dpi=120)
    plt.draw()
    
def plot2():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    dets = getColumn(filename,2)
    r = getColumn(filename,3)
    theta = getColumn(filename,4)
    phi = getColumn(filename,5)
    
    start=86000
    dets = dets[start:]
    r = r[start:]
    theta = theta[start:]
    phi = phi[start:]
    
    ax.plot(dets,theta,'.',label='theta')
    ax.plot(dets,phi,'x',label='phi')
    
    ax2.plot(dets,r,',',label='r',alpha=0.2)
    
    ax.set_xlabel('Det ID')
    ax.set_ylabel('Angle (degrees)')
    ax2.set_ylabel('meters')
    
    ax.legend(loc= 'upper left')
    ax2.legend(loc= 'upper right')
    
    plt.savefig('in5_zoom.png', dpi=120)
    plt.draw()

if __name__ == '__main__':
    plot1()
    plot2()
    plt.show()
    
    

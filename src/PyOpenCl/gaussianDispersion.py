'''
Created on Oct 10, 2014

@author: rhf

Based on : https://github.com/HMP1/Cylinder

'''

import numpy as np

class GaussianDispersion(object):
    def __init__(self, npts=35, width=0, nsigmas=3): #number want, percent deviation, #standard deviations from mean
        """
        @param npts: Number of points (0 to npts)
        @param witdh: deviation
        @param sigmas: number of standard deviations from mean
         
        """
        
        self.type = 'gaussian'
        self.npts = npts
        self.width = width
        self.nsigmas = nsigmas
        print("GaussianDispersion: npts=%.2f width=%.2f nsigmas%.2f "%(npts,width,nsigmas))

    def get_pars(self):
        return self.__dict__

    def get_weights(self, center, min, max, relative):
        """
        @param center: is the center of the distribution
        @param min: min allowed value
        @param max: max allowed value
        @param relative: is True if the width is relative to the center instead of absolute
        For polydispersity use relative.  
        For orientation parameters use absolute.     
        """
        npts, width, nsigmas = self.npts, self.width, self.nsigmas
        sigma = width * center if relative else width
        if sigma == 0:
            return np.array([center, 1.], 'd')
        x = center + np.linspace(-nsigmas * sigma, +nsigmas * sigma, npts)
        x = x[(x >= min) & (x <= max)]
        px = np.exp((x-center)**2 / (-2.0 * sigma * sigma))
        print "GaussianDispersion weights:",x.shape,px.shape
        return x, px

def _plot2Axes(x1,x2):
    import numpy as np
    import matplotlib.pyplot as plt
    fig, ax1 = plt.subplots()
    ax1.plot(x1)
    ax2 = ax1.twinx()
    ax2.plot(x2,'r.')
    ax2.set_ylabel('weigths', color='r')
    plt.show()

def test():
    g = GaussianDispersion(100,.1,5)
    value, weight = g.get_weights(70, 0, 1000, True)
    print value, value.shape
    print weight, weight.shape
    _plot2Axes(value,weight)
    
    
    
if __name__=="__main__":
    print "Starting..."
    test()
    print "End!"
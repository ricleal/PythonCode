'''
Created on Oct 10, 2014

@author: rhf

Based on : https://github.com/HMP1/Cylinder

'''

import numpy as np

class GaussianDispersion(object):
    def __init__(self, npts=35, width=0, nsigmas=3): #number want, percent deviation, #standard deviations from mean
        """
        @param npts: Npts = number of points to average over the distribution (0 to npts)
        @param witdh: deviation
        @param sigmas: number of standard deviations from mean
         
        """
        
        self.type = 'gaussian'
        self.npts = npts
        self.width = width
        self.nsigmas = nsigmas
        print("GaussianDispersion: Num points=%d; Deviation percentage=%.2f; Num of deviations from mean=%d"%(npts,width,nsigmas))

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

   
    
def plotValuesAndWeights(x1,x2,**kwargs):
    import matplotlib.pyplot as plt
    plt.plot(x1,x2,".")
    plt.title(str(kwargs), fontsize=10)
    plt.ylabel('Weight')    
    plt.xlabel('Value')    
    plt.show()


def test():
    kwargs1 = dict(npts=100, width=0.1, nsigmas=3)
    g = GaussianDispersion(**kwargs1)
    
    kwargs2 = dict(center=70, min=0, max=1000, relative=True)
    value, weight = g.get_weights(**kwargs2)
    #print value, value.shape
    #print weight, weight.shape
    kwargs = dict(kwargs1.items() + kwargs2.items() )
    plotValuesAndWeights(value, weight, **kwargs)
        
if __name__=="__main__":
    print "Starting..."
    test()
    print "End!"
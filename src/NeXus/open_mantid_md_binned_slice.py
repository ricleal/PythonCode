'''
Created on Oct 29, 2013

@author: leal
'''

import nxs
import time
import numpy as np
import pylab as plt
plt.switch_backend('macosx')
#import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm

partial_time = time.time()
start_time = time.time()

def timeit():
  global partial_time
  now = time.time()
  diff_total = now - start_time
  diff_partial = now - partial_time
  partial_time = time.time()
  print '**** Time: last: %dm %ds :: total: %dm %ds' % (int(diff_partial // 60),
    int(diff_partial % 60), int(diff_total // 60), int(diff_total % 60))


class NexusReader(object):
    '''
    Functions to a read a nexus file
    '''


    def __init__(self, filepath):
        '''
        Constructor
        '''
        self.filepath = filepath
        self.data = None
    def isValid(self):
        try :
            fp = nxs.open(self.filepath,'r')
            fp.close()
        except Exception:
            return False
        return True
    
    def readData(self):
        f = nxs.open(self.filepath)
        f.opengroup('MDHistoWorkspace')

        f.opendata('signal')
        self.data = f.getdata()
        f.closedata()

        self.qs = self.read_axes(f)

        f.closegroup()
        f.close()
    
    def read_axes(self, nexus_handler):
        qs = []
        for q in "Q1,Q2,Q3".split(","):
            nexus_handler.opendata(q)
            #setattr(self, q, nexus_handler.getdata())
            qs.append(nexus_handler.getdata())
            nexus_handler.closedata()
        return qs
        
        
    
    def cast_data(self,target='float16'):
        self.data = self.data.astype(target)
    
    def trim_faces(self, threshold = 0.1):
        def get_face(M, dim, front_side):
            if front_side:
                side = 0
            else:
                side = -1
            index = tuple(side if i == dim else slice(None) for i in range(M.ndim))
            return M[index]
        
        def remove_face(M, dim, front_side):
            if front_side:
                dim_slice = slice(1, None)
            else:
                dim_slice = slice(None, -1)
            index = tuple(dim_slice if i == dim else slice(None) for i in range(M.ndim))
            return M[index]
        
        def iter_faces(M):
            for dim in range(M.ndim):
                for front_side in (True, False):
                    yield get_face(M, dim, front_side)

        def chop_recursive(M):
            #print "M shape", M.shape
            for dim in range(self.data.ndim):
                for front_side in (True, False):
                    this_face = get_face(M, dim, front_side)
                    this_face_has_element_higher_than_treshold = False
                    #print "---->", np.max(this_face), np.min(this_face)                    
                    if np.max(this_face) > threshold:
                        this_face_has_element_higher_than_treshold = True
                        break;
                    if not this_face_has_element_higher_than_treshold:
                        M = remove_face(M, dim, front_side)
                        M = chop_recursive(M)
            return M
                    
        M = self.data
        M = chop_recursive(M)
        self.data = M
    
    def plot_it(self):
        d = self.data[:,:,180]
        d[d<0.2]=0
        im = plt.imshow(d, cmap='hot')
        plt.colorbar(im, orientation='horizontal')
        plt.show()

class plotter:
    def __init__(self, im, i=0):
        self.im = im
        self.i = i
        self.vmin = im.min()
        self.vmax = im.max()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        
        self.fig.canvas.mpl_connect('key_press_event',self.hande_event)
        #self.fig.canvas.mpl_connect('key_press_event', self.print_event)
        self.draw()
        #self.cb = self.fig.colorbar(self.cax)
        #self.cb2 = self.fig.colorbar(self.cax2)
        
        plt.show()
    
    def draw(self):
        
        if self.im.ndim is 2:
            im = self.im
        if self.im.ndim is 3:
            print 'Drawing...', self.i
            im = self.im[...,self.i]
            self.ax.set_title('Linear %s'%self.i)
            self.ax2.set_title('Log %s'%self.i)
            
        self.cax = self.ax.imshow(im,  interpolation='nearest', cmap=cm.jet,  vmin=self.vmin,  vmax=self.vmax)
        self.cax2 = self.ax2.imshow(im,  interpolation='nearest', cmap=cm.jet,  norm=LogNorm(vmin=0.01,  vmax=1))
        #self.cax2 = self.ax2.matshow(im, cmap=cm.rainbow, norm=LogNorm(vmin=0.01,  vmax=1))
                
    def print_event(self,event):
        print event

    def hande_event(self, event):
        old_i = self.i
        if event.key=='right':
            self.i = min(self.im.shape[2]-1, self.i+1)
        elif event.key == 'left':
            self.i = max(0, self.i-1)
        if old_i != self.i:
            self.draw()
            self.fig.canvas.draw()

def slice_show(im, i=0):
    plotter(im, i)
                            
if __name__ == '__main__':
    timeit()
    filepath = '/Users/rhf/Dropbox (ORNL)/data/mde_test_bin.nxs'
    n1 = NexusReader(filepath=filepath)
    print 'n1 is valid?', n1.isValid()
    timeit()
    n1.readData()
    timeit()
    print n1.data.shape
    print n1.data.dtype
    
    n1.cast_data()
    timeit()
    print n1.data.dtype
    
    print "Before chop:", n1.data.shape
    #n1.trim_faces(threshold=0.5)
    timeit()
    print "After chop:", n1.data.shape
    
    #n1.plot_it()
    slice_show(n1.data,245)
    timeit()
    print 30*"*", " READY ", 30*"*"
    
    

'''
Created on Oct 29, 2013

@author: leal
'''

import nxs
import time
import numpy as np
import mayavi.mlab as mlab

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
        #f.opengroup('signal')
        f.opendata('signal')
        self.data = f.getdata()
        f.closedata()
        #f.closegroup()
        f.closegroup()
        f.close()
    
    def cast_data(self,target='float16'):
        self.data = self.data.astype(target)
    
    def plotFancy(self):
        if self.data is not None:
            a = self.data
            src = mlab.pipeline.scalar_field(a)
            mlab.pipeline.iso_surface(src, contours=[a.min() + 0.1 * a.ptp(), ], opacity=0.1)
            mlab.pipeline.iso_surface(src, contours=[a.max() - 0.1 * a.ptp(), ],)
            mlab.pipeline.image_plane_widget(src,
                                             plane_orientation='z_axes',
                                             slice_index=len(a[0,0,:])/2,) 


    def plotData3D(self):
        if self.data is not None:
            a = self.data
            #mlab.pipeline.volume(mlab.pipeline.scalar_field(a))
            mlab.pipeline.volume(mlab.pipeline.scalar_field(a), vmin=0.3, vmax=1)
    
    def plotContour(self):
        if self.data is not None:
            a = self.data
            #mlab.pipeline.volume(mlab.pipeline.scalar_field(a))
            mlab.contour3d(a, contours=8, opacity=0.3, vmin=0.3, vmax=1)
    
    def plotCutPlanes(self):
        if self.data is not None:
            s = self.data
            mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                                    plane_orientation='x_axes',
                                    slice_index=100,
                                )
            mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                                    plane_orientation='y_axes',
                                    slice_index=100,
                                )
            mlab.outline()
    
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
        

        
            
if __name__ == '__main__':
    timeit()
    filepath = '/home/rhf/Dropbox (ORNL)/data/mde_test_bin.nxs'
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
    
    n1.plotAll()
    timeit()
    mlab.show()
    
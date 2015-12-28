import nxs
import time
import numpy as np
import matplotlib.pyplot as plt
import os

FILEPATH = "/SNS/MANDI/IPTS-12697/0/4089/NeXus/MANDI_4089_event.nxs"
OUTPUTPATH = "/tmp"

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
    
    def plot_data_as_images(self, normalise=True):
        f = nxs.open(self.filepath)
        f.opengroup('entry')
        
        if normalise:
            sum = self.get_monitor_counts(f)
        else:
            sum = 1
        entries = f.getentries()
        banks = [ key for key, value in entries.items() if value == 'NXdata']
        for bank in banks:
            f.opengroup(bank)
            f.opendata('data_x_y')
            data = f.getdata()
            
            data = data/np.float32(sum)*sum
            
            self.save_as_plot(data,bank)
            
            f.closedata()
            f.closegroup()

        f.closegroup()
        f.close()

    def get_monitor_counts(self, f, monitor_entry_name = 'monitor1'):
        f.opengroup(monitor_entry_name)
        f.opendata('data')
        data = f.getdata()
        sum = np.sum(data)
        f.closedata()
        f.closegroup()
        return sum
    
    def save_as_plot(self,data,filename,outputpath=OUTPUTPATH, framed=True):
        out_path = os.path.join(OUTPUTPATH, filename+'.png')
        print "Saving:", out_path
        if framed:
            plt.clf()
            plt.imshow(data)
            plt.colorbar()
            plt.savefig(out_path)
        else:
            fig = plt.figure(frameon=False)              
            ax = plt.Axes(fig, [0., 0., 1., 1.])
            ax.set_axis_off()
            fig.add_axes(ax)
            ax.imshow(data, aspect='auto')
            fig.savefig(out_path,bbox_inches='tight')
        
        
        
        

if __name__ == '__main__':
    n = NexusReader(FILEPATH)
    n.plot_data_as_images()
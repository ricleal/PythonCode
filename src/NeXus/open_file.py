'''
Created on Oct 29, 2013

@author: leal
'''

import nxs

class NexusReader(object):
    '''
    Functions to a read a nexus file
    '''


    def __init__(self, filepath):
        '''
        Constructor
        '''
        self.filepath = filepath
    
    def isValid(self):
        try :
            fp = nxs.open(self.filepath,'r')
            fp.close()
        except Exception:
            return False
        return True
   
if __name__ == '__main__':
    filepath = '/net/serdon/illdata/data/in5/internalUse/rawdata/110877.nxs'
    n1 = NexusReader(filepath=filepath)
    print 'n1 is valid?', n1.isValid()
    filepath = '/net/serdon/illdata/data/in4/internalUse/rawdata/073123'
    n1 = NexusReader(filepath=filepath)
    print 'n1 is valid?', n1.isValid()
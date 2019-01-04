import os
import h5py
import numpy as np
import getpass

from datetime import datetime

class Log(object):

    def __init__(self, filename="reduction.log", path=os.getcwd()):
        '''
        Opens the file handler

        os.path.dirname(os.path.abspath( __file__ ))
        '''
        print("Saving the file to", path)
        self._fh = h5py.File(os.path.join(path, filename), 'w')
        self._initial_setup()
    
    def __del__(self):
        self._fh.close()

    def _initial_setup(self):
        '''
        Stuff that goes into the file and it's independent of the data itself
        '''
        self._fh.attrs[u'timestamp'] = datetime.now().isoformat()
        self._fh.attrs[u'username'] = getpass.getuser()
        self._fh.attrs[u'mantid_version'] = 3.4 # TODO
    



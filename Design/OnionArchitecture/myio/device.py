from .core.low_level_io import read_from_device, write_to_device

class Device(object):
    '''
    Abstract class
    '''
    def __init__(self, id):
        self.id = id
        print("Init device with ID:", id)

    def read(self):
        read_from_device(self.id)

    def write(self, value):
        write_to_device(self.id)

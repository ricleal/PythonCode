class Device(object):
    '''
    Abstract class
    '''
    def __init__(self, id):
        print("Init device with ID:", id)

    def read(self):
        raise NotImplementedError

    def write(self, value):
        raise NotImplementedError

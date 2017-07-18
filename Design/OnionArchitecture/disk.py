from myio.device import Device


class Disk(Device):

    def __init__(self, id):
        super().__init__(id)
        print('Init Disk...')

    def read(self):
        print('Reading from the Disk...')

    def write(self, value):
        print('Writing to the Disk:', value)

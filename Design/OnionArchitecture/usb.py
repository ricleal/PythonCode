from myio.device import Device


class Usb(Device):

    def __init__(self, id):
        super().__init__(id)
        print('Init Usb...')

    def read(self):
        print('Reading from the Usb...')
        super().read()

    def write(self, value):
        print('Writing to the Usb:', value)
        super().write(value)
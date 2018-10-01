from collections import OrderedDict
import time

class MyOrderedDict(OrderedDict):

    def _set_value(value):
        if type(value) == str
    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, {
            "value": value,
            "timestamp": time.time()})
    
    def __getitem__(self,key):
        value = OrderedDict.__getitem__(self, key)
        return value['value']

d = MyOrderedDict()
d['my_key'] = 'my_value'

print(d)
print(d['my_key'])
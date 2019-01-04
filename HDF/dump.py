#!/usr/bin/env python3

import h5py
import numpy as np
from faker import Faker

filename = "/tmp/test.h5"
fake = Faker('en_US')
fake.seed(123)


def generate_dummy_dict(n=10):
    return {fake.name(): fake.msisdn() for _ in range(n)}


f = h5py.File(filename, 'w')
f.attrs[u'default'] = u'entry'
f.attrs[u'file_name'] = filename

# Create a group
group = f.create_group("Metadata")
group.attrs[u'metadata'] = u'degrees'

# Create datasets with pairs of fake.name() : fake.msisdn()
for k, v in generate_dummy_dict().items():
    ds = group.create_dataset(k, data=np.array(
        list(map(int, v))))  # Array of digits

# Read back the datasets
for i in group.items():
    print(i)
    data_as_array = np.array(i[1])
    print(" -> ", data_as_array)

f.close()

#!/usr/bin/env python

import datetime
import json
import numpy as np
import time

'''
Produces dummy json data
every interval_seconds
'''

interval_seconds = 1

if __name__ == '__main__':
    while(True):
        data = dict(
            date = str(datetime.datetime.now()),
            data = np.random.random_sample(10).tolist(),
        )
        print json.dumps(data)
        time.sleep(interval_seconds)

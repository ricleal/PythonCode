#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Blaze odo:
http://odo.pydata.org/en/latest/index.html

Format json:
cat usage.json | python -m json.tool


Json generator:
http://www.json-generator.com/

'''

from odo import odo
import pandas as pd
import matplotlib.pylab as plt

FILENAME = 'usage.json'

df = odo(FILENAME, pd.DataFrame)

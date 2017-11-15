from __future__ import print_function

import base64
import re
from io import BytesIO
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams

# icon size
rcParams['figure.figsize'] = 1, 1


def parse(filename):
    '''
    '''
    col_x, col_y, headers, data = None, None, [], []
    with open(filename) as f:
        lines = f.readlines()
        line_cycle = cycle(lines)
        line = next(line_cycle)
        while "scan completed" not in line:
            if line.startswith('# def_x'):
                _, col_x = line.split('=')
            elif line.startswith('# def_y'):
                _, col_y = line.split('=')
            elif line.startswith('# col_headers'):
                line = next(line_cycle)
                headers = line.split()
                headers.remove('#')
                line = next(line_cycle)
                while not line.startswith('#'):
                    # string to array of int/float
                    data.append(
                        list(map(float, re.findall(r'\d*\.?\d+', line))))
                    line = next(line_cycle)
            line = next(line_cycle)
    return(col_x.strip(), col_y.strip(), headers, data)  


def plot(col_x, col_y, headers, data):
    '''
    '''
    data_array = np.array(data)
    data_array = np.core.records.fromarrays(
        data_array.transpose(),
        names=headers,
    )
    plt.plot(data_array[col_x], data_array[col_y])
    # Hide axis values
    plt.xticks([])
    plt.yticks([])

    figfile = BytesIO()
    plt.savefig(figfile, format='svg')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())

    with open('/tmp/test.html', 'w') as f:
        f.write('''<html>
            <img src="data:image/svg+xml;base64,{}" />
        </html>'''.format(figdata_png.decode('ascii')))


if __name__ == '__main__':
    col_x, col_y, headers, data = parse('data.dat')
    plot(col_x, col_y, headers, data)

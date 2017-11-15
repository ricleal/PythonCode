from __future__ import print_function

import base64
import re
from io import BytesIO
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams
from glob import glob

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
        while "scan completed" not in line and "scan stopped" not in line:
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
    plt.figure()
    plt.plot(data_array[col_x], data_array[col_y])
    # Hide axis values
    plt.xticks([])
    plt.yticks([])

    figfile = BytesIO()
    plt.savefig(figfile, format='svg')
    figfile.seek(0)
    figdata_svg = base64.b64encode(figfile.getvalue())
    plt.close()
    return figdata_svg


def save_thumbnail(figdata_svg, filename_out='/tmp/test.html'):
    with open(filename_out, 'w') as f:
        f.write('''<html>
            <img src="data:image/svg+xml;base64,{}" />
        </html>'''.format(figdata_svg.decode('ascii')))


def save_thumbnails(figdata_svgs, filename_out='/tmp/test_multiple.html'):
    with open(filename_out, 'w') as f:
        f.write('<html>')
        for img in figdata_svgs:
            f.write('<img src="data:image/svg+xml;base64,{}" /><br/>\n'.format(img.decode('ascii')))
        f.write('</html>')

def plot_1(filename):
    col_x, col_y, headers, data = parse(filename)
    figdata_svg = plot(col_x, col_y, headers, data)
    save_thumbnail(figdata_svg)

def plot_multiple(path):
    filenames = glob(path)
    figdata_svgs = []
    for filename in filenames:
        try:
            print("Processing {}...".format(filename))
            col_x, col_y, headers, data = parse(filename)
            figdata_svg = plot(col_x, col_y, headers, data)
            figdata_svgs.append(figdata_svg)
        except Exception:
            print("Error processing {}...".format(filename))
    save_thumbnails(figdata_svgs)

if __name__ == '__main__':
    # plot_1('data.dat')
    plot_multiple('/HFIR/HB1/exp469/Datafiles/*.dat')

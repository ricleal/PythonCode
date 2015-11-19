#!/usr/bin/env python

"""

Curves y1 and y2

Finds K (scale factor) to superimpose these 2 curves!)

"""
import sys
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.optimize import leastsq

def residuals(p, x, f_target, f_to_optimise):
    """
    
    """
    k,b = p
    err = f_target(x)-(k*f_to_optimise(x)-b)
    return err

def peval(x,f,p):
    k,b = p
    return k*f(x)-b

def main(glob_pattern):
    files = glob.glob(glob_pattern)
    if len(files) == 0:
        print "No files found!"
        return
    dfs = []
    for file in files:
        df = pd.read_csv(file, skiprows=[1])
        df.insert(0, "ylog", np.log(df[' Y ']))
        plt.plot(df['# X '],df['ylog'],label=file)
        print file, df.shape, df.columns
        #print df[' Y ']
        dfs.append(df)
    
    # find reference DS
    maxs =[]
    for df in dfs:
        maxs.append(np.max(df[' Y ']))
    df_with_max_value = np.argmax(maxs)
    print "Reference:", df_with_max_value, files[df_with_max_value]
    
    
    # Find X range 
    mins =[]
    maxs = []
    for df in dfs:
        mins.append(np.min(df['# X ']))
        maxs.append(np.max(df['# X ']))
    x_range = [np.max(mins), np.min(maxs)]
    print "X range:",  x_range
    
    x = np.linspace(x_range[0], x_range[1], 100)
    
    # Interpolate functions
    fs = []
    for df in dfs:
        #f = interpolate.interp1d(df['# X '], df["ylog"])
        f = interpolate.interp1d(df['# X '], df[" Y "])
        fs.append(f)
    
    plt.legend(loc=1)
    plt.figure("Fits")
    # Let's get the scale factors
    for idx,(df,f,file) in enumerate(zip(dfs,fs,files)):
        
        if idx == df_with_max_value:
            plt.plot(x,f(x),label=file)
        else:
            plsq = leastsq(residuals, [1,1], args=(x,fs[df_with_max_value],f))
            print "plsq [k,b] =",plsq[0]
            plt.plot(x,peval(x,f,plsq[0]), '-', label='%s %s'%(file,plsq[0]))
        
    plt.legend(loc=1)
    plt.show()
    

if __name__ == "__main__":
    print len(sys.argv)
    if len(sys.argv) != 2:
        print "Use %s '*.txt'"%sys.argv[0]
    else:
        main(sys.argv[1])
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
from pprint import pprint
def residuals(p, x, f_target, f_to_optimise):
    """
    
    """
    k,b = p
    err = f_target(x)-(k*f_to_optimise(x)-b)
    return err

def peval(x,f,p):
    k,b = p
    return k*f(x)-b


def new_plot(dfs,col_names,labels,title):
    plt.figure(title)
    for (df,label) in zip(dfs,labels):
        plt.plot(df[col_names[0]],df[col_names[1]],label=label)
    plt.legend(loc=1)

def new_plot_log(dfs,col_names,labels,title):
    plt.figure(title)
    for (df,label) in zip(dfs,labels):
        plt.loglog(df[col_names[0]],df[col_names[1]],label=label)
    plt.grid(True,which="both")
    plt.legend(loc='lower left')
    

def main(glob_pattern):
    files = glob.glob(glob_pattern)
    if len(files) == 0:
        print "No files found!"
        return
    dfs = []
    for file in files:
        df = pd.read_csv(file, skiprows=[0,1], names=['X', 'Y', 'E', 'DX'])
        print file, df.shape, df.columns
        df.insert(len(df.columns), "xlog", np.log(df['X']))
        df.insert(len(df.columns), "ylog", np.log(df['Y']))
        dfs.append(df)
    
    new_plot(dfs,['X','Y'],files,"Linear")
    new_plot_log(dfs,['X','Y'],files,"Log")
    
    # find reference DS
    maxs =[]
    for df in dfs:
        maxs.append(np.max(df['Y']))
    df_with_max_value = np.argmax(maxs)
    print "Reference:", df_with_max_value, files[df_with_max_value]
    
    
    # Find X range 
    mins =[]
    maxs = []
    for df in dfs:
        # X minimum when Y > 0
        mins.append(np.min(df.loc[df['Y']>0,['X']]))
        maxs.append(np.max(df['X']))
    x_range = [np.max(mins), np.min(maxs)]
    print "X range:",  x_range
    
    x = np.linspace(x_range[0], x_range[1], 200)
    #x = np.linspace(0.010, 0.12, 100)
    
    
    # Interpolate functions
    fs = []
    for df in dfs:
        #f = interpolate.interp1d(df['X'], df["Y"])
        f = interpolate.interp1d(df['X'], df["Y"])
        fs.append(f)
    
    
    fig_linear = plt.figure("Fits Linear")
    ax_linear = fig_linear.add_subplot(111)
    fig_log = plt.figure("Fits Log")
    ax_log = fig_log.add_subplot(111)
    
    # Let's get the scale factors
    for idx,(df,f,file) in enumerate(zip(dfs,fs,files)):
        if idx == df_with_max_value:
            ax_linear.plot(x,f(x),label=file + " (Ref)")
            ax_log.plot(np.log(x),np.log(f(x)),label=file + " (Ref)")
        else:
            plsq, cov, infodict,mesg,ier = leastsq(residuals, [1,-1], args=(x,fs[df_with_max_value],f),full_output=True)
            print "Solution Found!" if ier in [1, 2, 3,4] else "Solution NOT Found!"
            print "\t", file, ": [K,b] =",plsq
            print "\tErrors for [K,b] =", np.sqrt(np.diag(cov))
            ax_linear.plot(x,peval(x,f,plsq), '-', label='%s K=%.2f b=%.2f'%(file,plsq[0],plsq[1]))
            ax_log.loglog(x,peval(x,f,plsq), '-', label='%s K=%.2f b=%.2f'%(file,plsq[0],plsq[1]))
    ax_linear.legend(loc=1)
    ax_log.grid(True,which="both")
    ax_log.legend(loc='lower left')
    
    plt.show()
    

if __name__ == "__main__":
    print len(sys.argv)
    if len(sys.argv) != 2:
        print "Use %s '*.txt'"%sys.argv[0]
    else:
        main(sys.argv[1])
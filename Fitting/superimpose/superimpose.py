#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Finds K (scale factor) + b to superimpose these 2 curves!)

I(scaled) = f * I(original) – b 

Needs packages:
pandas
scipy
matplotlib
numpy
tabulate

"""
from settings import logger, args, config

import sys
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import scipy.optimize as optimize
from pprint import pprint
from tabulate import tabulate
from operator import itemgetter



def residuals(p, x, f_target, f_to_optimise):
    """
    
    """
    k,b = p
    err = f_target(x)-(k*f_to_optimise(x)-b)
    #return np.sum(err**2)
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
    

def main(argv):
    
    reference = args['reference']
    files = glob.glob(args['input'])
    if len(files) == 0:
        logger.error("No files found!")
        return
    # Reference:
    if reference not in files:
        files.append(reference)
    files = sorted(files)
    reference_idx = files.index(reference)
    logger.debug("Reference: %s (%s)"%(reference, reference_idx))
    
    
    dfs = []
    for file in files:
        df = pd.read_csv(file, skiprows=[0,1], names=['X', 'Y', 'E', 'DX'])
        logger.debug("%s %s %s" % (file, df.shape, df.columns.values))
        dfs.append(df)
    
    new_plot(dfs,['X','Y'],files,"Linear")
    new_plot_log(dfs,['X','Y'],files,"Log")
    
    # Find X range 
    mins =[]
    maxs = []
    for df in dfs:
        # X minimum when Y > 0
        mins.append(np.min(df.loc[df['Y']>0,['X']]))
        maxs.append(np.max(df['X']))
    x_min = np.max(mins)
    x_max = np.min(maxs)
    q_min = args['qmin']
    q_max = args['qmax']
    if q_min > x_min:
        x_min = q_min
    if q_max < x_max:
        x_max = q_max
    x = np.linspace(x_min, x_max, 200)
    logger.info("Q range: %.4f - %.4f"%(x_min,x_max))
    
    # Interpolate functions
    fs = []
    for df in dfs:
        f = interpolate.interp1d(df['X'], df['Y'])
        fs.append(f)
    
    
    fig_linear = plt.figure("Fits Linear")
    ax_linear = fig_linear.add_subplot(111)
    fig_log = plt.figure("Fits Log")
    ax_log = fig_log.add_subplot(111)
    
    table = []
    # Let's get the scale factors
    for idx,(df,f,file) in enumerate(zip(dfs,fs,files)):
        if idx == reference_idx:
            ax_linear.plot(x,f(x),label=file + " (Ref)")
            ax_log.plot(np.log(x),np.log(f(x)),label=file + " (Ref)")
            table.append([file,0,0,0,0])
        else:
            plsq, cov, infodict,mesg,ier = optimize.leastsq(residuals, [1,1], args=(x,fs[reference_idx],f),full_output=True)
            logger.debug("Solution Found for %s. %s"%(file,mesg)) if ier in [1, 2, 3,4] else logger.warning("Solution NOT Found for %s. %s"%(file,mesg))
            errors = np.sqrt(np.diag(cov))
            y = peval(x,f,plsq)
            ax_linear.plot(x,y, '-', label='%s K=%.2f b=%.2f'%(file,plsq[0],plsq[1]))
            ax_log.set_xlim(x[0],x[-1])
            ax_log.loglog(x,y, '-', label='%s K=%.2f b=%.2f'%(file,plsq[0],plsq[1]))
            table.append([file,plsq[0],errors[0],plsq[1],errors[1]])
    ax_linear.legend(loc=0)
    ax_log.grid(True,which="both")
    ax_log.legend(loc=0)#'lower left')
    
    logger.info( "\n%s" % tabulate(sorted(table, key=itemgetter(0)), headers=["File","K", "Err(K)","b","Err(b)"], floatfmt=".4f") )
    
    plt.show()
    

if __name__ == "__main__":
    main(sys.argv)
    logger.info("Done!")
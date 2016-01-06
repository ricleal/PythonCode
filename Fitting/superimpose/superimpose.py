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

def create_dataframes(files, headers=['X', 'Y', 'E', 'DX']):
    '''
    Parses the CSV files into Pandas Dataframes
    @param headers: List of headers present in the file 
    @return: list of dataframes
    '''
    dfs = []
    for file in files:
        df = pd.read_csv(file, skiprows=[0,1], names=headers)
        logger.debug("File: %s; Shape: %s; Header: %s" % (file, df.shape, df.columns.values))
        dfs.append(df)
    return dfs

def find_q_range(dfs, n_points = 200):
    '''
    Loop over all dataframes, find mins and maxs
    and find a :
        common minimal (max of all minimums)
        common maximal (min of all maximums)
    Creates a range of n_points within those limits
    @param dfs : list of pandas dataframes
    @return: Q range formed by n_points
    '''
    
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
    x = np.linspace(x_min, x_max, n_points)
    logger.info("Using Q range: %.4f - %.4f"%(x_min,x_max))
    return x

def create_interpolate_functions(dfs, x_header='X', y_header='Y'):
    '''
    For a list of pandas data frames, for every dataframe, gets
    an interpolate function for 2 given collumns x and y
    @return: list of interpolate functions 
    '''
    fs = []
    for df in dfs:
        f = interpolate.interp1d(df[x_header], df[y_header])
        fs.append(f)
    return fs;
    

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
    
    # Put the file content in dataframes
    dfs = create_dataframes(files)

    # Let's plot the raw data
    new_plot(dfs,['X','Y'],files,"Linear")
    new_plot_log(dfs,['X','Y'],files,"Log")
    
    # Interpolate functions
    interpolate_functions = create_interpolate_functions(dfs)
    
    # Find a common q_range for all data sets 
    q_range = find_q_range(dfs)
    
    # Fitting    
    fig_linear = plt.figure("Fits Linear")
    ax_linear = fig_linear.add_subplot(111)
    fig_log = plt.figure("Fits Log")
    ax_log = fig_log.add_subplot(111)
    
    table = []
    # Let's get the scale factors
    for idx,(df,interpolate_function,filename) in enumerate(zip(dfs,interpolate_functions,files)):
        if idx == reference_idx:
            ax_linear.plot(q_range,interpolate_function(q_range),label=filename + " (Ref)")
            ax_log.plot(np.log(q_range),np.log(interpolate_function(q_range)),label=filename + " (Ref)")
            table.append([filename,0,0,0,0])
        else:
            plsq, cov, infodict,mesg,ier = optimize.leastsq(residuals, [1,1], 
                                                            args=(q_range,interpolate_functions[reference_idx],interpolate_function),full_output=True)
            logger.debug("Solution Found for %s. %s"%(filename,mesg)) if ier in [1, 2, 3,4] else logger.warning("Solution NOT Found for %s. %s"%(filename,mesg))
            errors = np.sqrt(np.diag(cov))
            y = peval(q_range,interpolate_function,plsq)
            ax_linear.plot(q_range,y, '-', label='%s K=%.2f b=%.2f'%(filename,plsq[0],plsq[1]))
            ax_log.set_xlim(q_range[0],q_range[-1])
            ax_log.loglog(q_range,y, '-', label='%s K=%.2f b=%.2f'%(filename,plsq[0],plsq[1]))
            table.append([filename,plsq[0],errors[0],plsq[1],errors[1]])
    ax_linear.legend(loc=0)
    ax_log.grid(True,which="both")
    ax_log.legend(loc=0)#'lower left')
    
    logger.info( "\n%s" % tabulate(sorted(table, key=itemgetter(0)), headers=["File","K", "Err(K)","b","Err(b)"], floatfmt=".4f") )
    
    plt.show()
    

if __name__ == "__main__":
    main(sys.argv)
    logger.info("Done!")
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
import os.path


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


def plot_dataframes(dfs,headers,labels,title,plot_type='linear'):
    '''
    Plot a list of dataframes.
    @param headers: must be a list of 2 items with valid dataframe headers: ['X','Y']
    @param labels: Labels to use in the plot legend. Same length as list of dataframes. 
    @param plot_type: either linear or log
    new_plot(dfs,['X','Y'],filenames,"Linear")
    '''
    fig = plt.figure(title)
    ax = fig.add_subplot(111)
    for (df,label) in zip(dfs,labels):
        if plot_type is 'linear':
            ax.plot(df[headers[0]],df[headers[1]],label=label)
        else:
            ax.loglog(df[headers[0]],df[headers[1]],label=label)
    ax.grid(True,which="both")
    ax.legend(loc='best')
    return ax
    
def create_dataframes(filenames, headers=['X', 'Y', 'E', 'DX']):
    '''
    Parses the CSV files into Pandas Dataframes
    @param headers: List of headers present in the file 
    @return: list of dataframes
    '''
    dfs = []
    for filename in filenames:
        df = pd.read_csv(filename, skiprows=[0,1], names=headers)
        df.filename = filename
        df.fullpath = os.path.abspath(filename)
        logger.debug("File: %s; Shape: %s; Header: %s" % (df.fullpath, df.shape, df.columns.values))
        dfs.append(df)
    return dfs

def discard_points(dfs,begin,end):
    '''
    Remove from the list of dataframes
    the first and last n points
    @param begin: n points to remove at the beginning
    @param end: n points to remove at the end
    '''
    for df in dfs:
        if begin > 0:
            df.drop(df.index[0:begin],inplace=True)
        if end > 0:
            df.drop(df.index[-end:],inplace=True)
        logger.debug("File: %s; New Shape: %s." % (df.filename, df.shape))
    return dfs

def save_as_csv(dfs,suffix='_scaled.csv'):
    for df in dfs:
        file_path_prefix, _ = os.path.splitext(df.fullpath)
        csv_path = file_path_prefix + suffix
        df.to_csv(csv_path)
        logger.debug("CSV File saved to %s"%csv_path)
    return dfs
    

def find_q_range(dfs):
    '''
    Loop over all dataframes, find mins and maxs
    and find a :
        common minimal (max of all minimums)
        common maximal (min of all maximums)
    @param dfs : list of pandas dataframes
    @return: Q range [min,max]
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
    return x_min,x_max

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


def fit(x, f_target, f_to_optimise, guess = [1,1]):
    '''
    '''
    plsq, cov, infodict, mesg, ier = optimize.leastsq(residuals, guess, 
                                                     args=(x,f_target, f_to_optimise),full_output=True)
    return plsq, cov, mesg
            
def append_fit_to_dfs(dfs, reference_idx, interpolate_functions):
    '''
    Fit all datasets to the reference
    @return: fitting params and the covariance matrix 
    '''
    plsqs = []
    covs = []
    q_min,q_max = find_q_range(dfs) 
    for idx,(df,interpolate_function) in enumerate(zip(dfs,interpolate_functions)):
        logger.debug("***** Fitting %s"%df.filename)
        # Find a common q_range for all data sets 
        q_range = np.linspace(q_min, q_max, len(df.index))        
        if idx != reference_idx:            
            plsq, cov, mesg = fit(q_range,interpolate_functions[reference_idx],interpolate_function)
            logger.info(mesg)
            y = peval(q_range,interpolate_function,plsq)                        
            df['q_range'] = pd.Series(q_range, index=df.index)
            df['y_range_fit'] = pd.Series(y, index=df.index)
            y = peval(df['X'],interpolate_function,plsq)
            df['y_fit'] = pd.Series(y, index=df.index)
            plsqs.append(plsq)
            covs.append(cov)
        else:
            df['q_range'] = pd.Series(q_range, index=df.index)
            y = interpolate_function(q_range)
            df['y_range_fit'] = pd.Series(y, index=df.index)
            y = interpolate_function(df['X'])
            df['y_fit'] = pd.Series(y, index=df.index)
            plsqs.append(None)
            covs.append(None)
    return plsqs, covs

def create_summary_table(plsqs, covs, filenames):
    table = []
    for plsq, cov,filename in zip(plsqs, covs,filenames):
        if plsq is None or cov is None:
            table.append([filename,0,0,0,0])
        else:
            errors = np.sqrt(np.diag(cov))
            table.append([filename,plsq[0],errors[0],plsq[1],errors[1]])
    logger.info( "\n%s" % tabulate(sorted(table, key=itemgetter(0)), headers=["File","K", "Err(K)","b","Err(b)"], floatfmt=".4f") )
    return table

def main(argv):
    
    reference_filename = args['reference']
    filenames = glob.glob(args['input'])
    if len(filenames) == 0:
        logger.error("No files found!")
        return
    # Reference:
    if reference_filename not in filenames:
        filenames.append(reference_filename)
    filenames = sorted(filenames)
    reference_idx = filenames.index(reference_filename)
    logger.debug("Reference: %s (%s)"%(reference_filename, reference_idx))
    
    # Put the file content in dataframes
    dfs = create_dataframes(filenames)

    dfs = discard_points(dfs,args['discard_begin'],args['discard_end'])
    
    # Let's plot the raw data   
    plot_dataframes(dfs,['X','Y'],filenames,"Raw Linear")
    plot_dataframes(dfs,['X','Y'],filenames,"Raw Log",plot_type='log')
    
    # Interpolate functions
    interpolate_functions = create_interpolate_functions(dfs)
    
    # Fitting!
    plsqs, covs = append_fit_to_dfs(dfs, reference_idx, interpolate_functions,)
    
    # Plot results
    plot_dataframes(dfs,['q_range','y_range_fit'],filenames,"Fit Linear Q Range")
    plot_dataframes(dfs,['q_range','y_range_fit'],filenames,"Fit Log Q Range", plot_type='log')

    plot_dataframes(dfs,['X','y_fit'],filenames,"Fit Linear")
    plot_dataframes(dfs,['X','y_fit'],filenames,"Fit Log", plot_type='log')
    
    # Table with results
    create_summary_table(plsqs, covs, filenames)
    
    print "****", args['no_save']
    if not args['no_save']: save_as_csv(dfs)
        
    plt.show()
    

if __name__ == "__main__":
    main(sys.argv)
    logger.info("Done!")
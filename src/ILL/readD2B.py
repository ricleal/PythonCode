#!/usr/bin/python

'''
Created on Oct 31, 2013

@author: leal

http://www.ill.eu/instruments-support/computing-for-science/data-analysis/raw-data/


'''
import re
import ast
import operator
import pprint
from collections import Counter
from string import ascii_uppercase as letters
import numpy as np

class ILLAsciiLoader(object):
    
    detectorShape=(128,128) # rows, collumns
    headerDic = {}
    spectraList = []
    
    
    def __init__(self,filepath = '/net/serdon/illdata/data/d2b/exp_5-21-1076/rawdata/123944'):
        self.fp = open(filepath,'r')
        
    def __del__(self):
        self.fp.close()
    
    
    def parseFile(self):
        line = self.fp.readline().strip()
        while (len(line) > 0):
            if line.startswith('RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'):
                self.parseR()
            elif line.startswith('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'):
                self.parseA()
            elif line.startswith('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII'):
                out = self.parseI()
                if out is not None:
                    self.headerDic.update(out)
            elif line.startswith('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'):
                out = self.parseF()
                if out is not None:
                    self.headerDic.update(out)
            elif line.startswith('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS'):
                self.startsParsingSpectra()
            
            # keeps going
            line = self.fp.readline().strip()
        
    def _slice(self,text,width):
        out = []
        position = 0
        while position < len(text):
            thisWord = text[position:position + width]
            thisWord = thisWord.strip()
            if len(thisWord) > 0:
                out.append(thisWord)
            position += width
        return out
    
    def _slipString(self,line,regexp ="\W+\s\W*"):
        regexp ="[^a-zA-Z0-9_\(\)]+\s[^a-zA-Z0-9_\(\)]*"
        '''
        Splits a string by regular expression
        Default : keeps one space as one word 
        '''
        return re.split(regexp,line.strip())
    
    def _renameExistingValues(self,arrayOfText):
        for idx,i in enumerate(arrayOfText) :
            found = 0;
            for j in arrayOfText :
                if i == j:
                    found+=1;
                    if found > 1:
                        arrayOfText[idx] = arrayOfText[idx]+"%d"%found
                        found+=1
        return arrayOfText
        

    def parseR(self):
        """
        RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
        122994       0       4          
        
        NRUN    is the run number (numor ) for the data following
        NTEXT    is the number of lines of descriptive text which follow
        NVERS    is the version of the data (modified as data structure changes)
        """
        
        line = self.fp.readline().strip().split()
        self.headerDic['NRUN'] = line[0]
        self.headerDic['NTEXT'] = line[1]
        self.headerDic['NVERS'] = line[2]
        
        
    def parseA(self):
        """
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
              80       1                                                                
        Inst User L.C.   Date     Time                                                  
        D2B Koza  ritt08-Jul-13 14:42:19                                                
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
              80       1                                                                
        Title                                                                   Scantype
        Zn4Sb3 08.07.2013 10' Coll slits=200 1.59 A                             2theta  
        
        NCHARS     is the number of characters to be read from the next data field using the format (80A1)
        NTEXT    is the number of lines of descriptive text before this data
        """
        
        line = self.fp.readline().strip().split()
        nchars = int(line[0])
        ntext =  int(line[1])
        key = self.fp.readline().strip()
        value=""
        for i in range(ntext):
            value += self.fp.readline().strip()
        self.headerDic[key] = value
    
    def parseI(self):
        """
        IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
              31       4                                                                
           nvers   ntype   kctrl   manip   nbang   nkmes  npdone   jcode   ipara   ianal
           imode    itgv  iregul   ivolt    naxe npstart  ilast1     isa  flgkif      ih
              ik   nbsqs  nb_det  nbdata icdesc1 icdesc2 icdesc3 icdesc4 icdesc5 icdesc6
         icdesc7                                                                        
               4       2       4       1       3      25      25       0       1       0
               0       0       1       0       2       0       0       0       0       0
               0       0       1   16384       1       2       3       0       0       0
               0       
        NINTGR    NTEXT                (10I8)
        
        NINTGR     is the number of integer numbers to be read from the next data 
            field using the format (10I8)
        NTEXT    is the number of line of descriptive text before the data
        """
        return self.parseIorR(length=8)
        
    def parseF(self):
        """
        FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
              50      10                                                                
                H (Hmin)        K (Kmin)        L (Lmin)             phi             chi
                   omega  2theta (gamma)             psi         ub(1,1)         ub(1,2)
                 ub(1,3)         ub(2,1)         ub(2,2)         ub(2,3)         ub(3,1)
                 ub(3,2)         ub(3,3)      wavelength  dmonochromator       danalyser
                  energy            Hmax            Kmax            Lmax          DeltaH
                  DeltaK          DeltaL     Deltaenergy         Ki (Kf)       Ddetector
                    xoff            zoff          radius            yoff        attenuat
              scan start       scan step      scan width          preset    add.bkg.step
           add.bkg.width  add.bkg.preset  couplingfactor         (spare)         (spare)
               Temp-s.pt      Temp-Regul     Temp-sample       Voltmeter       Mag.field
          0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00  0.49975000E+02
          0.59500002E+00  0.15185000E+03  0.00000000E+00  0.10000000E+01  0.00000000E+00
          0.00000000E+00  0.00000000E+00  0.10000000E+01  0.00000000E+00  0.00000000E+00
          0.00000000E+00  0.10000000E+01  0.15900000E+01  0.00000000E+00  0.00000000E+00
          0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00
          0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00
          0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00
          0.15125000E+03  0.50000000E-01  0.11999970E+01  0.10000000E+06  0.00000000E+00
          0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00  0.00000000E+00
          0.30589900E+03  0.30589500E+03  0.30500900E+03  0.21000000E+01  0.00000000E+00
        """
        
        return self.parseIorR(length=16)
        
    
    def parseIorR(self,length):
        """
        
        """
        line = self.fp.readline().strip().split()
        if len(line) >= 2: # text + values
            nvalues = int(line[0]) # number of float / integer fields
            ntext =  int(line[1]) # number of text lines
            
            keys = []
            for i in range(ntext):
                line = self.fp.readline()[:-1]#remove CR
                keys.extend(self._slice(line, length))
            keys = self._renameExistingValues(keys)
            
            values = []
            while len(values) < nvalues:
                line = self.fp.readline()[:-1]
                valuesStr = self._slice(line, length)
                values.extend([ast.literal_eval(i) for i in valuesStr])
            
            # If more values than keys. Group values for last key
            diff =  len(values) - len(keys)
            if diff > 0:
                diff += 1
                valuesToCompress = values[-diff:]
                values = values[:-diff]
                values.append(valuesToCompress)

            return dict(zip(keys, values))
        else:
            # spectra!
            nvalues = int(line[0]) # number of float / integer fields
#             values = []
#             while len(values) < nvalues:
#                 line = self.fp.readline()[:-1]
#                 valuesStr = self._slice(line, length)
#                 values.extend([ast.literal_eval(i) for i in valuesStr])
            values = self.parseIFromSpectrum(nvalues, length)
            return values
    
    def parseIFromSpectrum(self,nvalues,length):
        values = np.zeros(nvalues,int)
        pos = 0;
        while pos < len(values):
            line = self.fp.readline()[:-1]
            valuesStr = self._slice(line, length)
            for i in valuesStr:
                i = ast.literal_eval(i);
                values[pos]=i
                pos+=1
        return values

    def parseS(self):
        """
        SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
           1      24      25  125760       0       1                                
    
        SSSSSSSSSS..    ...        ..SSS    (80A1)
        ISPEC    NREST    NTOT    NRUN    NTEXT    NPARS    (10I8)
        
        ISPEC    is the following sub-spectrum number
        NREST    is the number of subspectra remaining after ISPEC 
        NTOT    is the total number of subspectra in the run 
        NRUN    is the current run number
        NTEXT    is the number of lines of descriptive text
        NPARS    is the number of parameter sections (F, I etc, preceding the
                counts data), typically for step-scanning multi-detector
                instruments where additional information is stored at each step
        
        """
        line = self.fp.readline().strip().split()
        out = {}
        out["ISPEC"] = ast.literal_eval(line[0])
        out["NREST"] = ast.literal_eval(line[1])
        out["NTOT"]  = ast.literal_eval(line[2])
        out["NRUN"]  = ast.literal_eval(line[3])
        out["NTEXT"] = ast.literal_eval(line[4])
        out["NPARS"] = ast.literal_eval(line[5])
        return out
        
    def startsParsingSpectra(self):
        '''
        SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
       1      24      25  125760       0       1                                

        SSSSSSSSSS..    ...        ..SSS    (80A1)
        ISPEC    NREST    NTOT    NRUN    NTEXT    NPARS    (10I8)
        
        ISPEC    is the following sub-spectrum number
        NREST    is the number of subspectra remaining after ISPEC 
        NTOT    is the total number of subspectra in the run 
        NRUN    is the current run number
        NTEXT    is the number of lines of descriptive text
        NPARS    is the number of parameter sections (F, I etc, preceding the
                counts data), typically for step-scanning multi-detector
                instruments where additional information is stored at each step
        '''
         
        thisSpectrumParams = self.parseS()
        
        line = self.fp.readline().strip()
        while (len(line) > 0):
            if line.startswith('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII'):
                ## Parse spectra I
                outArr = self.parseI()
#                 outArr = np.array(out)
                outArr = np.reshape(outArr,self.detectorShape)
                outArr = outArr.T
                thisSpectrumParams["values"] = outArr
                self.spectraList.append(thisSpectrumParams)
            elif line.startswith('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'):
                out = self.parseF()
                if out is not None:
                    thisSpectrumParams.update(out)
            elif line.startswith('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS'):
                thisSpectrumParams = self.parseS()
                
            line = self.fp.readline().strip()
    
    def interleave(self):
        """
        Transform all spectra in an interleaved detector
        """
        nSpectra = len(self.spectraList)
        nRows,ncols = self.detectorShape
        ncolsTotal =  nSpectra*ncols
        fullDetector = np.zeros((nRows,ncolsTotal))
        
        for idx,i in enumerate(self.spectraList):
            for col in range(ncols): # 0 to 128
                thisCollumn = i["values"][:,col]
                fullDetector[:,nSpectra*col+idx] = thisCollumn
        
        return fullDetector
    
def main():
    l = ILLAsciiLoader('123976')
    l.parseFile()
    pprint.pprint(l.headerDic)
    #print len(l.spectraDic)
    #print l.spectraDic[len(l.spectraDic)-1]
    from matplotlib import pyplot as plt
#     for i in range(10,11):
#         print l.spectraList[i]
#         img = l.spectraList[i]["values"]
#         plt.imshow(img)
#         plt.show()
#     
    fullDet = l.interleave()
    plt.imshow(fullDet)
    plt.savefig('/tmp/test.png', dpi = 400)
    plt.show()
    
    
if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 17:21:05 2012

@author: leal

This will be used has script to generate XML for IN5

"""

# Angle list copied from LOAD HDF from LAMP
x = [ -11.9175,     -11.5451,     -11.1727,     -10.8003,     -10.4279,     -10.0554,     -9.68300,     -9.31058,     -8.93816,     -8.56573,     -8.19331,     -7.82089,     -7.44846,     -7.07604,     -6.70362,     -6.33119,     -5.95877,     -5.58635,     -5.21393,     -4.84150,     -4.46908,     -4.09666,     -3.72423,     -3.35181,     -2.97939,     -2.60696,     -2.23454,     -1.86212,     -1.48969,     -1.11727,    -0.744846,    -0.372423,    0.372423,     0.744847,      1.11727,      1.48969,      1.86212,      2.23454,      2.60696,      2.97939,      3.35181,      3.72423,      4.09666,      4.46908,      4.84150,      5.21393,      5.58635,      5.95877,     6.33119,      6.70362,      7.07604,      7.44846,      7.82089,      8.19331,      8.56573,      8.93816,      9.31058,      9.68300,      10.0554,      10.4279,      10.8003,      11.1727,      11.5451,      11.9175,     12.6624,      13.0348,      13.4072,      13.7797,      14.1521,      14.5245,      14.8969,      15.2694,      15.6418,      16.0142,      16.3866,      16.7590,      17.1315,      17.5039,      17.8763,      18.2487,     18.6212,      18.9936,      19.3660,      19.7384,      20.1109,      20.4833,      20.8557,      21.2281,      21.6005,      21.9730,      22.3454,      22.7178,      23.0902,      23.4627,      23.8351,      24.2075,     24.9524,      25.3248,      25.6972,      26.0696,      26.4420,      26.8145,      27.1869,      27.5593,      27.9317,      28.3042,      28.6766,      29.0490,      29.4214,      29.7939,      30.1663,      30.5387,     30.9111,      31.2836,      31.6560,      32.0284,      32.4008,      32.7732,      33.1457,      33.5181,      33.8905,      34.2629,      34.6354,      35.0078,      35.3802,      35.7526,      36.1251,      36.4975,     37.2423,      37.6147,      37.9872,      38.3596,      38.7320,      39.1044,      39.4769,      39.8493,      40.2217,      40.5941,      40.9666,      41.3390,      41.7114,      42.0838,      42.4562,      42.8287,     43.2011,      43.5735,      43.9459,      44.3184,      44.6908,      45.0632,      45.4356,      45.8081,      46.1805,      46.5529,      46.9253,      47.2978,      47.6702,      48.0426,      48.4150,      48.7874,     49.5323,      49.9047,      50.2771,      50.6496,      51.0220,      51.3944,      51.7668,      52.1393,      52.5117,      52.8841,      53.2565,      53.6289,      54.0014,      54.3738,      54.7462,      55.1186,     55.4911,      55.8635,      56.2359,      56.6083,      56.9808,      57.3532,      57.7256,      58.0980,      58.4704,      58.8429,      59.2153,      59.5877,      59.9601,      60.3326,      60.7050,      61.0774,     61.8223,      62.1947,      62.5671,      62.9395,      63.3120,      63.6844,      64.0568,      64.4292,      64.8017,      65.1741,      65.5465,      65.9189,      66.2913,      66.6638,      67.0362,      67.4086,     67.7810,      68.1535,      68.5259,      68.8983,      69.2707,      69.6432,      70.0156,      70.3880,      70.7604,      71.1328,      71.5053,      71.8777,      72.2501,      72.6225,      72.9950,      73.3674,     74.1122,      74.4846,      74.8571,      75.2295,      75.6019,      75.9743,      76.3468,      76.7192,      77.0916,      77.4640,      77.8365,      78.2089,      78.5813,      78.9537,      79.3262,      79.6986,     80.0710,      80.4434,      80.8158,      81.1883,      81.5607,      81.9331,      82.3055,      82.6780,      83.0504,      83.4228,      83.7952,      84.1677,      84.5401,      84.9125,      85.2849,      85.6573,     86.4022,      86.7746,      87.1470,      87.5195,      87.8919,      88.2643,      88.6367,      89.0092,      89.3816,      89.7540,      90.1264,      90.4989,      90.8713,      91.2437,      91.6161,      91.9885,     92.3610,      92.7334,      93.1058,      93.4782,      93.8507,      94.2231,      94.5955,      94.9679,      95.3404,      95.7128,      96.0852,      96.4576,      96.8300,      97.2025,      97.5749,      97.9473,     98.6922,      99.0646,      99.4370,      99.8094,      100.182,      100.554,      100.927,      101.299,      101.672,      102.044,      102.416,      102.789,      103.161,      103.534,      103.906,      104.279,     104.651,      105.023,      105.396,      105.768,      106.141,      106.513,      106.885,      107.258,      107.630,      108.003,      108.375,      108.748,      109.120,      109.492,      109.865,      110.237,     110.982,      111.355,      111.727,      112.099,      112.472,      112.844,      113.217,      113.589,      113.962,      114.334,      114.706,      115.079,      115.451,      115.824,      116.196,      116.568,     116.941,      117.313,      117.686,      118.058,      118.431,      118.803,      119.175,      119.548,      119.920,      120.293,      120.665,      121.038,      121.410,      121.782,      122.155,      122.527,     123.272,      123.645,      124.017,      124.389,      124.762,      125.134,      125.507,      125.879,      126.251,      126.624,      126.996,      127.369,      127.741,      128.114,      128.486,      128.858,     129.231,      129.603,      129.976,      130.348,      130.721,      131.093,      131.465,      131.838,      132.210,      132.583,      132.955,      133.328,      133.700,      134.072,      134.445,      134.817]

# Just to test the gaps between panels
for idx,i in enumerate(x):
    
    if idx > 0:
        dif= i - x[idx-1]
        if dif > 0.4:
            print idx, dif, ' -> ', idx-1 ,' and ', idx
    else:
        print idx
print idx

'''
Write the door types and psotion of the tubes
'''

# Reverse the list like LAMP does
x.reverse()
writeHeader=True
door=0
for idx,(i,j) in enumerate(zip(x,range(1,32*12+1))):
    if writeHeader==True:
        print '''<type name="door%d">
    <component type="standard-tube">'''%door
        door+=1
        writeHeader = False
    print '<location r="4.0" t="%f" name="tube_%d" > <facing x="0" y="0" z="0"/> </location>'%(i,idx)
    if idx > 0 and j%32 == 0:
        print '</component>\n</type>'
        writeHeader=True


'''
Write detector IDs.
I'm assuming 1024 between each detector ID
'''

writeHeader=True
door=0
for idx,i in enumerate(range(1,32*12+1)):
    if writeHeader==True:
        print '<idlist idname="door%d">'%door
        door+=1
        writeHeader = False
    print '<id start="%d" end="%d" />'%(idx*256,idx*256+256-1)    
    if i%32 == 0:
        print '</idlist>'
        writeHeader=True

''' 
Standard tube: 256

<type name="standard-tube" outline="yes">
    <component type="standard-pixel">
     <location y="-1.4635693359375"/>
     ...
     <location y="1.46356933593751"/>
    </component>
  </type>
'''
import numpy as np
yPixels = np.linspace(-1.4635693359375,1.46356933593751,256)
print '<type name="standard-tube" outline="yes">\
<component type="standard-pixel">'
for i in yPixels:
    print '<location y="%f"/>'%i
print '</component></type>'


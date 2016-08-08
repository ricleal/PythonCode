## Mandi tests

2 621 440 detectors

###`mandi_dump.py`:

Dump `(x,y,z)` of every detector into a pandas dataframe.

###`mandi_read.py`:

Read it back, append spherical coordinates `(r,t,p)` and save it as other dataframe.

Results:

```
$ python2 mandi_read.py
Data frame headers:['name' 'bank_name' 'i' 'j' 'x' 'y' 'z']
Cartesian to Sperical took 0.819 seconds
NEW Data frame headers:['name' 'bank_name' 'i' 'j' 'x' 'y' 'z' 'r' 't' 'p']
XYZ for Pixel: xyz_2d[128,128] = [-0.00747811 -0.37506834  0.16469329]
Reshape and Indexing took 0.103 seconds
```

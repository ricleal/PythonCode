## Mandi tests

2 621 440 detectors

Dump x,y,z of every detector into a pandas dataframe.

Read id back, append spherical coordinates (r,t,p) and save it as other dataframe.

Results:

```
$ python mandi_read.py 
'spherical' ((array([[ 0.07128832, -0.40785943,  0.09191706],
       [ 0.07129393, -0.40760608,  0.09248071],
       [ 0.07129954, -0.40735272,  0.09304436],
       ..., 
       [-0.1877869 ,  0.33930886,  0.26351482],
       [-0.18729538,  0.33966949,  0.26358796],
       [-0.18680386,  0.34003012,  0.26366111]]),), {}) 0.30 sec
New data frame headers: ['name' 'x' 'y' 'z' 'r' 't' 'p']
DF Saved!
```

0.3 seconds :)

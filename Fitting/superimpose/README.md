# SuperImpose

Finds K (scale factor) + b to superimpose all the curves given as parameters

```
I(scaled) = f * I(original) – b
```

Needs packages:
- pandas
- scipy
- matplotlib
- numpy
- tabulate


If needed change defaults in ```config.cfg```:
```
[General]
qmin = 0.0001
qmax = 1.0
```

Help:

```
$ ./superimpose.py -h
usage: superimpose.py [-h] -r REFERENCE -i INPUT [-q QMIN] [-m QMAX]

Calculates: I_{scaled}(Q) = K*I(Q)+b

optional arguments:
  -h, --help            show this help message and exit
  -r REFERENCE, --reference REFERENCE
                        File to use as reference to scale all curves
  -i INPUT, --input INPUT
                        Input files (if reference is included it will ignored)
  -q QMIN, --qmin QMIN  Q min. If not given, gets it from the config file.
  -m QMAX, --qmax QMAX  Q max. If not given, gets it from the config file.

```
Run as:
```
python superimpose.py -r data_2/Si_4m6A_abs_1.txt -i 'data_2/Si_4m6A_abs_*' --qmin 0.01 --qmax 0.019
```

If needed, install missing packages with ```pip```:

```
pip install <package name> --user
```

Errors in analysis.ornl.gov:
```
$ ./superimpose.py -r data_2/Si_4m6A_abs_1.txt -i 'data_2/Si_4m6A_abs_*' --qmin 0.009 --qmax 0.019
Traceback (most recent call last):
  File "./superimpose.py", line 22, in <module>
      import pandas as pd
      ImportError: No module named pandas
```

```
$ ./superimpose.py -r data_2/Si_4m6A_abs_1.txt -i 'data_2/Si_4m6A_abs_*' --qmin 0.009 --qmax 0.019
Traceback (most recent call last):
  File "./superimpose.py", line 28, in <module>
      from tabulate import tabulate
      ImportError: No module named tabulate
```

The missing packages should be only these two:
```
pip install pandas tabulate --user
```

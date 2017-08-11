import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['image.cmap'] = 'viridis'
plt.rcParams['figure.figsize'] = 10,10

# genererate some 2D data:
# Axis
x = np.linspace(-1,1,100)
y = np.linspace(-1,1,100)
# Z
xx,yy = np.meshgrid(x, x)
r = np.hypot(xx, yy)

# Pic 1
plt.figure()
plt.title("imshow")
extent=(x[0], x[-1], y[0], y[-1])
plt.imshow(r, extent=extent, origin='upper', aspect='auto')

# Note: I can not get Z value! It appears on the bottom bar though....
# Check example below with pcolormesh
def format_coord_imshow(x, y):
    print("{} {}".format(x,y))
    return "(%.2f,%.2f)"%(x,y)

# Get the axis!
ax = plt.gca()
ax.format_coord = format_coord_imshow

#
#
# Pic 2
#
#
plt.figure()
plt.title("pcolormesh")
plt.pcolormesh(xx, yy, r)

def find_nearest_index(array,value):
    '''
    Given an array finds the nearest index of the value
    '''
    idx = (np.abs(array-value)).argmin()
    return idx

numrows, numcols = r.shape
def format_coord_pcolormesh(x_coord, y_coord):
    col = find_nearest_index(x,x_coord)
    row = find_nearest_index(y,y_coord)
    if col>=0 and col<numcols and row>=0 and row<numrows:
        z_coord = r[row,col]
        print("{:,.2f} {:,.2f} {:,.2f}".format(x_coord, y_coord, z_coord))
        return '(%.2f,%.2f) = %.2f'%(x_coord, y_coord, z_coord)
    else:
        return 'x=%1.4f, y=%1.4f'%(x_coord, y_coord)


# Get the axis!
ax = plt.gca()
ax.format_coord = format_coord_pcolormesh

plt.show()

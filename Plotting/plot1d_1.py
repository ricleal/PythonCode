import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['image.cmap'] = 'viridis'
plt.rcParams['figure.figsize'] = 10,10

# genererate some 1D data:
# Axis
x = np.linspace(-np.pi,np.pi,100)
y = np.sin(x)

# Pic 1
plt.figure()
plt.plot(x,y,'o')

# Note: I can not get Z value! It appears on the bottom bar though....
# Check example below with pcolormesh
def format_coord_imshow(x, y):
    print(":: {:,.2f} {:,.2f}".format(x,y))
    return "(%.2f,%.2f)"%(x,y)

# Get the axis!
ax = plt.gca()
ax.format_coord = format_coord_imshow

def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y
    if event.xdata and event.ydata:
        ax = event.inaxes  # the axes instance
        print('Over: %f %f' % (event.xdata, event.ydata))

plt.connect('motion_notify_event', on_move)

plt.show()

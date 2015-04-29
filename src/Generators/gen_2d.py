import numpy as np
import matplotlib.pyplot as plt

def make_it_nan (array, distance):
    for i, row in enumerate(array):
        for j, value in enumerate(row):
            if dist[i,j] > distance:
                z[i,j] = np.NaN
    return z
            

def dump_as_csv(x,y,z):
    # Make sparse false!
    
    xx, yy = np.meshgrid(x, y, sparse=False)
    a = zip(xx.flatten(),yy.flatten(),z.flatten())
    ar = np.array(a)
    np.savetxt("/tmp/array.csv", ar, fmt='%.2e', delimiter=',', newline='\n', header='x,y,z')
    with open("/tmp/array.txt","w") as f:
        for row in ar:
            f.write("[%s]\n" % ', '.join(str(x) for x in row) )
    
    a = zip(xx.flatten(),yy.flatten(),z.flatten(), np.sqrt(z.flatten()) )
    ar = np.array(a)
    np.savetxt("/tmp/array_err.csv", ar, fmt='%.2e', delimiter=',', newline='\n', header='x,y,z,err')
    with open("/tmp/array_err.txt","w") as f:
        for row in ar:
            f.write("[%s]\n" % ', '.join(str(x) for x in row) )
    

x = np.arange(-5, 5, 0.1)
y = np.arange(-5, 5, 0.1)
xx, yy = np.meshgrid(x, y, sparse=True)
dist = np.hypot(xx, yy) # Linear distance from point 0, 0
z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)

z = make_it_nan (array=z, distance=5)

dump_as_csv(x,y,z)

# plot
h = plt.contourf(x,y,z,100)
plt.show()


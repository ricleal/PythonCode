import mpld3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

# read CSV as a numpy array
filePath = 'data.csv'
data = mlab.csv2rec(filePath)

# load collumns as vectors
data_x = data['position']
data_y = data['value']

# figure
fig = plt.figure('.: MatPlotLib Example :.')
fig.suptitle('Plot for file '+filePath, fontsize=12, fontweight='bold')

# Add my axis (I only have one, but I could have two, e.g., mirrored Y)
ax = fig.add_subplot(111)

# plot raw data
# I'm going to add some labels to add a legend after
ax.plot(data_x,data_y,'o', label='Raw data')
ax.set_xlabel(data.dtype.names[0])

# Now I want to have X axis with some Latex:
from matplotlib import rc
rc('text', usetex=True)
ax.set_ylabel(data.dtype.names[1]+' ($\\AA^{-1}$)')
rc('text', usetex=False)

# fit data with a polynomial of degree 1: ax+b=0
a,b = np.polyfit(data_x, data_y, 1)
data_y_fitted = np.polyval([a, b], data_x)

#plot fitted data
ax.plot(data_x,data_y_fitted,'-', label='Fitted data')

# Let's add the legend to the lower right corner
ax.legend(loc= 'lower right')


html_plot = mpld3.fig_to_html(fig)

html_str = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>The HTML5 Herald</title>
</head>
<body>
<h1>Here we have a simple plot in mpld3</h1>
<div>
  %s
</div>
<p>Latex rendering is not working :(</p>
</div>
</body>
</html>
"""%html_plot

html_file= open("index.html","w")
html_file.write(html_str)
html_file.close()

import SimpleHTTPServer
import SocketServer
PORT = 8080
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
print "serving at port", PORT, "Open in your browser: http://localhost:%s/"%PORT
httpd.serve_forever()

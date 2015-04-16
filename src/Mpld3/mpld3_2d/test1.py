import mpld3
import numpy as np
import matplotlib.pyplot as plt

# figure
fig = plt.figure('.: MatPlotLib Example :.')

# Add my axis (I only have one, but I could have two, e.g., mirrored Y)
ax = fig.add_subplot(111)

x, y = np.mgrid[-10:10, -10:10]
dist = np.hypot(x, y) # Linear distance from point 0, 0
z = np.cos(2 * dist / np.pi)

# Now I want to have X axis with some Latex:
from matplotlib import rc
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
ax.set_title(r'$\cos(\frac{2*\sqrt{x^2 + y^2}}{\pi})$', size=16)


im = ax.imshow(z, origin='lower', interpolation='bicubic',
          extent=(x.min(), x.max(), y.min(), y.max()))

plt.colorbar(im)

#plt.show()


html_plot = mpld3.fig_to_html(fig)

html_str = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>mpld3 plot</title>
</head>
<body>
<h1>Here we have a simple 2D plot in mpld3</h1>
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


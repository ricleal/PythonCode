import numpy as np
import bokeh
from bokeh.models.widgets import Dropdown
from bokeh.io import output_file, show, vform
#from bokeh.models import Callback
from bokeh.models import CustomJS
from bokeh.plotting import figure
'''
Possible bug submitted to bokeh!
Dropdown always returning the last menu item... #2631
https://github.com/bokeh/bokeh/issues/2631
'''
output_file("dropdown.html")

# Dummy plot, otherwise the Dropdown button is partially hidden...
x = np.linspace(-2*np.pi,2*np.pi,100)
y = np.sin(x)
p = figure(title="Sin(x)", x_axis_label='x', y_axis_label='sin(x)')
p.line(x, y)


callback = CustomJS(args=None, code="""
        console.log(cb_obj)
        console.log(cb_obj.get('value'))
        console.log(cb_obj.get('action'))
        var cm_chosen = cb_obj.get('action');
        alert(cm_chosen);
    """)

menu = [("Item %s"%i, "item_%s"%i) for i in range(10) ]
dropdown = Dropdown(label="Dropdown button %s"%bokeh.__version__, type="success",
                    menu=menu, callback=callback)

show(vform(dropdown,p))

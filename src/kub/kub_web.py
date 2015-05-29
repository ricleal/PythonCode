from bottle import request, route
import bottle
import tempfile
import os

def plot(filename='CSVReport.csv'):

    import csv
    import tabular as tb
    import matplotlib.pyplot as plt
    import numpy as np
    import datetime
    import mpld3

    ELECT_PRICE_KW = 0.085
    ELECT_SERVICE_FEE = 14
    GAS_PRICE_THERM = 1.247
    GAS_SERVICE_FEE = 6.65

    data = tb.tabarray(SVfile=filename,
        delimiter=',', doublequote=True,)

    data_elect = data[ data["Service Agreement Type"] == "E-RES" ]
    data_gas = data[ data["Service Agreement Type"] == "G-RES" ]

    fig = plt.figure(1)

    dates = np.array(data_elect["Billing Period End"])
    x = [datetime.datetime.strptime(i, "%m/%d/%Y" ) for i in dates]
    y = data_elect["Consumption"]
    ax1 = plt.subplot(211)
    plt.plot(x, y, 'o')
    for i,j in zip(x,y):
        ax1.annotate('$%.f'%(j*ELECT_PRICE_KW+ELECT_SERVICE_FEE), xy=(i,j))#,xytext=(5,0), textcoords='offset points')
    plt.title("E-RES")
    ax1.grid()
    ax1.set_xlim([min(x) - datetime.timedelta(10,0),max(x) + datetime.timedelta(30,0)])
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()


    dates = np.array(data_gas["Billing Period End"])
    x = [datetime.datetime.strptime(i, "%m/%d/%Y" ) for i in dates]
    y = data_gas["Consumption"]
    ax2 = plt.subplot(212)
    plt.plot(x, y, 'ro')
    for i,j in zip(x,y):
        ax2.annotate('$%.f'%(j*GAS_PRICE_THERM+GAS_SERVICE_FEE), xy=(i,j))#,xytext=(5,0), textcoords='offset points')
    plt.title("G-RES")
    ax2.grid()
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    ax2.set_xlim([min(x) - datetime.timedelta(10,0),max(x) + datetime.timedelta(30,0)])

    #plt.show()

    html_plot = mpld3.fig_to_html(fig)

    html_str = """<!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>KUB plot</title>
    </head>
    <body>
    <h1>KUB Plot</h1>
    <div>
      %s
    </div>
    </div>
    </body>
    </html>
    """%html_plot

    return html_str


@route('/', method='GET') # or @route('/login')
def render_form():
    return '''<!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>KUB plot</title>
    </head>
    <body>
        <h1>Upload your CSV file.</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
          <p>Select a file: <input type="file" name="upload" accept="csv" /></p>
          <p><input value="Start upload" type="submit" /></p>
        </form>
    </body>
    </html>
    '''

@route('/upload', method='POST')
def do_upload():

    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.csv'):
        return '<p>File extension not allowed.</p>'

    local_file = tempfile.NamedTemporaryFile(delete=False)
    upload.save(local_file.name, overwrite=True)
    html = plot(local_file.name)
    return html



bottle.run(host='localhost', port=8080)

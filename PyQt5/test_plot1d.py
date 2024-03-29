#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Plot 1D
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
#from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtCore import QUrl
import plots

html = '''<html>
<head>
    <title>Plotly Example</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
    <body>
    %(plot_content)s
    </body>
</html>'''

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = QWebView()
    w.resize(800, 600)
    w.move(300, 300)
    w.setWindowTitle('Simple 1D Plot')

    plot_content = plots.plot1d()

    w.setHtml(html%{'plot_content':plot_content})
    w.show()

    sys.exit(app.exec_())

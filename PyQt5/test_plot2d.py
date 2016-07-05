#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we create a simple
window in PyQt5.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
#from PyQt5.QtWebEngineWi  import QWebView
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
    w.resize(900, 700)
    w.move(300, 300)
    w.setWindowTitle('Simple 2D Plot')

    plot_content = plots.plot2d()

    w.setHtml(html%{'plot_content':plot_content})
    w.show()

    sys.exit(app.exec_())

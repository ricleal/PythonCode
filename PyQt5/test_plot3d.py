#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Plotly 3D not working
Besause WebGL not available
https://trac.webkit.org/wiki/QtWebKitWebGL
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsScene
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QGraphicsWebView
from PyQt5 import QtWebKitWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtOpenGL import QGLWidget
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
    w.setWindowTitle('Simple Plot')

    QWebSettings.globalSettings().setAttribute(QWebSettings.AcceleratedCompositingEnabled, True)
    QWebSettings.globalSettings().setAttribute(QWebSettings.WebGLEnabled, True)

    plot_content = plots.plot3d()
    w.setHtml(html%{'plot_content':plot_content})
    w.show()

    sys.exit(app.exec_())

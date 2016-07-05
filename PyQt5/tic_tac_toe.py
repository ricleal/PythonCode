#!/usr/bin/env python

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtWebKitWidgets import QGraphicsWebView
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
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

class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers | QGL.DirectRendering)))
        QWebSettings.globalSettings().setAttribute(QWebSettings.AcceleratedCompositingEnabled, True)

        scene = QGraphicsScene(self)


        w = QGraphicsWebView()
        w.resize(900, 700)
        plot_content = plots.plot3d()
        w.setHtml(html%{'plot_content':plot_content})
        scene.addItem(w)

        scene.setSceneRect(0, 0, 900, 700)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("Plot 3D")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())

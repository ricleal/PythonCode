#!/usr/bin/env python3

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QFrame)
from PyQt5.QtWebKitWidgets import QGraphicsWebView, QWebPage
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtCore import QUrl
import plots


"""

Trying to get webgl to work!

This explodes in Ubuntu 16.04 with NVidia Version: 361.42
"""

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
    import sys

    app = QApplication(sys.argv)

    page = QWebPage()
    pScene = QGraphicsScene();
    pView = QGraphicsView(pScene)
    pView.setFrameShape(QFrame.NoFrame)
    pView.setViewport(QGLWidget())


    pWebview = QGraphicsWebView()
    pWebview.setPage(page);

    pWebview.setResizesToContents(True);

    plot_content = plots.plot3d()
    pWebview.setHtml(html%{'plot_content':plot_content})

    pScene.addItem(pWebview)
    pScene.setSceneRect(0, 0, 900, 700)

    pView.show()

    sys.exit(app.exec_())

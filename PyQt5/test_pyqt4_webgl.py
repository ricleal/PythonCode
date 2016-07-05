#!/usr/bin/env python3

"""
This explodes in Ubuntu 16.04 with NVidia Version: 361.42  
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
app = QApplication([])
v = QGraphicsView()
s = QGraphicsScene()
v.setScene(s)
v.show()
v.resize(600,600)
v.setViewport(QGLWidget())
r = QGraphicsRectItem(0, 0, 10, 10)
s.addItem(r)

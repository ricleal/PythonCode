#!/usr/bin/env python

import sys
from canvas import MatplotlibCanvas
from plotui import Ui_plot_window
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import numpy as np


class plotview(QtGui.QMainWindow):
    def __init__(self, parent=None,cmdpipes = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_plot_window()
        self.ui.setupUi(self)

        self.layout = QtGui.QVBoxLayout(self.ui.plot_group_box)
        self.figure = MatplotlibCanvas(self.ui.plot_widget)
        self.layout.addWidget(self.figure.toolbar)
        self.layout.addWidget(self.figure.canvas)

    def plot_2d_sample(self):
        data = np.random.rand(10, 20)
        self.figure.axes.imshow(data, interpolation='bicubic')
        self.figure.axes.grid(True)
        self.figure.canvas.draw()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    plot = plotview()
    plot.plot_2d_sample()
    plot.show()
    if app.exec_():
        pass

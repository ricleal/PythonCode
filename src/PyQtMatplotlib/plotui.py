# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot.ui'
#
# Created: Mon Nov  2 11:34:06 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_plot_window(object):
    def setupUi(self, plot_window):
        plot_window.setObjectName(_fromUtf8("plot_window"))
        plot_window.resize(787, 628)
        self.plot_widget = QtGui.QWidget(plot_window)
        self.plot_widget.setObjectName(_fromUtf8("plot_widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.plot_widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plot_group_box = QtGui.QGroupBox(self.plot_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_group_box.sizePolicy().hasHeightForWidth())
        self.plot_group_box.setSizePolicy(sizePolicy)
        self.plot_group_box.setTitle(_fromUtf8(""))
        self.plot_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_group_box.setObjectName(_fromUtf8("plot_group_box"))
        self.verticalLayout.addWidget(self.plot_group_box)
        plot_window.setCentralWidget(self.plot_widget)

        self.retranslateUi(plot_window)
        QtCore.QMetaObject.connectSlotsByName(plot_window)

    def retranslateUi(self, plot_window):
        plot_window.setWindowTitle(_translate("plot_window", "MainWindow", None))

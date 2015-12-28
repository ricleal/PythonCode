from PyQt4.QtCore import *
from PyQt4.QtGui  import *
import sys

class MyMainWindow(QWidget):

    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.form_widget = FormWidget(self)
        self.resize(400, 400)
        self.restoreMainWindowState()

    def restoreMainWindowState(self):
        ####
        # Save state to: ~/.config/MyCompany/MyApp.con
        #self.settings = QSettings("MyCompany", "MyApp")
        self.settings = QSettings("/tmp/myapp.ini",QSettings.IniFormat)
        self.form_widget.textbox_restore_state(self.settings)

    def saveMainWindowState(self):
        self.form_widget.textbox_save_state(self.settings)

    def closeEvent(self, event):
        self.saveMainWindowState()
        QMainWindow.closeEvent(self, event)

class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.cb = QCheckBox('Show title', self)
        self.layout.addWidget(self.cb)

        self.table = QTableWidget(self)
        self.table.resize(400, 250)
        self.table.setColumnCount(2)
        self.table.resizeColumnsToContents()
        self.currentRowCount = self.table.rowCount()
        self.layout.addWidget(self.table)

        self.textbox = QLineEdit(self)
        self.layout.addWidget(self.textbox)

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)
        self.button1.clicked.connect(self.handleButton)

        self.setLayout(self.layout)

    def textbox_save_state(self,settings):
        name = 'textbox'
        value = self.textbox.text()
        settings.setValue(name, value)    # save ui values, so they can be restored next time

    def textbox_restore_state(self,settings):
        name = 'textbox'
        value = settings.value(name)
        self.textbox.setText(value.toString())


    def handleButton(self):
        print 'Current Row Count =',self.currentRowCount
        self.table.insertRow(self.currentRowCount)
        self.table.setItem(self.currentRowCount , 0, QTableWidgetItem("Cell (%d,0)"%self.currentRowCount))
        self.table.setItem(self.currentRowCount , 1, QTableWidgetItem("Cell (%d,1)"%self.currentRowCount))
        self.currentRowCount = self.table.rowCount()
        self.table.resizeColumnsToContents()

app = QApplication([])
foo = MyMainWindow()
foo.show()
sys.exit(app.exec_())

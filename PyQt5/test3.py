#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
QWebView with static html
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
#from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtCore import QUrl

html = '''<html>
<head>
    <title>A Sample Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <hr />
    <p>Simple Paragraph.</>
</body>
</html>'''

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = QWebView()
    w.resize(800, 600)
    w.move(300, 300)
    w.setWindowTitle('Simple Plot')
    w.setHtml(html)
    w.show()
    sys.exit(app.exec_())

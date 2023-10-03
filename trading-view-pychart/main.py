import os
import sys
import time
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

class myClass(QObject):
    def __init__(self, page:QWebEnginePage=None):
        QObject.__init__(self)
        self.page = page
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    myWeb=QWebEngineView()
    myChannel=QWebChannel()
    testWeb=myClass(page=myWeb.page())
    myWeb.page().setWebChannel(myChannel)
    myChannel.registerObject('testObject',testWeb) 
    url = QUrl.fromLocalFile(os.path.abspath(r'trading-view-pychart/template.html'))
    print(url)
    myWeb.load(url)
    win.setCentralWidget(myWeb)
    win.setWindowTitle('Trading View PyChart')
    win.statusBar().showMessage('Trading View')
    win.show()
    sys.exit(app.exec())
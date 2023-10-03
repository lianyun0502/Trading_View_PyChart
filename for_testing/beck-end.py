import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
import time

info="2"
class myClass(QObject):
    def __init__(self, page:QWebEnginePage=None):
        QObject.__init__(self)
        self.page = page
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.send_time)
        # self.timer.start()

    @QtCore.Slot(str, result=str)
    def hello(self, message):
        print('call received')
        # print(f'hello from python: {message}')
        if message == 'start' and not self.timer.isActive():
            self.timer.start()
        return f'hello from python: {message}'

    @Slot()
    def testPy2JS(self):
        self.page.runJavaScript('waitingMessage='+info+';')

    @Slot(str)
    def testJS2Py(self, msg):
        print(msg)

    @QtCore.Slot(result=None)
    def send_time(self):
        self.page.runJavaScript(f'sysTime("receive_time :{time.strftime("%H:%M:%S")}")')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    myWeb=QWebEngineView()
    myChannel=QWebChannel()
    testWeb=myClass(page=myWeb.page())
    myWeb.page().setWebChannel(myChannel)
    myChannel.registerObject('testObject',testWeb) 
    url = QUrl.fromLocalFile(os.path.abspath(r'for_testing/font-end.html'))
    print(url)
    myWeb.load(url)
    win.setCentralWidget(myWeb)
    win.setWindowTitle('JS_to_Python')
    win.statusBar().showMessage('JS_to_Python')
    win.show()
    sys.exit(app.exec())
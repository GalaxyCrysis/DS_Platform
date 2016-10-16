from PyQt4 import QtGui,QtCore,uic

class mainWindow(QtGui.QMainWindow):
    #init main window
    def __init__(self):
        super(mainWindow,self).__init__()
        uic.loadUi("main.ui",self)


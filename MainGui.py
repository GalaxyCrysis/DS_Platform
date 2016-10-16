from PyQt4 import QtGui,QtCore,uic
from dbImporter import dbImporter

class mainWindow(QtGui.QMainWindow):
    #init main window
    def __init__(self):
        super(mainWindow,self).__init__()
        uic.loadUi("main.ui",self)
        self.setWindowTitle("Data Science Platform")
        #init variables
        self.dataList = list()
        self.nameList = list()
        self.addMenu()

        self.show()

    #init the Menu bar for the Gui
    def addMenu(self):
        importMenu = self.menuBar().addMenu("Import Dataset")
        importMenu.addAction("Import from Database", self.importDB)
        importMenu.addAction("Import from local File",self.importFile)

    def importDB(self):
        print("")

    def importFile(self):
        print("")




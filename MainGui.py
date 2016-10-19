from PyQt4 import QtGui,QtCore,uic
from dbImporter import dbImporter
from fileImporter import fileImporter


class mainWindow(QtGui.QMainWindow):
    #init main window
    def __init__(self):
        super(mainWindow,self).__init__()
        uic.loadUi("ui/main.ui",self)
        self.setWindowTitle("Data Science Platform")
        #init variables
        self.dataList = list()
        self.nameList = list()
        self.typeList = list()
        self.addMenu()
        self.show()

    #init the Menu bar for the Gui
    def addMenu(self):
        importMenu = self.menuBar().addMenu("Import Dataset")
        importMenu.addAction("Import from Database", self.importDB)
        importMenu.addAction("Import from local File",self.importFile)


    #import data from a database
    def importDB(self):
        importer = dbImporter()
        importer.exec()
        #the importer dialog closes when importing data. Then we append the new data to the lists for later use
        if importer.close():
            name,dataframe,type = importer.importData()
            self.nameList.append(name)
            self.dataList.append(dataframe)
            self.typeList.append(type)


    #import data from a local file
    def importFile(self):
        importer = fileImporter()
        importer.exec()
        # the importer dialog closes when importing data. Then we append the new data to the lists for later use
        if importer.close():
            name,dataframe,type = importer.importData()
            self.nameList.append(name)
            self.dataList.append(dataframe)
            self.typeList.append(type)





from PyQt4 import QtGui,QtCore,uic
from src.dbImporter import dbImporter
from src.fileImporter import fileImporter


class mainWindow(QtGui.QMainWindow):
    #init main window
    def __init__(self):
        super(mainWindow,self).__init__()
        uic.loadUi("../ui/main.ui",self)
        self.setWindowTitle("Data Science Platform")
        #init variables
        self.dataList = list()
        self.nameList = list()
        self.typeList = list()
        self.addMenu()
        self.show()


    #init the Menu bar for the Gui
    def addMenu(self):
        #init main menu
        mainMenu = self.menuBar().addMenu("Session")

        #init the import dataset menu
        importMenu = self.menuBar().addMenu("Import Dataset")
        importMenu.addAction("Import from Database", self.importDB)
        importMenu.addAction("Import from local File",self.importFile)

        #init the data processing menu
        processMenu = self.menuBar().addMenu("Data processing")
        processMenu.addAction("Prepare Data",self.prepareData)
        processMenu.addAction("Visualization",self.visualize)


    def prepareData(self):
        print("")

    def visualize(self):
        print("")


    #function for updating the data table and data list
    def updateDataWidgets(self,name,info,type):
        rowCount = self.dataTable.rowCount()
        self.dataTable.insertRow(rowCount)
        self.dataTable.setItem(rowCount, 0, QtGui.QTableWidgetItem(name))
        self.dataTable.setItem(rowCount, 1, QtGui.QTableWidgetItem(info))
        self.dataTable.setItem(rowCount, 2, QtGui.QTableWidgetItem(type))
        self.dataBox.addItem(name)


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
            shape = dataframe.shape
            info = str(shape[0]) + " obj. of " + str(shape[1]) + " variables"
            self.updateDataWidgets(name,info,type)




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
            info = ""
            if type == "Dataset":
                shape = dataframe.shape
                info = str(shape[0]) + " obj. of " + str(shape[1]) + " variables"
            elif type == "Text":
                info = str(len(dataframe.split("\n"))) + " li. of " + str(len(dataframe.split(" "))) + " words"
            else:
                info = "no info"
            self.updateDataWidgets(name,info,type)








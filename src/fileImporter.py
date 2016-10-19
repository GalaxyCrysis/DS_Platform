from PyQt4 import QtGui,QtCore,uic
import pandas as pd


class fileImporter(QtGui.QDialog):
    def __init__(self):
        super(fileImporter,self).__init__()
        uic.loadUi("../ui/fileImporter.ui",self)

        #init variables
        self.dataframe = ""
        self.dfName = ""
        self.openButton.clicked.connect(self.openFile)
        self.importButton.clicked.connect(self.importData)
        self.type = ""
        self.show()


    #function for uploading a file via q file dialog
    def openFile(self):
        # get file name from f dialog
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open file", "/home")

        # open file
        file = open(file_name, "r")
        if self.textCheck.isChecked():
            self.dataframe = file.read()
            self.type = "Text"
        elif self.preprocessCheck.isChecked():
            self.dataframe = file.read()
            self.type = "to be preprocessed"
        else:
            split = str(self.splitBox.currentText())
            self.dataframe = pd.read_table(file,sep=split)
            self.type = "Dataset"
        self.dataBrowser.setText(str(self.dataframe))

    def importData(self):
        self.dfName = self.nameEdit.text()
        self.close()
        return (self.dfName,self.dataframe,self.type)






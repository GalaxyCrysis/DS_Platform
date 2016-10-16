from PyQt4 import QtGui,QtCore, uic
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from mysql.connector import Error
import mysql.connector
import pandas as pd
from pandas.io.sql import DatabaseError

class dbImporter(QtGui.QDialog):
    def __init__(self):
        # init dbImporter ui
        super(dbImporter, self).__init__()
        uic.loadUi("dbImporter.ui", self)
        #init variables
        self.dfName = ""
        self.dataframe =""
        #connect buttons
        self.getDataButton.clicked.connect(self.getData)


        self.show()

    #get data from database
    def getData(self):
        # get database information from line edits
        user = self.userEdit.text()
        password = self.passwordEdit.text()
        host = self.hostEdit.text()
        port = self.portEdit.text()
        database = self.databaseEdit.text()
        table = self.tableEdit.text()
        db = str(self.dbBox.currentText())
        statement = self.statementEdit.text()

        #get data from mysql database
        if db == "MySQL":
            try:
                conn = mysql.connector.connect(host=host,database=database,user = user,password=password)
                if conn.is_connected():
                    try:
                        if statement == "":
                            self.dataframe = pd.read_sql("SELECT * FROM " + table, con=conn)
                        else:
                            self.dataframe = pd.read_sql(statement, con=conn)
                    except DatabaseError as err:
                        self.dataframe = "Error: "+ str(err)



            except Error as err:
                self.dataframe = "Error: "+str(err)

        self.dataBrowser.setText(str(self.dataframe))
        self.dfName = table

    #import data by closing the window
    def importData(self):
        if "Error: " not in self.dataframe:
            self.close()
            return (self.dfName,self.dataframe)


















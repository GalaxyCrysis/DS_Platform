from PyQt4 import QtGui,QtCore, uic
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from mysql.connector import Error
import mysql.connector
import pandas as pd
from pandas.io.sql import DatabaseError
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import CursorNotFound

from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from cassandra import DriverException


class dbImporter(QtGui.QDialog):
    def __init__(self):
        # init dbImporter ui
        super(dbImporter, self).__init__()
        uic.loadUi("ui/dbImporter.ui", self)
        #init variables
        self.dfName = ""
        self.dataframe =""
        self.type = ""
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
                        conn.shutdown()
                    except DatabaseError as err:
                        self.dataframe = "Error: "+ str(err)



            except Error as err:
                self.dataframe = "Error: "+str(err)

        #get data from MongoDB database
        elif db == "MongoDB":
            try:
                # connect with database
                if user and password:
                    mongo_uri = "mongodb://%s:%s@%s:%s/%s" % (user, password, host, port, database)
                    client = MongoClient(mongo_uri)
                else:
                    client = MongoClient(host, port)

                # get database
                dbase = client[database]
                #fetch the data and put it into a pandas dataframe
                try:
                   if statement == "":
                      cursor = dbase[table].find()

                   else:
                      cursor = dbase[table].find(statement)

                   self.dataframe = pd.DataFrame(list(cursor))
                   del(self.dataframe["_id"])
                   cursor.close()
                   client.close()

                except CursorNotFound as err:
                    self.dataframe = "Error: "+ str(err)

            except ConnectionFailure as err:
                self.dataframe = "Error: " + str(err)

        #get data from PostgreSQL database
        elif db == "PostgreSQL":
            try:
                pygrehost = host + ":" + port
                conn = "connect(database=database,host=pygrehost,user=user,password=password)"
                try:
                    if statement == "":
                        self.dataframe = pd.read_sql("SELECT * FROM " + table, con=conn)
                    else:
                        self.dataframe = pd.read_sql(statement, con=conn)

                except DatabaseError as err:
                    self.dataframe = "Error: " + str(err)

            except  :
                self.dataframe = "Error: cannot connect to the database"

        #get data from a cassandar cluster
        if db == "Cassandra":
            cluster_list = host.split(" ")
            cluster = Cluster(cluster_list,port=port,protocol_version=3)
            try:
                session = cluster.connect()
                session.row_factory = dict_factory
                if statement == "":
                    rows = session.execute("SELECT * FROM " + table)
                else:
                    rows = session.execute(statement)
                self.dataframe = pd.DataFrame(list(rows))
                session.shutdown()


            except DriverException as err:
                print("Error: " + str(err))


        self.dataBrowser.setText(str(self.dataframe))
        self.dfName = table
        self.type = "dataset"

    #import data by closing the window
    def importData(self):
        if "Error: " not in self.dataframe:
            self.close()
            return (self.dfName,self.dataframe,self.type)


















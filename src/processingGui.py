from PyQt4 import QtGui,QtCore,uic
import numpy as np
import pandas as pd

class PreprocessorGui(QtGui.QDialog):
    def __init__(self):
        super(PreprocessorGui,self).__init__()
        uic.loadUi("../ui/processing.ui",self)
        self.show()
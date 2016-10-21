from src.MainGui import mainWindow
from PyQt4 import QtGui
import sys


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = mainWindow()
    app.exec()

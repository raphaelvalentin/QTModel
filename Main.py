"""
Author: Raphael.
"""

__version__ = '0.4'

import sys, os
from PyQt4 import QtCore, QtGui

from UI_Widgets.Ui_MainWindow import Ui_MainWindow

         
class QTModel(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QTModel, self).__init__(parent)
        self.ui = Ui_MainWindow()
        #self.setWindowIcon(QtGui.QIcon('LayoutCreator.ico'))        
        self.ui.setupUi(self)
        



def main():
    global app
    app = QtGui.QApplication(sys.argv)
    form = QTModel()
    form.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
 

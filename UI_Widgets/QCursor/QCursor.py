
    
import sys
from PyQt4 import QtCore, QtGui
from Ui_Cursor import Ui_Cursor




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(MainWindow.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
 
        data = [
                ['x1', 0, 1e3, 1e4],
                ['x2', 1e-6, 1.5e-6, 2e-6],
               ['x3', -1, 0, 1],
                
                   ]
                
        self.setupCursor(MainWindow, data)        
 
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self._cursors = []
        
        
    def myslot(self, key, value):
        print key, value


    def setupCursor(self, MainWindow, data):
        for key, vmin, value, vmax in data:
            self.centralwidget1 = QtGui.QWidget(MainWindow)
            ui_widget = Ui_Cursor()
            ui_widget.setupUi(self.centralwidget1)
            ui_widget.setLabel(key)
            
            ui_widget.valueChanged.connect(self.myslot)

        
            
            ui_widget.setRange(vmin, vmax)
            ui_widget.setValue(value)
            self.verticalLayout.addWidget(self.centralwidget1)






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())    

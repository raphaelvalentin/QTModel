from PyQt4 import QtCore, QtGui
import QTParamBox 

class Ui_QTParamBox(QtCore.QObject):

    itemChanged = QtCore.pyqtSignal(object)

    def setupUi(self, Form):
        Form.setObjectName( ("Form"))
        Form.resize(900, 900)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(("gridLayout"))
        self.centralwidget = QtGui.QWidget(Form)
        self.paramBox = QTParamBox.QTParamBox()
        self.paramBox.setupUi(self.centralwidget)
        self.gridLayout.addWidget(self.centralwidget, 0, 0, 0, 0)       
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.paramBox.itemChanged.connect( self.itemChanged.emit  )        
        
    def setData(self, data):
        self.paramBox.setData(data)

    def setValue(self, key, value):
        self.paramBox.setValue(key, value)
        
    def data(self):
        return self.paramBox.data()
    
    def headerData(self):
        return self.paramBox.headerData()

    def addEmptyRow(self):
        self.paramBox.addEmptyRow()
        
    def delRow(self):
        self.paramBox.delRow()
        
    def setRow(self, i, key, values):
        self.paramBox.setRow(i, key, values)
        
            

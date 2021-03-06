from PyQt4 import QtCore, QtGui
import QDataListView 

class Ui_QDataListView(QtCore.QObject):

    currentValueChanged = QtCore.pyqtSignal(object)

    def setupUi(self, Form):
        Form.setObjectName( ("Form"))
        Form.resize(100, 100)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName( ("gridLayout"))
        self.dataTree = QDataListView.DataTree(Form)
        self.dataTree.setSizeHint(135, 135)
        self.dataTree.currentValueChanged.connect( self.currentValueChanged.emit  )
        self.gridLayout.addWidget(self.dataTree, 0, 0, 0, 0)
        
        QtCore.QMetaObject.connectSlotsByName(Form)

    def setData(self, data):
        self.dataTree.setData(data)
        
    def getSelectedRow(self):
        return self.dataTree.getSelectedRow()

    def getPlotIndexes(self):
        return self.dataTree.getPlotIndexes()

    def getBenchIndex(self):
        return self.dataTree.getBenchIndex()

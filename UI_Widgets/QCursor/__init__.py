from PyQt4 import QtCore, QtGui
import Ui_Cursor 

class Ui_QCursorWindow(QtCore.QObject):

    valueChanged = QtCore.Signal(str, float)

    def setupUi(self, Form, data=[]):
        Form.setObjectName( ("Form"))
        Form.resize(900, 900)
        #self.centralwidget = QtGui.QWidget(Form)
        #self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        if len(data):
            self.setupCursor(Form, data)        
            spacerItem = QtGui.QSpacerItem(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
            self.verticalLayout.addItem(spacerItem)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def valueChangedSlot(self, key, value):
        self.valueChanged.emit(key, value)

    def setupCursor(self, Form, data):
        for key, vmin, value, vmax in data:
            self.parent = QtGui.QWidget(Form)
            ui_widget = Ui_Cursor.Ui_Cursor()
            ui_widget.setupUi(self.parent)
            ui_widget.setLabel(key)
            ui_widget.valueChanged.connect(self.valueChangedSlot)
            ui_widget.setRange(vmin, vmax)
            ui_widget.setValue(value)
            self.verticalLayout.addWidget(self.parent)



        

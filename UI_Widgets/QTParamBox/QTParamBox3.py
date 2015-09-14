# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ParamView.ui'
#
# Created: Tue Apr 28 17:35:20 2015
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class QTParamBox(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(402, 456)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(4)
        self.verticalLayout.addWidget(self.tableWidget)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
	
	#print dir(self.tableWidget)
	
	#self.tableWidget.resizeColumnsToContents()
	
	self.tableWidget.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Name", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Value", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Min", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Max", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Max", None))
	
    def setData(self, table):
        n = len(table)
	self.getRowCount = n
        self.tableWidget.setRowCount(n)

	for i, row in enumerate(table):
 	
            for j, value in enumerate(row):
                item = QtGui.QTableWidgetItem()
	        if j==0:
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                  QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Checked)
		    
		self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)
                item.setText(_translate("Form", str(value), None))
		
	hh = self.tableWidget.horizontalHeader()
        hh.setStretchLastSection(True)	


    def setValue(self, i, value):
        item = QtGui.QTableWidgetItem()
	self.tableWidget.setItem(2, i, item)
        item = self.tableWidget.item(2, i)
        item.setText(_translate("Form", str(value), None))
    
    @property
    def data(self):
        array2d = []
	for i in xrange(self.getRowCount):
	    row = []
            for j in xrange(3):
	        item = self.tableWidget.item(i, j)
	        row.append( float(item.text()) )
	    array2d.append(row)
        return array2d
    
    @property
    def headerData(self):
        row = []
	for i in xrange(self.getRowCount):
            item = self.tableWidget.verticalHeaderItem(i)
            row.append( str(item.text()) )
	return row

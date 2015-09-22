# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from time import time

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

class QTParamBox(QtCore.QObject):

    itemChanged = QtCore.pyqtSignal(tuple)

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
        self.getRowCount = 0
        self.lastChanged = time()

	hh = self.tableWidget.horizontalHeader()
        hh.setStretchLastSection(False)	
	hh.setResizeMode(0, QtGui.QHeaderView.Stretch | QtGui.QHeaderView.Interactive)
	hh.setResizeMode(1, QtGui.QHeaderView.Fixed)
	hh.setResizeMode(2, QtGui.QHeaderView.Fixed)
	hh.setResizeMode(3, QtGui.QHeaderView.Fixed)
	self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
	

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Name", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Min", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Value", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Max", None))

        def pseudofunction(*args):
           # do not to emit when items changed to fast (turn-around for a bug, not good...)
           if time() - self.lastChanged > 0.2: 
               item = self.tableWidget.item(*args)
	       if str(item.text())=='':
	           return
	       self.lastChanged = time()
           self.itemChanged.emit(args)
        self.tableWidget.cellChanged.connect(pseudofunction) 

    def setData(self, table):
	for i, row in enumerate(table):
            self.setRow(i, row[0], row[1:])
		
    def setValue(self, key, value):
        for i in xrange(self.getRowCount):
	    item = self.tableWidget.item(i, 0)
	    if str(item.text()) == key:
	        item = QtGui.QTableWidgetItem()
	        self.tableWidget.setItem(i, 2, item)
	        item = self.tableWidget.item(i, 2)
                item.setText(_translate("Form", str(value), None))
                return

    def setRow(self, i, key, values):

        # add new row
	self.getRowCount += 1
        self.tableWidget.setRowCount(self.getRowCount)
        # write key
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(i, 0, item)
        item = self.tableWidget.item(i, 0)
        item.setText(_translate("Form", str(key), None))
        # write values
        for j, value in enumerate(values):
            item = QtGui.QTableWidgetItem()
	    self.tableWidget.setItem(i, j+1, item)
            item = self.tableWidget.item(i, j+1)
            item.setText(_translate("Form", str(value), None))
                
    def data(self):
        array2d = []
	for i in xrange(self.getRowCount):
	    row = []
            for j in xrange(4):
	        item = self.tableWidget.item(i, j)
	        item = str(item.text())
	        if item.isalpha():
	            row.append( item )
	        else:
	            try:
	                row.append( float(item) )
	            except:
	                row.append( item )
	    array2d.append(row)
        return array2d
    
    def headerData(self):
        row = []
	for i in xrange(self.getRowCount):
            item = self.tableWidget.verticalHeaderItem(i)
            row.append( str(item.text()) )
	return row

    def addEmptyRow(self):
        self.getRowCount += 1
        self.tableWidget.setRowCount(self.getRowCount)
	
    def delRow(self):
        selectedRows = self.tableWidget.selectionModel().selectedRows()
        iRows = [indx.row() for indx in selectedRows]
        x = range(self.getRowCount)
        a = []
        while len(iRows):
            b = iRows.pop()
            a.append(x.index(b))
        for i in a:
            self.tableWidget.removeRow(i)
            self.getRowCount -= 1
 

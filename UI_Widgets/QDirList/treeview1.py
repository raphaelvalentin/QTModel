# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'treeview.ui'
#
# Created: Wed Apr 29 14:46:27 2015
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(200, 300)
        self.centralwidget = QtGui.QWidget(Form)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.treeView = QtGui.QTreeView(Form)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.horizontalLayout.addWidget(self.treeView)
        Form.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        
        self.model = QtGui.QDirModel()        
        

        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index('.'))
        
        #filter = ['*.*']
        #self.model.setNameFilters(filter) 
        
        
        

        #self.model.setNameFilters(filter)
        
        help(self.model.setNameFilters)



        
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        #self.treeView.hideColumn(3)

        self.treeView.setAnimated(False)
        self.treeView.setIndentation(20)
        self.treeView.setSortingEnabled(True)

        self.treeView.setWindowTitle("Dir View")
        self.treeView.resize(350, 480)

        self.treeView.doubleClicked.connect(lambda item: self.doubleClickedAction(item))
        


    def doubleClickedAction(self, item):
        i = item.row()
        indexItem = self.model.index(i, 0, item.parent())
        print self.model.filePath(indexItem)
        
        


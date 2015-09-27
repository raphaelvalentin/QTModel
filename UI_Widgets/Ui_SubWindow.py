
from PyQt4 import QtCore, QtGui
from QTextEdit import Ui_QTextEditWindow
from QTParamBox import Ui_QTParamBox
from QDataListView import Ui_QDataListView
from QInterPy import Ui_LogSubWindow
from PyQTGraph import Ui_pyQTGraph
from QCursor import Ui_QCursorWindow



class QMdiParameterBoxSubWindow(QtGui.QMdiSubWindow):

    itemChanged = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super(QMdiParameterBoxSubWindow,self).__init__(parent)
        self.setWindowTitle( 'Untitled3' )
        self.setWindowIcon(QtGui.QIcon('LayoutCreator.ico'))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.resize(500, 300)
        widget = QtGui.QWidget()
        self.subwin_abq = Ui_QTParamBox()
        self.subwin_abq.setupUi(widget)
        widget.setParent(self)
        self.setWidget(widget)
        parent.addSubWindow(self)
        self.widget = widget
        self.show()
        self.subwin_abq.itemChanged.connect( self.itemChanged.emit  )        

    def addEmptyRow(self):
        self.subwin_abq.addEmptyRow()

    def delRow(self):
        self.subwin_abq.delRow()

    def setData(self, data):
        self.subwin_abq.setData(data)

    def setValue(self, key, value):
        self.subwin_abq.setValue(key, value)

    def setRow(self, i, key, row):
        self.subwin_abq.setRow(i, key, row)
        
    def data(self):
        return self.subwin_abq.data()
        
    def iteritems(self):
        for key, min, value, max in self.subwin_abq.data():
            yield key, value
    
    def headerData(self):
        return self.subwin_abq.headerData()
        
    def setFilename(self, filename):
        self.__filename__ = str(filename)
        self.setWindowTitle( filename.split('/')[-1].split('\\')[-1] + ' - ' + filename )
        
    def filename(self):
        return self.__filename__
        
# generic
class QMdiScriptSubWindow(QtGui.QMdiSubWindow):

    def __init__(self, parent):
        super(QMdiScriptSubWindow,self).__init__(parent)
        self.setWindowTitle( 'Untitled' )
        self.setWindowIcon(QtGui.QIcon('LayoutCreator.ico'))
        self.resize(500, 400)
        widget = QtGui.QWidget()
        self.subwin_abq = Ui_QTextEditWindow()
        self.subwin_abq.setupUi(widget)
        widget.setParent(self)
        self.setWidget(widget)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.show()

    def text(self):
        return str(self.subwin_abq.plainTextEdit.edit.toPlainText())

    def setText(self, string):
        self.subwin_abq.plainTextEdit.setText(string)
        
    def setFilename(self, filename):
        self.__filename__ = str(filename)
        self.setWindowTitle( filename.split('/')[-1].split('\\')[-1] + ' - ' + filename )
        
    def filename(self):
        return self.__filename__
        


class DockDataTreeSubWindow(QtGui.QDockWidget):

    currentValueChanged = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super(DockDataTreeSubWindow,self).__init__(parent)
        self.setWindowTitle( 'Project Manager' )
        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.setMinimumWidth(140)


        widget = QtGui.QWidget()
        self.subwin_abq = Ui_QDataListView()
        self.subwin_abq.setupUi(widget)
        self.setWidget(widget)
        parent.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
        self.subwin_abq.currentValueChanged.connect( self.currentValueChanged.emit  )        
        
    def setData(self, data):
        self.subwin_abq.setData(data)

    def getSelectedRow(self):
        return self.subwin_abq.getSelectedRow()

    def getPlotIndexes(self):
        return self.subwin_abq.getPlotIndexes()

    def getBenchIndex(self):
        return self.subwin_abq.getBenchIndex()

   
class DockLogSubWindow(QtGui.QDockWidget):
    def __init__(self, parent):
        super(DockLogSubWindow,self).__init__(parent)
        self.setWindowTitle( 'Log File' )
        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        widget = QtGui.QWidget()
        self.subwin_abq = Ui_LogSubWindow()
        self.subwin_abq.setupUi(widget)
        self.setWidget(widget)
        parent.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
        
    def append(self,text):
        self.subwin_abq.plainTextEdit.moveCursor(QtGui.QTextCursor.End)
        self.subwin_abq.plainTextEdit.insertPlainText( text )
       


class QMdiPlotSubWindow(QtGui.QMdiSubWindow):
    def __init__(self, parent, plt):
        super(QMdiPlotSubWindow,self).__init__(parent)
        self.setWindowTitle( 'Untitled' )
        self.setWindowIcon(QtGui.QIcon('LayoutCreator.ico'))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.resize(500, 300)
        widget = QtGui.QWidget()
        self.subwin_abq = Ui_pyQTGraph()
        self.subwin_abq.setupUi(widget, plt)
        widget.setParent(self)
        self.setWidget(widget)
        parent.addSubWindow(self)
        self._isClosed = False
        self.show()

    def update(self, plt):
        self.subwin_abq.update(plt)
        
    def setName(self, name):
        self._name = name
        self.setWindowTitle( name )
        
    def name(self):
        if hasattr(self, '_name'):
            return self._name
        else:
            return None

    def closeEvent(self, event):
        super(QMdiPlotSubWindow,self).closeEvent(event)
        self._isClosed = True
    
    def isClosed(self):
        return self._isClosed

    def reopen(self, plt):
        widget = QtGui.QWidget()
        self.subwin_abq = Ui_pyQTGraph()
        self.subwin_abq.setupUi(widget, plt)
        widget.setParent(self)
        self.setWidget(widget)
        self._isClosed = False
        self.show()
        
            


class QMdiCursorSubWindow(QtGui.QMdiSubWindow):

    valueChanged = QtCore.Signal(str, float)

    def __init__(self, parent, data):
        super(QMdiCursorSubWindow,self).__init__(parent)
        self.setWindowTitle( 'Cursor' )
        self.setWindowIcon(QtGui.QIcon('LayoutCreator.ico'))
        self.resize(500, 400)
        widget = QtGui.QWidget()
        self.subwin_abq = Ui_QCursorWindow()
        self.subwin_abq.setupUi(widget, data)
        self.subwin_abq.valueChanged.connect(self.valueChangedSlot)
        widget.setParent(self)
        parent.addSubWindow(self)
        self.setWidget(widget)
        self.adjustSize()
        self.show()
        
    def valueChangedSlot(self, key, value):
        self.valueChanged.emit(key, value)
        




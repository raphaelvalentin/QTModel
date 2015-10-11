from PyQt4 import QtCore, QtGui
import sys
from Queue import Queue
from exec_script import Interpy

__all__ = ['WriteStream', 'MyReceiver', 'queue', 'QInterpy', 'Ui_LogSubWindow']
        
class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue
        
    def write(self, text):
        self.queue.put(text)

class MyReceiver(QtCore.QObject):
    mysignal = QtCore.pyqtSignal(str)
    
    def __init__(self,queue,*args,**kwargs):
        super(MyReceiver,self).__init__(*args,**kwargs)
        self.queue = queue

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)
 

queue = Queue()

class QInterpy(QtCore.QThread):

    finished = QtCore.pyqtSignal()
    
    mutex = QtCore.QMutex()

    def __init__(self,locals={},*args,**kwargs):
        super(QInterpy,self).__init__(*args,**kwargs)
        self.interpy = Interpy(locals)
        self.locals = self.interpy.locals

    def run(self):
        QInterpy.mutex.lock()
        sys.stdout = WriteStream(queue)
        self.interpy.runsource(self.source, self.filename, symbol='exec')
        self.locals = dict(self.interpy.locals)
        sys.stdout = sys.__stdout__
        QInterpy.mutex.unlock()
        self.finished.emit()
        
    def runsource(self, source, filename="<source>"):
        self.source = source
        self.filename = filename

    def __del__(self):
        QInterpy.mutex.unlock()
        self.wait()
    
       
class Ui_LogSubWindow(object):
    def setupUi(self, Form):
        Form.setObjectName( ("Form"))
        Form.resize(800, 640)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName( ("gridLayout"))
        self.plainTextEdit = _QTextEdit("", Form)
        self.plainTextEdit.setSizeHint(50, 10)
        self.plainTextEdit.setObjectName( ("plainTextEdit"))
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 0, 0)
        QtCore.QMetaObject.connectSlotsByName(Form)
    

    def append(self, text):
        self.plainTextEdit.append(text)


class _QTextEdit(QtGui.QTextEdit):
    _sizehint = None

    def setSizeHint(self, width, height):
        self._sizehint = QtCore.QSize(width, height)

    def sizeHint(self):
        if self._sizehint is not None:
            return self._sizehint
        return super(MyWidget, self).sizeHint()
       


      

import code
from PyQt4 import QtCore, QtGui
import sys
import time
import random


class Interpy(code.InteractiveInterpreter):

    __environ__ = dict(globals())
    
    def __init__(self, locals={}):
        environ = {}
        environ.update( Interpy.__environ__ )
        environ.update( locals )
        code.InteractiveInterpreter.__init__(self, locals=environ)

    def runcode(self, code):
        try:
            exec code in self.locals
        except:
            self.showtraceback() 




class GenericThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function(*self.args,**self.kwargs)
        return


class MyApp(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 280, 600)
        self.setWindowTitle('threads')

        self.layout = QtGui.QVBoxLayout(self)

        self.testButton = QtGui.QPushButton("test")
        self.connect(self.testButton, QtCore.SIGNAL("released()"), self.test)
        self.listwidget = QtGui.QListWidget(self)

        self.layout.addWidget(self.testButton)
        self.layout.addWidget(self.listwidget)

        self.threadPool = []
        

    def add(self, text):
        """ Add item to list widget """
        print "Add: " + text
        self.listwidget.addItem(text)
        #self.listwidget.sortItems()


    def addBatch2(self,text="",iters=6,delay=0.3):
        for i in range(iters):
            #time.sleep(delay) # artificial time delay
            session = Interpy(locals={'sleep':time.sleep, 'random':random.random})
            session.runcode(text)
            self.emit( QtCore.SIGNAL('add(QString)'), 'toto'  + str(i) )

        
    def test(self):
        self.listwidget.clear()

        # generic thread using signal
        
        self.threadPool.append( GenericThread(self.addBatch2,"sleep(random())",delay=0.3) )
        self.disconnect( self, QtCore.SIGNAL("add(QString)"), self.add )
        self.connect( self, QtCore.SIGNAL("add(QString)"), self.add )
        
        
        help(self.threadPool)
        self.threadPool[len(self.threadPool)-1].start()


  
# run
app = QtGui.QApplication(sys.argv)
test = MyApp()
test.show()
app.exec_()  

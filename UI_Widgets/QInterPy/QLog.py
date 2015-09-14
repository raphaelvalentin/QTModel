import sys
from Queue import Queue
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

class MyReceiver(QObject):
    mysignal = pyqtSignal(str)

    def __init__(self,queue,*args,**kwargs):
        QObject.__init__(self,*args,**kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)


# Create Queue and redirect sys.stdout to this queue
queue = Queue()
sys.stdout = WriteStream(queue)

# Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
thread = QThread()
my_receiver = MyReceiver(queue)
my_receiver.mysignal.connect(app.appendText)
my_receiver.moveToThread(thread)
thread.started.connect(my_receiver.run)
thread.start()



import sys, os

from PyQt4 import QtCore, QtGui
#from pyqtgraph.Qt import QtCore, QtGui


class base(QtCore.QObject):

    valueChanged = QtCore.pyqtSignal(object, object)

    def __init__(self):
        super(base, self).__init__()
        self.keys = []
        self.values = []

    def __len__(self):
        return self.keys.__len__()
        
    def __getitem__(self, key):
        i = self.keys.index(key)
        return self.values[i]

    def __setitem__(self, key, value):
        try:
            i = self.keys.index(key)
            self.values[i] = value
            self.valueChanged.emit(key, value)
            return value
        except ValueError:
            self.keys.append(key)
            self.values.append(value)

    def iteritems(self):
        for key, value in zip(self.keys, self.values):
            yield key, value         
        


base1 = base()

def f(*s):
    print 'write', s
base1.valueChanged.connect(f)

base1['toto'] = 123
base1['toto'] = 124
   

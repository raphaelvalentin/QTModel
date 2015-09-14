#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
import numpy as np
import pyqtgraph as pg

from time import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

def rand(n):
    data = np.random.random(n)
    data[int(n*0.1):int(n*0.13)] += .5
    data[int(n*0.18)] += 2
    data[int(n*0.1):int(n*0.13)] *= 5
    data[int(n*0.18)] *= 20
    data *= 1e-12
    return data, np.arange(n, n+len(data)) / float(n)



    
class Ui_pyQTGraph(object):
    def setupUi(self, Form):
        Form.setObjectName( ("PyQTGraph"))
        Form.resize(500, 500)
        self.pyQTGraphWidget = QtGui.QWidget(Form)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        Form.setCentralWidget(self.pyQTGraphWidget)
        self.pyQTGraphWidget.setLayout(self.verticalLayout)
        pw = pg.PlotWidget(name='Plot1')
        p1 = pw.plot()
        p1.setPen((0,0,0), width=2, cosmetic=True)
        yd, xd = rand(100)
        p1.setData(y=yd, x=xd)
        
        pw.setBackgroundBrush(QBrush(QColor(Qt.white)))
        labelStyle = {'color': '#000', 'font-size': '13pt'}         
        pw.showGrid(x=True, y=True) 
        pw.getAxis('bottom').setPen((0,0,0), width=2, cosmetic=True)
        pw.getAxis('left').setPen((0,0,0), width=2, cosmetic=True) 
        self.verticalLayout.addWidget(pw)
        
        pw.setLabel('left', 'Value', units='V', **labelStyle)
        pw.setLabel('bottom', 'Time', units='s', **labelStyle)
        pw.setXRange(0, 2)
        pw.setYRange(0, 1e-10)
        self.p1 = p1
        

        p2 = pw.plot()
        yd, xd = rand(20)
        p2.setData(y=yd, x=xd)
        p2.setPen((0,200,0), width=3, cosmetic=True)
       
        help(p1.setSymbol)
        
        
    def updateData(self):
        yd, xd = rand(20)
        self.p1.setData(y=yd, x=xd)


       

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_pyQTGraph()
        self.ui.setupUi(self)

    def update(self):
        self.ui.updateData()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    
    t = QtCore.QTimer()
    t.timeout.connect(myapp.update)
    t.start(200)

    
    myapp.show()
    sys.exit(app.exec_())        


#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
import numpy as np
import pyqtgraph as pg
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Ui_pyQTGraph(object):
    def setupUi(self, Form):
        Form.setObjectName( ("PyQTGraph"))
        Form.resize(500, 500)
        self.pyQTGraphWidget = QtGui.QWidget(Form)
        Form.setCentralWidget(self.pyQTGraphWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.pyQTGraphWidget.setLayout(self.verticalLayout)

    def addFigure(self, xlabel='x-coordinate', ylabel='y-coordinate'):
        self.fig = pg.PlotWidget(name='Plot')
        self.fig.setBackgroundBrush(QBrush(QColor(Qt.white)))
        self.fig.showGrid(x=True, y=True) 
        self.fig.getAxis('bottom').setPen(pg.mkPen(0,0,255))
        self.fig.getAxis('left').setPen(pg.mkPen(255,0,0)) 
        labelStyle = {'color': '#000', 'font-size': '13pt'}         
        self.fig.setLabel('left', ylabel, units='', **labelStyle)
        self.fig.setLabel('bottom', xlabel, units='', **labelStyle)
        self.verticalLayout.addWidget(self.fig)

    def addPlot(self, x, y):
        p1 = self.fig.plot()
        p1.setPen((0,0,0), width=2, cosmetic=True)
        p1.setData(y=y, x=x)
        self.fig.enableAutoRange('xy', False)
        return p1
        
    def addScatter(self, x, y):
        p1 = self.fig.plot()
        p1.setPen(None)
        p1.setSymbol('s')
        p1.setSymbolPen(None)
        p1.setSymbolSize(10)
        p1.setSymbolBrush((100, 100, 255, 50))
        p1.setData(y=y, x=x)
        self.fig.enableAutoRange('xy', False)
        return p1
        
       

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_pyQTGraph()
        self.ui.setupUi(self)

    #def update(self):
    #    self.ui.updateData()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    
    t = QtCore.QTimer()
    t.timeout.connect(myapp.update)
    t.start(200)

    
    myapp.show()
    sys.exit(app.exec_())        


def rand(n):
    data = np.random.random(n)
    data[int(n*0.1):int(n*0.13)] += .5
    data[int(n*0.18)] += 2
    data[int(n*0.1):int(n*0.13)] *= 5
    data[int(n*0.18)] *= 20
    data *= 1e-12
    return data, np.arange(n, n+len(data)) / float(n)



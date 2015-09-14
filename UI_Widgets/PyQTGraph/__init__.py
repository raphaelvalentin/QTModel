#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
import numpy as np
import pyqtgraph as pg

__all__ = ['Ui_pyQTGraph']

    
class Ui_pyQTGraph(object):

    def setupUi(self, Form, plt):
        Form.setObjectName( ("PyQTGraph"))
        Form.resize(500, 500)
        Form.setWindowTitle('X-Y Plot')
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName( ("gridLayout"))
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        widget = pg.PlotWidget()
        self.PlotWidget = Ui_PlotWidget()
        self.PlotWidget.setupUi(widget)
        self.PlotWidget.plot(plt)
        self.gridLayout.addWidget(widget, 0, 0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def update(self, plt):
        self.PlotWidget.clear()
        self.PlotWidget.plot(plt)
        
class Ui_PlotWidget(object):

    def setupUi(self, widget):
        widget.setBackgroundBrush(QtGui.QBrush( QtGui.QColor(255, 255, 255) ))
        widget.showGrid(x=True, y=True) 
        widget.getAxis('bottom').setPen((0,0,0), width=2, cosmetic=True)
        widget.getAxis('left').setPen((0,0,0), width=2, cosmetic=True)
        widget.setLabel('bottom', **{'color':'#000', 'font-size':'13pt'})
        widget.setLabel('left', **{'color':'#000', 'font-size':'13pt'})
        self.widget = widget

    def plot(self, plt):
        self.widget.setLabel('bottom', plt['xlabel'], units=plt['xunit'])
        self.widget.setLabel('left', plt['ylabel'], units=plt['yunit'])
        for curve_type, x, y, color in reversed(plt['items']):
            if curve_type is 'line':
                curve = self.widget.plot()
                curve.setPen(color, width=2, cosmetic=True)
                curve.setData(y=y, x=x)
            elif curve_type is 'scatter':
                curve = self.widget.scatterPlot(symbolBrush=color, symbolPen='w', size=6)
                curve.setData(y=y, x=x)

    def clear(self):
        self.widget.clear()
    


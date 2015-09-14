# -*- coding: utf-8 -*-

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

__all__ = ['Ui_Cursor']


import numpy as np
import re
import math

SI = {'':1, 'k':1e3, 'M':1e6, 'G':1e9, 'T':1e12, 'P':1e15, 'E':1e18, 'Z':1e21, 'Y':1e24, 
      'm':1e-3, 'µ':1e-6, 'n':1e-9, 'p':1e-12, 'f':1e-15, 'a':1e-18, 'z':1e-21, 'y':1e-24 }


def ToSI(d):
  incPrefixes = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
  decPrefixes = ['m', 'µ', 'n', 'p', 'f', 'a', 'z', 'y']

  degree = int(math.floor(math.log10(math.fabs(d)) / 3))

  prefix = ''

  if degree!=0:
    ds = degree/math.fabs(degree)
    if ds == 1:
      if degree - 1 < len(incPrefixes):
        prefix = incPrefixes[degree - 1]
      else:
        prefix = incPrefixes[-1]
        degree = len(incPrefixes)

    elif ds == -1:
      if -degree - 1 < len(decPrefixes):
        prefix = decPrefixes[-degree - 1]
      else:
        prefix = decPrefixes[-1]
        degree = -len(decPrefixes)

    scaled = float(d * math.pow(1000, -degree))

    return scaled, prefix

  else:
    return d, ''


class QDoubleSpinBox(QtGui.QDoubleSpinBox):
    def setValue(self, value):
        value, suffix = ToSI(value)
        super(QDoubleSpinBox, self).setValue(value)
        super(QDoubleSpinBox, self).setSuffix(suffix)

    def value(self):
        value = super(QDoubleSpinBox, self).value()
        suffix = super(QDoubleSpinBox, self).suffix()
        return value*SI[suffix]

        
class ScientificDoubleSpinBox(QtGui.QDoubleSpinBox):

    def __init__(self, *args, **kwargs):
        super(ScientificDoubleSpinBox, self).__init__(*args, **kwargs)
        self.setMinimum(-np.inf)
        self.setMaximum(np.inf)
        self.validator = FloatValidator()
        #self.setDecimals(1000)

    def validate(self, text, position):
        return self.validator.validate(text, position)

    def fixup(self, text):
        return self.validator.fixup(text)

    def valueFromText(self, text):
        return float(text)

    def textFromValue(self, value):
        return format_float(value)

    def stepBy(self, steps):
        text = self.cleanText()
        groups = _float_re.search(text).groups()
        decimal = float(groups[1])
        decimal += steps
        new_string = "{:g}".format(decimal) + (groups[3] if groups[3] else "")
        self.lineEdit().setText(new_string)

_float_re = re.compile(r'(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)')

def valid_float_string(string):
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False

def format_float(value):
    """Modified form of the 'g' format specifier."""
    string = "{:g}".format(value).replace("e+", "e")
    string = re.sub("e(-?)0*(\d+)", r"e\1\2", string)
    return string

class FloatValidator(QtGui.QValidator):

    def validate(self, string, position):
        string= str(string)
        if valid_float_string(string):
            return (QtGui.QValidator.Acceptable, position)
        if string == "" or string[position-1] in 'e.-+':
            return (QtGui.QValidator.Intermediate, position)
        return (QtGui.QValidator.Invalid, position)

    def fixup(self, text):
        match = _float_re.search(text)
        return match.groups()[0] if match else ""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

class Ui_Cursor(QtCore.QObject):

    valueChanged = QtCore.Signal(str, float)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalLayout.setMargin(5)        
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.horizontalSlider = QtGui.QSlider(Form)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        
        self.precisionSlider = 10000.0
        self.horizontalSlider.setRange(0, self.precisionSlider)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalLayout.addWidget(self.horizontalSlider)

        self.doubleSpinBox = pg.SpinBox(parent=Form, suffix='', siPrefix=True, dec=True, decimals=3)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.doubleSpinBox.setFixedWidth(80)
        self.doubleSpinBox.setFixedHeight(25)
        self.horizontalLayout.addWidget(self.doubleSpinBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        
        def SliderSetValueSlot(value):
            self.doubleSpinBox.setValue(value)
            minimum, maximum = self._minimum, self._maximum
            value = self.precisionSlider*(value-minimum)/(maximum-minimum)
            self.horizontalSlider.setValue(int(value))
            
        def SpinBoxSetValueSlot(value):
            minimum, maximum = self._minimum, self._maximum
            value = (minimum*(self.precisionSlider-value)+maximum*value)/self.precisionSlider
            self.doubleSpinBox.setValue(value)

        self.doubleSpinBox.valueChanged.connect(SliderSetValueSlot)
        self.horizontalSlider.valueChanged.connect(SpinBoxSetValueSlot)
        
        def ValueEmit1(*args):
            name = self.label.text()
            value = self.doubleSpinBox.value()
            self.valueChanged.emit(name, value)
        
        def ValueEmit2(*args):
            if self.doubleSpinBox.hasFocus():
                name = self.label.text()
                value = self.doubleSpinBox.value()
                self.valueChanged.emit(name, value)
        
        self.horizontalSlider.sliderReleased.connect(ValueEmit1)
        self.doubleSpinBox.sigValueChanged.connect(ValueEmit2)


    def setLabel(self, label):
        self.label.setText(label)
        
    def label(self):
        return self.label.text()
        
    def setRange(self, minimum, maximum):
        self._minimum, self._maximum = minimum, maximum
        d = maximum-minimum
        self.doubleSpinBox.setOpts(step=0.01, minStep=min(0.01,d/100.))
        self.doubleSpinBox.setMinimum(minimum, update=False)
        self.doubleSpinBox.setMaximum(maximum, update=True)
        value = self.doubleSpinBox.value()
        value = self.precisionSlider*(value-minimum)/(maximum-minimum)
        self.horizontalSlider.setValue(int(value))

    def setValue(self, value):
        self.doubleSpinBox.setValue(value)
        minimum, maximum = self._minimum, self._maximum     
        value = self.precisionSlider*(value-minimum)/(maximum-minimum)
        self.horizontalSlider.setValue(int(value))
         
    def value(self):
        return self.doubleSpinBox.value()
        

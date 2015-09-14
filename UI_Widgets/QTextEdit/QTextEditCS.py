#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
# Python 2.7
 
import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from bibcolorsyntax import ColorSyntax # pour coloration syntaxique 


############
from PyQt4.Qt import QFrame, QWidget, QTextEdit, QHBoxLayout, QPainter

#############################################################################
class QTextEditCS(QtGui.QWidget):

    class NumberBar(QWidget):
 
        def __init__(self, *args):
            QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visibile.
            self.highest_line = 0
 
        def setTextEdit(self, edit):
            self.edit = edit
 
        def update(self, *args):
            '''
            Updates the number bar to display the current set of numbers.
            Also, adjusts the width of the number bar if necessary.
            '''
            # The + 4 is used to compensate for the current line being bold.
            width = self.fontMetrics().width(str(self.highest_line)) + 4
            if self.width() != width:
                self.setFixedWidth(width)
            QWidget.update(self, *args)
 
        def paintEvent(self, event):
            contents_y = self.edit.verticalScrollBar().value()
            page_bottom = contents_y + self.edit.viewport().height()
            font_metrics = self.fontMetrics()
            current_block = self.edit.document().findBlock(self.edit.textCursor().position())
 
            painter = QPainter(self)
 
            line_count = 0
            # Iterate over all text blocks in the document.
            block = self.edit.document().begin()
            while block.isValid():
                line_count += 1
 
                # The top left position of the block in the document
                position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()
 
                # Check if the position of the block is out side of the visible
                # area.
                if position.y() > page_bottom:
                    break
 
                # We want the line number for the selected line to be bold.
                bold = False
                if block == current_block:
                    bold = True
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)
 
                # Draw the line number right justified at the y position of the
                # line. 3 is a magic padding number. drawText(x, y, text).
                painter.drawText(self.width() - font_metrics.width(str(line_count)) - 3, round(position.y()) - contents_y + font_metrics.ascent()+3, str(line_count))
 
                # Remove the bold style if it was set previously.
                if bold:
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)
 
                block = block.next()
 
            self.highest_line = line_count
            painter.end()
 
            QWidget.paintEvent(self, event)
 

 
    def __init__(self, script="", parent=None):
        super(QTextEditCS, self).__init__(parent)
        self.resize(800, 600)
        self.script = script
 
        self.edit = QtGui.QTextEdit(self)
 
        # met une police de caractère même largeur pour tous les caractères
        font = QtGui.QFont()
        font.setFamily(u"DejaVu Sans Mono") # police de Qt4
        font.setStyleHint(QtGui.QFont.Courier) # si la police est indisponible
        font.setPointSize(10)
        self.edit.setFont(font)
 
        # met en place la coloration syntaxique
        self.colorSyntax = ColorSyntax(self.edit.document())
 
        # affiche le script colorisé
        self.setText(self.script)
 
        # positionne le QTextEdit dans la fenêtre
        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)
        
        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)
        layout.addWidget(self.number_bar)
        layout.addWidget(self.edit)
        self.setLayout(layout)

        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)
 
    def eventFilter(self, object, event):
        # Update the line numbers for all events on the text edit and the viewport.
        # This is easier than connecting all necessary singals.
        if object in (self.edit, self.edit.viewport()):
            self.number_bar.update()
            return False
        return QFrame.eventFilter(object, event)
 


    #========================================================================
    def setText(self, chaineunicode):
        """Ecrire dans le widget edit (QTextEdit)"""
        self.edit.append(chaineunicode)
        # fait bouger le curseur à la fin du texte
        self.edit.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        # force le rafraichissement pour affichage en temps réel
        QtCore.QCoreApplication.processEvents() 



 
#############################################################################
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
 
    scriptsql = u""""""
 
    fen = QTextEditCS(scriptsql)
    fen.show()
    sys.exit(app.exec_())

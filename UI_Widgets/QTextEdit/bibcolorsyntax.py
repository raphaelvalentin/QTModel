#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
#Python 2.7
 
import os, sys
 
from PyQt4 import QtCore, QtGui
 
#############################################################################
class ColorSyntax(QtGui.QSyntaxHighlighter):
 
    #========================================================================
    def __init__(self, parent=None):
        super(ColorSyntax, self).__init__(parent)
 
        # liste des règles: [[regex, format], [regex, format], ...]
        self.regles = []
 

        #--------------------------------------------------------------------
        #         
        chaine0_format = QtGui.QTextCharFormat()
        chaine0_format.setForeground(QtCore.Qt.blue)
        chaine0_motif = "^(def)+(\s)+([a-zA-Z_][a-zA-Z0-9_]*)"
        chaine0_regex = QtCore.QRegExp(chaine0_motif)
        #chaine0_regex.setMinimal(True)
        self.regles.append([chaine0_regex, chaine0_format])

        chaine0_format = QtGui.QTextCharFormat()
        chaine0_format.setForeground(QtCore.Qt.blue)
        chaine0_motif = "^(class)+(\s)+([a-zA-Z_][a-zA-Z0-9_]*)"
        chaine0_regex = QtCore.QRegExp(chaine0_motif)
        #chaine0_regex.setMinimal(True)
        self.regles.append([chaine0_regex, chaine0_format])

        chaine0_format = QtGui.QTextCharFormat()
        chaine0_format.setForeground(QtCore.Qt.blue)
        chaine0_motif = "(\s)+^(def)+(\s)+([a-zA-Z_][a-zA-Z0-9_]*)"
        chaine0_regex = QtCore.QRegExp(chaine0_motif)
        #chaine0_regex.setMinimal(True)
        self.regles.append([chaine0_regex, chaine0_format])

        #--------------------------------------------------------------------
        # coloration des mots clés Python 
        motcles_format = QtGui.QTextCharFormat()
        orange = QtGui.QColor("orange")
        motcles_format.setForeground(orange) # mots clés en bleu
        # liste des mots à considérer
        motcles_motifs = ["class", "def", "import", "from", "for", "with", "if", "elif", "else", "in", "return", "print", "as", "raise", "and", "or", "break", "not", "while"]
        # enregistrement dans la liste des règles
        for motcles_motif in motcles_motifs:
            motcles_regex = QtCore.QRegExp("\\b" + motcles_motif + "\\b", 
                                                    QtCore.Qt.CaseSensitive)
            self.regles.append([motcles_regex, motcles_format])

        #--------------------------------------------------------------------
        # coloration des mots clés Python 
        motcles_format = QtGui.QTextCharFormat()
        purple = QtGui.QColor("purple")
        motcles_format.setForeground(purple) # mots clés en bleu
        # liste des mots à considérer
        motcles_motifs = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '_', '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin', 'bool', 'buffer', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'long', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']
        # enregistrement dans la liste des règles
        for motcles_motif in motcles_motifs:
            motcles_regex = QtCore.QRegExp("\\b" + motcles_motif + "\\b", 
                                                    QtCore.Qt.CaseSensitive)
            self.regles.append([motcles_regex, motcles_format])

 
        #--------------------------------------------------------------------
        # nombre entier ou flottant
        nombre_format = QtGui.QTextCharFormat()
        nombre_format.setForeground(QtCore.Qt.darkGreen)
        nombre_motif =  "\\b[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?\\b"
        nombre_regex = QtCore.QRegExp(nombre_motif)
        nombre_regex.setMinimal(True)
        #self.regles.append([nombre_regex, nombre_format])
 
        #--------------------------------------------------------------------
        # chaine de caractères simple quote: '...'
        chaine1_format = QtGui.QTextCharFormat()
        chaine1_format.setForeground(QtCore.Qt.darkGreen)#red)
        chaine1_motif = "\'.*\'"
        chaine1_regex = QtCore.QRegExp(chaine1_motif)
        chaine1_regex.setMinimal(True)
        self.regles.append([chaine1_regex, chaine1_format])
 
        #--------------------------------------------------------------------
        # chaine de caractères double quotes: "..."
        chaine2_format = QtGui.QTextCharFormat()
        chaine2_format.setForeground(QtCore.Qt.darkGreen)
        chaine2_motif = '\".*\"'
        chaine2_regex = QtCore.QRegExp(chaine2_motif)
        chaine2_regex.setMinimal(True)
        self.regles.append([chaine2_regex, chaine2_format])
 
        #--------------------------------------------------------------------
        # delimiteur: parenthèses, crochets, accolades
        delimiteur_format = QtGui.QTextCharFormat()
        delimiteur_format.setForeground(QtCore.Qt.red)
        delimiteur_motif = "[\)\(]+|[\{\}]+|[][]+"
        delimiteur_regex = QtCore.QRegExp(delimiteur_motif)
        #self.regles.append([delimiteur_regex, delimiteur_format])
 
        #--------------------------------------------------------------------
        # commentaire sur une seule ligne et jusqu'à fin de ligne: --...\n
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtCore.Qt.red)
        comment_motif = "#[^\n]*"
        comment_regex = QtCore.QRegExp(comment_motif)
        self.regles.append([comment_regex, comment_format])
 
        #--------------------------------------------------------------------
        # commentaires multi-lignes: /*...*/        
        self.commentml_format = QtGui.QTextCharFormat()
        self.commentml_format.setForeground(QtCore.Qt.darkGreen)
 
        self.commentml_deb_regex = QtCore.QRegExp("\"\"\".*")
        self.commentml_fin_regex = QtCore.QRegExp("\"\"\"")
 


    #========================================================================
    def highlightBlock(self, text):
        """analyse chaque ligne et applique les règles"""
 
        # analyse des lignes avec les règles
        for expression, tformat in self.regles:
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, tformat)
                index = expression.indexIn(text, index + length)
 
        self.setCurrentBlockState(0)
 
        #pour les commentaires multilignes: /* ... */ 
        startIndex = 0
        if self.previousBlockState()!=1:
            startIndex = self.commentml_deb_regex.indexIn(text)
 
        while startIndex>=0:
            endIndex = self.commentml_fin_regex.indexIn(text, startIndex)
            if endIndex==-1:
                self.setCurrentBlockState(1)
                commentml_lg = len(text)-startIndex
            else:
                commentml_lg = endIndex-startIndex + \
                                       self.commentml_fin_regex.matchedLength()
 
            self.setFormat(startIndex, commentml_lg, self.commentml_format)
 
            startIndex = self.commentml_deb_regex.indexIn(text, 
                                                       startIndex+commentml_lg)

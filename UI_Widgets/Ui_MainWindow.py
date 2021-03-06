# -*- coding: utf-8 -*-

"""
Author: Raphael.
"""



from PyQt4 import QtCore, QtGui
from QTextEdit import Ui_QTextEditWindow
from QTParamBox import Ui_QTParamBox
from Ui_SubWindow import *
import sys, os
from rawdata.table import table


#from syntax import Bench
def isclass(obj):
    return hasattr(obj, '__dict__')

from UI_Widgets.QInterPy import *
#from Queue import Queue



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

from exec_script import *
__data__ = { 'model' : {},
             'bench' : {},
             'plot'  : {},
             'param' : {},
            }
from UI_Widgets import VariablesData


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, **kwargs):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setSizeIncrement(QtCore.QSize(10, 10))


        MainWindow.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        MainWindow.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        MainWindow.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        MainWindow.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.mdiArea = QtGui.QMdiArea(self.centralwidget)
        self.mdiArea.setSizeIncrement(QtCore.QSize(0, 0))
        self.mdiArea.setObjectName(_fromUtf8("mdiArea"))
        self.verticalLayout.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        # status bar
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        
        # create actions
        self.createActions(MainWindow)
        
        # create menu
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.menubarUi(MainWindow)
        
        self.toolbarUi(MainWindow)
        self.createDockWindows(MainWindow)

        version = kwargs.get('version', None)
        if version:
            MainWindow.setWindowTitle("QTModel %s"%version)
        else:
            MainWindow.setWindowTitle("QTModel")

        self.retranslateUi(MainWindow)

        # manage project path
        from os.path import expanduser
        project_path = os.path.join(expanduser("~"),'.qtmodel')
        if not os.path.exists(project_path):
            os.mkdir(project_path)


        #self.current_path = './Projects'        
        self.current_path = project_path
        self.project_path = project_path      

        # override the closeEvent 
        MainWindow.closeEvent = lambda event: self.closeEvent(MainWindow)
            
        QtCore.QObject.connect( self.mdiArea, QtCore.SIGNAL('subWindowActivated(QMdiSubWindow*)'), 
                                lambda subwindow: self.changedFocusSlot(MainWindow, subwindow) )

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

        
    def retranslateUi(self, MainWindow):
        return 

    # create actions
    def createActions(self, MainWindow):
        icon = QtGui.QIcon.fromTheme("empty")
        self.newScriptAct = QtGui.QAction(icon, "&Script", MainWindow,
                statusTip="Create a new script file", 
                triggered=lambda: self.newScript(MainWindow))
                
        self.newParameterBoxAct = QtGui.QAction("&Parameter Box", MainWindow,
                statusTip="Create a new parameter box", 
                triggered=lambda: self.newParameterBox(MainWindow))

        icon = QtGui.QIcon.fromTheme("document-open")
        self.openAct = QtGui.QAction(icon, "&Open...", MainWindow,
                shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an existing file", 
                triggered=lambda: self.loadFile(MainWindow))

        icon = QtGui.QIcon.fromTheme("document-save")
        self.saveAct = QtGui.QAction(icon, "&Save", MainWindow,
                shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the document to disk", 
                triggered=lambda: self.saveFile(MainWindow))

        icon = QtGui.QIcon.fromTheme("document-save-as")
        self.saveAsAct = QtGui.QAction(icon, "Save &As...", MainWindow,
                shortcut=QtGui.QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=lambda: self.saveAsFile(MainWindow))

        icon = QtGui.QIcon.fromTheme("gtk-close")
        self.exitAct = QtGui.QAction(icon, "E&xit", MainWindow, 
                shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=lambda: self.closeEvent(MainWindow))

        self.tileAct = QtGui.QAction("&Tile", MainWindow, 
                shortcut="Ctrl+T",
                statusTip="Tile the windows",
                triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QtGui.QAction("&Cascade", MainWindow, 
                 shortcut="Ctrl+C",
                statusTip="Cascade the windows",
                triggered=self.mdiArea.cascadeSubWindows)

        self.aboutQtAct = QtGui.QAction("About &Qt", MainWindow,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

        self.aboutAct = QtGui.QAction("&About", MainWindow,
                statusTip="Show the About box",
                triggered=lambda: self.aboutMessageBox(MainWindow))

        icon = QtGui.QIcon.fromTheme("mail-attachment")
        self.AttachToProjectAct = QtGui.QAction(icon, "Attach to Project", MainWindow,
                statusTip="Attach the file to the project",
                triggered=lambda: self.attachToProject(MainWindow))

        self.AddRowAct = QtGui.QAction("Add Row", MainWindow,
                statusTip="Add a row of the table",
                triggered=lambda: self.mdiArea.activeSubWindow().addEmptyRow())

        self.DelRowAct = QtGui.QAction("Delete Row", MainWindow,
                statusTip="Delete rows of the table",
                triggered=lambda: self.mdiArea.activeSubWindow().delRow())

        icon = QtGui.QIcon.fromTheme("gtk-execute")
        self.ExecuteBenchAct = QtGui.QAction(icon, "Execute", MainWindow,
                statusTip="Execute the bench",
                triggered=lambda: self.executeBench(MainWindow, self.DockDataTreeSubWindow.getSelectedRow()))

        icon = QtGui.QIcon("UI_Widgets/StyleSheet/graph-256.png")
        self.TracePlotAct = QtGui.QAction(icon, "Trace Plot", MainWindow,
                statusTip="Trace the plot",
                triggered=lambda: self.tracePlot(MainWindow, self.DockDataTreeSubWindow.getSelectedRow()))

        icon = QtGui.QIcon("UI_Widgets/StyleSheet/preferences-desktop.svg")
        self.OpenCursorBoxAct = QtGui.QAction(icon, "Cursor Box", MainWindow,
                statusTip="Open the cursor box window",
                triggered=lambda: self.newCursorBoxWindow(MainWindow))

        self.AutoExecuteAct = QtGui.QAction("Auto Execute", MainWindow,
                statusTip="Auto Execute the benches", checkable=True
                )

        self.DelVariableData = QtGui.QAction("Del Variable Data", MainWindow,
                statusTip="Delete one variable data", 
                triggered=lambda: self.delVariableData(self.DockDataTreeSubWindow.getSelectedRow()))


    def toolbarUi(self, MainWindow):
        self.toolbar_document = QtGui.QToolBar()
        self.toolbar_document.addAction(self.newScriptAct)
        self.toolbar_document.addAction(self.openAct)
        self.toolbar_document.addAction(self.saveAct)
        self.toolbar_document.addAction(self.saveAsAct)
        self.toolbar_document.addAction(self.exitAct)
        MainWindow.addToolBar(self.toolbar_document)
 
        self.toolbar_action = QtGui.QToolBar()
        self.toolbar_action.addAction(self.AttachToProjectAct)
        self.toolbar_action.addAction(self.ExecuteBenchAct)
        self.toolbar_action.addAction(self.TracePlotAct)
        self.toolbar_action.addAction(self.OpenCursorBoxAct)
        MainWindow.addToolBar(self.toolbar_action)
 
        self.toolbar_table = QtGui.QToolBar()
        self.toolbar_table.addAction(self.AddRowAct)
        self.toolbar_table.addAction(self.DelRowAct)
        MainWindow.addToolBar(self.toolbar_table)
       

    # define the initial menubar
    def menubarUi(self, MainWindow):
        self.menubar.clear()
        
        # set top-level menu bar 
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuFile.setTitle(_translate("MainWindow", "File", None)) 
        self.menubar.addAction(self.menuFile.menuAction())

        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menubar.addAction(self.menuEdit.menuAction())

        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuWindow"))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menubar.addAction(self.menuView.menuAction())

        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName(_fromUtf8("menuWindow"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window", None))
        self.menuWindow.aboutToShow.connect(lambda: self.menubarUiSubWindowFocus(MainWindow))
        self.menubar.addAction(self.menuWindow.menuAction())

        self.menuAction = QtGui.QMenu(self.menubar)
        self.menuAction.setObjectName(_fromUtf8("menuAction"))
        self.menuAction.setTitle(_translate("MainWindow", "Actions", None))
        self.menubar.addAction(self.menuAction.menuAction())
        
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help", None))
        self.menubar.addAction(self.menuHelp.menuAction())
        
        # set second-level menu bar
        icon = QtGui.QIcon.fromTheme("document-new")
        self.menuFileNew = QtGui.QMenu(self.menubar)
        self.menuFileNew.setObjectName(_fromUtf8("menuFile"))
        self.menuFileNew.setTitle(_translate("MainWindow", "New", None)) 
        self.menuFileNew.setIcon(icon)
        self.menuFile.addAction(self.menuFileNew.menuAction())
        
        self.menuFileNew.addAction( self.newScriptAct )
        self.menuFileNew.addAction( self.newParameterBoxAct )
                
        self.menuFile.addAction( self.openAct )
        self.menuFile.addAction( self.saveAct )
        self.menuFile.addAction( self.saveAsAct )
        self.menuFile.addAction( self.exitAct )
        
        #self.menuEdit.addAction( self.AutoExpandTreeAct )

        self.menuWindow.addAction( self.tileAct )
        self.menuWindow.addAction( self.cascadeAct )

        self.menuAction.addAction( self.AttachToProjectAct )
        self.menuAction.addAction( self.ExecuteBenchAct )
        self.menuAction.addAction( self.AutoExecuteAct )
        self.menuAction.addAction( self.DelVariableData )
        self.menuAction.addAction( self.OpenCursorBoxAct )
        self.menuAction.addAction( self.TracePlotAct )   
        self.menuAction.addAction( self.AddRowAct )
        self.menuAction.addAction( self.DelRowAct )

        self.ExecuteBenchAct.setEnabled(False)
        self.OpenCursorBoxAct.setEnabled(False)
        self.TracePlotAct.setEnabled(False)
        self.AddRowAct.setEnabled(False)
        self.DelRowAct.setEnabled(False)
        self.DelVariableData.setEnabled(False)
        self.AttachToProjectAct.setEnabled(False)

        self.menuHelp.addAction( self.aboutAct )
        self.menuHelp.addAction( self.aboutQtAct )


    def warningMessage(self, MainWindow, message=''):    
        QtGui.QMessageBox.warning(MainWindow,
                            "Warning",
                            message)

    def closeEvent(self, MainWindow):
        QtGui.qApp.closeAllWindows()
        QtGui.QApplication.quit()
        raise SystemExit()

    def menubarUiSubWindowFocus(self, MainWindow):
        self.menuWindow.clear()
        self.menuWindow.addAction( self.tileAct )
        self.menuWindow.addAction( self.cascadeAct )
        self.menuWindow.addSeparator()
        for subwindow in self.mdiArea.subWindowList():
            name = str(subwindow.windowTitle())
            short_name = name.split('-')[0].strip()
            def setFocus(subwindow):
                subwindow.showNormal()
                subwindow.raise_()
                subwindow.activateWindow()
                subwindow.setFocus(True)
            menu1 = QtGui.QAction(short_name, MainWindow,
                                  statusTip="Show the window",
                                  triggered= (lambda x: lambda: setFocus(x))(subwindow)) # fix scoping problem
            self.menuWindow.addAction( menu1 )



    #---------------------------------------------------------------------------
    def createDockWindows(self, MainWindow):
    
        self.DockLogSubWindow = DockLogSubWindow(MainWindow)
        self.menuView.addAction(self.DockLogSubWindow.toggleViewAction())

        # log listener
        self.thread1 = QtCore.QThread()
        self.my_receiver = MyReceiver(queue)
        self.my_receiver.mysignal.connect(self.DockLogSubWindow.append)
        self.my_receiver.moveToThread(self.thread1)
        self.thread1.started.connect(self.my_receiver.run)
        self.thread1.start()

        self.DockDataTreeSubWindow = DockDataTreeSubWindow(MainWindow)
        self.DockDataTreeSubWindow.setData(__data__)
        self.menuView.addAction(self.DockDataTreeSubWindow.toggleViewAction())
        
        self.DockDataTreeSubWindow.currentValueChanged.connect( self.changedCurrentTreeItem )


        #self.customerList.currentTextChanged.connect(self.insertCustomer)
        #self.paragraphsList.currentTextChanged.connect(self.addParagraph)

    def delVariableData(self, index):
        child = index.text()
        parent = index.parent().text()
	parent = parent.lower()
        if parent in VariablesData.__globals__.keys():
            if child in VariablesData.__globals__[parent].keys():
                del VariablesData.__globals__[parent][child]
                __data__[parent] = VariablesData.__globals__[parent]
                self.DockDataTreeSubWindow.setData(__data__)
                self.statusbar.showMessage( 'Succeed to delete the item.')
                return True
        self.statusbar.showMessage( 'Failed to delete the item...')
        return False

    def executeBench(self, MainWindow, index):

        def pseudofunction(self, index):
            key = index.text()
            value = __data__['bench'][key]
            environ = dict(__data__['model'].iteritems())
            environ[key] = value
            interpy = QInterpy(locals=environ)
            instances = {}
            for subwindow in VariablesData.__globals__['param'].values():
                instances.update( dict(subwindow.iteritems()) )
            cmd = [ "import sys, traceback",
                    "try:",
                    "    kwargs = %s"           	% str(instances),
                    "    obj = %s"           		% key,
                    "    result = %s(**kwargs)"           	% key,
                    "    obj.__dict__.update(result.__dict__)",
                    "except BaseException, e:",
                    "    type, value, tb = sys.exc_info()",
                    "    for name, noline, funcname, message in traceback.extract_tb(tb):",
                    "        if name=='<script>':",
                    "            print 'Error at line %d: %s' % (noline, str(e))",
                    "        print '%s :: Error at line %d: %s' % (name, noline, str(e))",
                    "    print ",
                  ]
            interpy.runsource( "\n".join(cmd), filename=key )

            def finished(self, interpy, index):
                key = index.text()
                obj = interpy.locals.get('obj', None)
                if obj:
                    __data__['bench'][key]  = obj
                    self.DockDataTreeSubWindow.setData(__data__)
                else:
                    raise Exception('Error: an error occurs during the bench simulation.')
                    
            interpy.finished.connect(lambda:finished(self, interpy, index))
            interpy.start()

        if index.parent().text() == "Bench":
            pseudofunction(self, index)

        elif index.text() == "Bench":
            for child in index.childs():
                if child.ischeck():
                    pseudofunction(self, child)


        # update plots
        opened = []
        for subwindow in self.mdiArea.subWindowList():
            if isinstance(subwindow, QMdiPlotSubWindow) and subwindow.isClosed() == False:
                opened.append(subwindow.name())
                

        for indx in self.DockDataTreeSubWindow.getPlotIndexes():
            if indx.text() in opened:
                self.tracePlot(MainWindow, indx)



    def tracePlot(self, MainWindow, index):
        def pseudofunction(self, index):
            key = index.text()
            value = __data__['plot'][key]
            environ = dict({name:bench for name, bench in __data__['bench'].iteritems()})
            environ[key] = value
            interpy = QInterpy(locals=environ)
            cmd = [ "try:",
                    "    plt['currentname'] = '%s'"           	% key,
                    "    plt['%s'] = {}"           		% key,
                    "    plt['%s']['xlabel'] = ''"           	% key,
                    "    plt['%s']['ylabel'] = ''"           	% key,
                    "    plt['%s']['xunit'] = ''"           	% key,
                    "    plt['%s']['yunit'] = ''"           	% key,
                    "    plt['%s']['items'] = []"           	% key,
                    "    %s()"          			% key,
                    "except:",
                    "    print 'Warning: plot is empty'",
                    "    print"
                  ]
            interpy.runsource( '\n'.join(cmd), filename=key )


            def finished(self, interpy, index):
                key = index.text()
                plt = dict(**interpy.locals['plt'][key])
                find = False
                for subwindow in self.mdiArea.subWindowList():
                    if isinstance(subwindow, QMdiPlotSubWindow) and subwindow.name() == key:
                        subwindow.update( plt )
                        find = True
                        if subwindow.isClosed() == True:
                            subwindow.reopen( plt )
                        break
                if find == False:
                    plotWindow = QMdiPlotSubWindow(self.mdiArea, plt)
                    plotWindow.setName( key )


            interpy.finished.connect(lambda:finished(self, interpy, index))
            interpy.start()

        
        if index.parent().text()  == "Plot":
            pseudofunction(self, index)
        else:
            self.statusbar.showMessage( 'Plot Opening Failed because no plot is selected...')
            
    def autoexecute(self, MainWindow):
        autoexecute = self.AutoExecuteAct.isChecked()
        if autoexecute:
            index = self.DockDataTreeSubWindow.getBenchIndex()
            self.executeBench(MainWindow, index)
    
    #---------------------------------------------------------------------------
    def setExistingDirectory(self, MainWindow):    
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(MainWindow,
                "Select A Root Folder For The Project",
                '', options)
        return directory

    def newScript(self, MainWindow):
        QMdiScriptSubWindow(self.mdiArea)

    def newParameterBox(self, MainWindow):
        QMdiParameterBoxSubWindow(self.mdiArea)
        
    def newCursorBoxWindow(self, MainWindow):
        index = self.DockDataTreeSubWindow.getSelectedRow()
        if index.parent().text() == 'Param':
            for subwindow in __data__['param'].values():
                if os.path.split(subwindow.filename())[-1] == index.text():
                    data = subwindow.data()
                    cursorBox = QMdiCursorSubWindow(self.mdiArea, data)
                    cursorBox.valueChanged.connect( subwindow.setValue )
                    

    def loadFile(self, MainWindow):

        filename = QtGui.QFileDialog.getOpenFileName(None,
            'Open a Script/Data File', self.project_path, "Python Files & Parameter Files (*.py *.dat);;")

        if filename is None: 
            self.statusbar.showMessage( 'No file has been selected...')
            return False

        try:
            filename = str(filename)

            if filename[-4:] == '.dat':
                subwindow = QMdiParameterBoxSubWindow(self.mdiArea)
                subwindow.setFilename(filename)
                d = table(filename).read()
                for i, (key, values) in enumerate(d.iteritems()):
                    subwindow.setRow(i, key, values)
                
            elif filename[-3:] == '.py':
                with open(filename) as f:
                    subwindow = QMdiScriptSubWindow(self.mdiArea)
                    subwindow.setText(f.read())
                    subwindow.setFilename(filename)


                   
        except IOError:
            self.statusbar.showMessage( 'Failed to load the file. The file cannot be read...')
            return False
        except Exception, e:
            self.statusbar.showMessage( str(e) )
            return False
        else:
            sys.path.append( os.path.dirname(filename) )
            self.statusbar.showMessage( "Successfully Loaded " + filename ) 
            return True

    def saveFile(self, MainWindow):
        subwindow = self.mdiArea.activeSubWindow()
        try:
            if subwindow == None:
                raise Exception( 'No active Window is selected to save...' )
            filename = subwindow.filename()

            if isinstance(subwindow, QMdiParameterBoxSubWindow):
                t = table(filename)
                for row in subwindow.data():
                    t[row[0]] = row[1:]
                t.write()
            elif isinstance(subwindow, QMdiScriptSubWindow):
                with open(filename, 'w') as g:
                    string = subwindow.text()
                    g.write(string)

        except IOError:
            self.statusbar.showMessage( 'Failed to save the file + %s...' % filename)
            return False
        except Exception, e:
            self.statusbar.showMessage( str(e) )
            return False
        else:
            self.statusbar.showMessage( "Successfully Saved " + filename ) 
            return True

    def saveAsFile(self, MainWindow):
        subwindow = self.mdiArea.activeSubWindow()
        try:
            if subwindow == None:
                raise Exception( 'No active Window is selected to save...' )

            filename = QtGui.QFileDialog.getSaveFileName(None,
                'Save a Script/Data File', self.project_path, "Python Files & Parameter Files (*.py *.dat);;")

            if not filename:
                Exception( "Failed to save to a file...")

            subwindow.setFilename(filename)

            if isinstance(subwindow, QMdiParameterBoxSubWindow):
                t = table(filename)
                for row in subwindow.data():
                    t[row[0]] = row[1:]
                t.write()
            elif isinstance(subwindow, QMdiScriptSubWindow):
                with open(filename, 'w') as g:
                    string = subwindow.text()
                    g.write(string)

        except IOError:
            self.statusbar.showMessage( 'Failed to save the file + %s...' % filename)
            return False
        except Exception, e:
            self.statusbar.showMessage( str(e) )
            return False
        else:
            self.statusbar.showMessage( "Successfully Saved " + filename ) 
            return True



    def changedFocusSlot(self, MainWindow, subwindow):
        self.DelVariableData.setEnabled(False)
        if isinstance(subwindow, QMdiParameterBoxSubWindow):
            self.ExecuteBenchAct.setEnabled(False)
            self.TracePlotAct.setEnabled(False)
            self.OpenCursorBoxAct.setEnabled(False)
            self.AttachToProjectAct.setEnabled(True)
            self.AddRowAct.setEnabled(True)
            self.DelRowAct.setEnabled(True)
        elif isinstance(subwindow, QMdiScriptSubWindow):
            self.AttachToProjectAct.setEnabled(True)
            self.ExecuteBenchAct.setEnabled(False)
            self.TracePlotAct.setEnabled(False)
            self.OpenCursorBoxAct.setEnabled(False)
            self.AddRowAct.setEnabled(False)
            self.DelRowAct.setEnabled(False)
      
    def changedCurrentTreeItem(self, index):
        if index.text() in ('Bench',) or index.parent().text() in ('Bench',):
            self.ExecuteBenchAct.setEnabled(True)
            self.TracePlotAct.setEnabled(False)
            self.OpenCursorBoxAct.setEnabled(False)
        if index.text() in ('Param',) or index.parent().text() in ('Param',):
            self.OpenCursorBoxAct.setEnabled(True)
            self.ExecuteBenchAct.setEnabled(False)
            self.TracePlotAct.setEnabled(False)
        if index.text() in ('Plot',) or index.parent().text() in ('Plot',):
            self.TracePlotAct.setEnabled(True)
            self.OpenCursorBoxAct.setEnabled(False)
            self.ExecuteBenchAct.setEnabled(False)
        if index.text() in ('Model',) or index.parent().text() in ('Model',):
            self.ExecuteBenchAct.setEnabled(False)
            self.TracePlotAct.setEnabled(False)
            self.OpenCursorBoxAct.setEnabled(False)
        self.DelVariableData.setEnabled(True)



    def attachToProject(self, MainWindow):

        subwindow = self.mdiArea.activeSubWindow()

        if isinstance(subwindow, QMdiScriptSubWindow):
            script = str(subwindow.text())
            # run the script and extract the add-on data
            environ = { 'setenv':VariablesData.setenv }
            obj1 = Interpy(locals=environ)
            obj1.runsource(script, filename='<script>', symbol="exec")
            if obj1.stderr.strip()<>"":
                msgerror = obj1.stderr.strip()
                self.warningMessage(MainWindow, message='The file failed to attach to the Project. \n %s'%msgerror)
		return
            if obj1.stdout.strip()<>"":
                print obj1.stdout.strip()
            __data__['model'] = VariablesData.__globals__['model']
            __data__['bench'] = VariablesData.__globals__['bench']
            __data__['plot'] = VariablesData.__globals__['plot']
            self.DockDataTreeSubWindow.setData(__data__)
            self.statusbar.showMessage( 'File attached successfully into the data hierarchy.') 

        elif isinstance(subwindow, QMdiParameterBoxSubWindow):
            key = os.path.split(subwindow.filename())[-1]
            VariablesData.__globals__['param'][key] = subwindow
            __data__['param'] = VariablesData.__globals__['param']
            self.DockDataTreeSubWindow.setData(__data__)
            subwindow.itemChanged.connect( lambda: self.autoexecute(MainWindow)  )
            self.statusbar.showMessage( 'Parameter File attached successfully into the data hierarchy.')




    def aboutMessageBox(self, MainWindow):
        msg = __doc__
        QtGui.QMessageBox.about(MainWindow, "About the QTModel", msg.strip())
        





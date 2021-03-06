from PyQt4 import QtCore, QtGui
import os

class Index(object):
    def __init__(self, obj, model):
        self.obj = obj
        self.model = model
    def text(self):
        variant = self.model.data(self.obj)
        return str(variant.toString())
    def childs(self):
        i=0
        for i in xrange(100):
            s = Index(self.obj.child(i,0), self.model)
            if s.text() == "": break
            yield s
    def parent(self):
        return Index(self.obj.parent(), self.model)
    def ischeck(self):
        obj = self.model.itemFromIndex(self.obj)
        if obj==None: return False
        i = obj.checkState()
        return [False, False, True][i]



class DomModel(QtGui.QStandardItemModel):

    def __init__(self, parent=None):
        super(DomModel, self).__init__(parent)


    def createData(self, data, selected=[]):
        
        
        QStandardItem = QtGui.QStandardItem

        font_root = QtGui.QFont()
        font_root.setItalic(True)
       
        # model
        row = QStandardItem('Model')
        row.setFont(font_root)
        row.setEditable(False)
        for key, value in data['model'].iteritems():
            item = QStandardItem(key)
            item.setEditable(False)
            row.appendRow(item)
        self.appendRow(row)
        
        # bench
        row = QStandardItem('Bench')
        row.setFont(font_root)
        row.setEditable(False)
        for key, value in data['bench'].iteritems():
            item = QStandardItem(key)
            item.setCheckable(True)
            #item.setCheckState(QtCore.Qt.Checked)
            if key in selected:
                item.setCheckState(2)
            item.setEditable(False)
            
            row.appendRow(item)
            obj = value
            
            keys = []
            for key, value in obj.__dict__.iteritems():
                if key[:2] == '__' and key[-2:] == '__' : continue
                if 'func' in key : continue

                if not key in keys:
                    keys.append( key )

            for key in dir(obj):
                value = getattr(obj, key)
                if key[:2] == '__' and key[-2:] == '__' : continue
                if 'func' in key : continue
                if not key in keys:
                    keys.append( key )

            for key in keys:
                item2 = QStandardItem(key)
                item2.setEditable(False)
                item.appendRow(item2)
        self.appendRow(row)
        
        # plot
        row = QStandardItem('Plot')
        row.setFont(font_root)
        row.setEditable(False)
        for key, value in data['plot'].iteritems():
            item = QStandardItem(key)
            item.setCheckable(False)
            item.setEditable(False)
            row.appendRow(item)
        self.appendRow(row)

        # param
        row = QStandardItem('Param')
        row.setFont(font_root)
        row.setEditable(False)
        for i, value in enumerate(data['param'].values()):
            key = value.filename()
            key = os.path.split(key)[1]
            item = QStandardItem(key)
            item.setEditable(False)
            row.appendRow(item)
        self.appendRow(row)

        # Optim
        row = QStandardItem('Optim')
        row.setFont(font_root)
        row.setEditable(False)
        self.appendRow(row) 

    def getPlotIndexes(self):
        index = Index(self.index(2, 0), self)
        for child in index.childs():
            yield child
        
    def getSelectedBench(self):
        index = Index(self.index(1, 0), self)
        for child in index.childs():
            if child.ischeck():
                yield child.text()

    


class DataTree(QtGui.QTreeView):

    currentValueChanged = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, model=DomModel):
        super(DataTree, self).__init__(parent)

        self.setAnimated(True)


        self.model = model()
        self.setModel(self.model)
        self.doubleClicked.connect(self.on_treeview_doubleClicked)
        self.expandToDepth(0)
        self.header().hide()

    def setData(self, data):
    
        if hasattr(self, 'model'):
            s = list(self.model.getSelectedBench())
            self.model = DomModel()
            self.model.createData(data, selected=s)
        else:
            self.model = DomModel()
            self.model.createData(data)
        self.setModel(self.model)
        self.expandToDepth(0)
        
        def pseudofunction(selected, deselected):
            index = Index(self.currentIndex(), self.model)
            self.currentValueChanged.emit(index)
        self.selectionModel().currentChanged.connect(pseudofunction)
        
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeview_doubleClicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        # path or filename selected
        data = self.model.data(indexItem)
        print str(data.toString())
        
        try:
            indexParentItem = self.model.index(index.parent().row(), 0, index.parent().parent())        
            data = self.model.data(indexParentItem)
            print str(data.toString())
        except:
            pass
        

        #child = self.currentIndex()
        #parent = child.parent()
        #child = self.model.data(child)
        #parent = self.model.data(parent)
        #self.valueChanged.emit(parent, child)
        
        
 
    #def getSelectedRow(self):
    #    try:
    #        child = self.currentIndex()
    #        parent = child.parent()
    #        child = self.model.data(child).toString()
    #        parent = self.model.data(parent).toString()
    #        return str(parent), str(child)
    #    except:
    #        return None, None
        
 
    def getSelectedRow(self):
        index = Index(self.currentIndex(), self.model)
        return index
 
    _sizehint = None
    def setSizeHint(self, width, height):
        self._sizehint = QtCore.QSize(width, height)

    def sizeHint(self):
        if self._sizehint is not None:
            return self._sizehint
        return super(MyWidget, self).sizeHint()

    def getPlotIndexes(self):
        return self.model.getPlotIndexes()
        
    def getBenchIndex(self):
        return Index(self.model.index(1, 0), self.model)
    
 
    

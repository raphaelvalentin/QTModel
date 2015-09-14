from PyQt4 import QtCore, QtGui
import os


class DomItem(object):

    #children = []

    def __init__(self, group=None, parent=None):
        self.parent = parent
        self.group = group
        self.children = []

    def data(self, column):
        d = self.group[column]
        if isinstance(d, QtGui.QStandardItem):

            return d
        return d

    def appendChild(self, group):
        self.children.append(DomItem(group, self))

    def child(self, row):
        c = self.children[row]
        return c

    def childrenCount(self):
        return len(self.children)

    def hasChildren(self):
        if len(self.children) > 0 :
            return True
        return False

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0

    def columnCount(self):
        return len(self.group)




class DomModel(QtCore.QAbstractItemModel):

    def __init__(self, parent=None):
        super(DomModel, self).__init__(parent)
        self.root = DomItem(["Name"])

    def createData(self, data):
    
  
        self.root.appendChild(['model'])
        self.root.appendChild(['bench'])
        self.root.appendChild(['plot'])
        self.root.appendChild(['param'])
        
        for i, key in enumerate(data['model']):
            self.root.child(0).appendChild([key])
            
        for i, key in enumerate(data['bench']):
            self.root.child(1).appendChild([key])
            item = data['bench'][key]['__obj__']
            
            keys = []
            for key, value in item.__dict__.iteritems():
                if key[:2] == '__' and key[-2:] == '__' : continue
                if not key in keys:
                    keys.append( key )

            for key in dir(item):
                value = getattr(item, key)
                if key[:2] == '__' and key[-2:] == '__' : continue
                if not key in keys:
                    keys.append( key )

            for key in keys:
                self.root.child(1).child(i).appendChild([key])
                
        for i, key in enumerate(data['plot']):
            self.root.child(2).appendChild([key])
            
        for i, value in enumerate(data['parameter']):
            key = value.filename()
            key = os.path.split(key)[1]
            self.root.child(3).appendChild([key])
                
    def columnCount(self, index=QtCore.QModelIndex()):
        if index.isValid():
            return index.internalPointer().columnCount()
        else:
            return self.root.columnCount()

    def rowCount(self, index=QtCore.QModelIndex()):
        #if index.row() > 0:
        #    return 0
        if index.isValid():
            item = index.internalPointer()
        else:
            item = self.root
        return item.childrenCount()

    def index(self, row, column, index=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, index):
            return QtCore.QModelIndex()
        if not index.isValid():
            item = self.root
        else:
            item = index.internalPointer()

        child = item.child(row)
        if child:
            return self.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        item = index.internalPointer()
        if not item:
            return QtCore.QModelIndex()

        parent = item.parent
        if parent == self.root:
            return QtCore.QModelIndex()
        else:
            return self.createIndex(parent.row(), 0, parent)

    def hasChildren(self, index):
        if not index.isValid():
            item = self.root
        else:
            item = index.internalPointer()
        return item.hasChildren()

    def data(self, index, role=QtCore.Qt.DisplayRole):
       if index.isValid() and role == QtCore.Qt.DisplayRole:
            return index.internalPointer().data(index.column())
       elif not index.isValid():
            return self.root.getData()

    def headerData(self, section, orientation, role):
       if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
           return self.root.data(section)

class DataTree(QtGui.QTreeView):

    currentValueChanged = QtCore.pyqtSignal(tuple)

    def __init__(self, parent=None, model=DomModel):
        super(DataTree, self).__init__(parent)
        self.model = model()
        self.setModel(self.model)
        self.doubleClicked.connect(self.on_treeview_doubleClicked)
        
        self.expandToDepth(0)
        



    def setData(self, data):
        self.model = DomModel()
        self.model.createData(data)
        self.setModel(self.model)
        self.expandToDepth(0)
        
        
        def pseudofunction(selected, deselected):
            indexItem = self.model.index(selected.row(), 0, selected.parent())
            child = self.model.data(indexItem)
            try:
                indexParentItem = self.model.index(selected.parent().row(), 0, selected.parent().parent())                    
                parent = self.model.data(indexParentItem)
                self.currentValueChanged.emit((parent, child))
            except:
                self.currentValueChanged.emit((child,))
        self.selectionModel().currentChanged.connect(pseudofunction)
        
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeview_doubleClicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        # path or filename selected
        data = self.model.data(indexItem)
        print data
        
        try:
            indexParentItem = self.model.index(index.parent().row(), 0, index.parent().parent())        
            data = self.model.data(indexParentItem)
            print data
        except:
            pass
        

        #child = self.currentIndex()
        #parent = child.parent()
        #child = self.model.data(child)
        #parent = self.model.data(parent)
        #self.valueChanged.emit(parent, child)
        
        
 
    def getSelectedRow(self):
        try:
            child = self.currentIndex()
            parent = child.parent()
            child = self.model.data(child)
            parent = self.model.data(parent)
            return parent, child
        except:
            return None, None
 
    _sizehint = None
    def setSizeHint(self, width, height):
        self._sizehint = QtCore.QSize(width, height)

    def sizeHint(self):
        if self._sizehint is not None:
            return self._sizehint
        return super(MyWidget, self).sizeHint()
 
    

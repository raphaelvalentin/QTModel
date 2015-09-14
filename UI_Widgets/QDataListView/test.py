import sys
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import *

class MyClass:
     def slot(self, selected, deselected):
         print len(selected), "items selected"
         print len(deselected), "items deselected"


if __name__ == "__main__":

     app = QApplication(sys.argv)
     model = QStandardItemModel()
     for i in range(10):
        item = QStandardItem("Item %i" % i)
        if i<4:
            item.setCheckable(True)

        model.appendRow([item])

     listView = QListView()
     listView.setModel(model)
     listView.show()

     myobj = MyClass()
     #QObject.connect(listView.selectionModel(),
     #    SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
     #    myobj.slot)

     sys.exit(app.exec_())

'''
Created on Dec 4, 2010

@author: falmarri
'''

from PyQt4 import QtCore


class PositionItem(object):
    def __init__(self, data, parent=None):
        
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column, role=None):
        '''
        if role is None:
            return self.itemData[column]
            '''
        if role == QtCore.Qt.DisplayRole:
            return str(self.itemData[column])
        elif role == QtCore.Qt.UserRole:
            return self.itemData[column]
        
        
        
        return QtCore.QVariant()

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0



class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self,rootItem,parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.rootItem = rootItem

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()
    
    def data(self, index, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        
        item = index.internalPointer()
        if role == QtCore.Qt.UserRole:
            return item.data(index.column(), role)
        return item.data(index.column(), role)


    def addPosition(self, position):
        pass
    
    
    def save(self, path=None):
        pass

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    
    
if __name__== '__main__':
    
    
    
    load('quotes.json')
    
    from PyQt4 import QtGui
    import sys
    app = QtGui.QApplication(sys.argv)

    model = TreeModel(build_model())

    view = QtGui.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.show()
    sys.exit(app.exec_())

    
    
    c1 = PositionItem('Test')
        
        
    #build_from_save()
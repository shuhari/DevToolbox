import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from strings import _
from utils.data_parser import parse_title


class CategoryItem:
    def __init__(self, data, parent=None):
        self._parent = parent
        self._children = []
        self._row = parent.childCount() if parent else 0
        self.load_data(data)

    def load_data(self, data):
        if isinstance(data, dict):
            self._title = parse_title(data['title'])
            self._widgetClass = data.get('widget', None)
            self._icon = data.get('icon', None)
        if isinstance(data, str):
            self._title = data
            self._widgetClass = None
            self._icon = None

    def __str__(self):
        message = 'CategoryItem(title={0}, widget={1})'
        return message.format(self._title,
                              self._widgetClass)

    def row(self):
        return self._row

    def parent(self):
        return self._parent

    def appendChild(self, data):
        child = CategoryItem(data, self)
        self._children.append(child)
        return child

    def childCount(self):
        return len(self._children)

    def childAt(self, row):
        if 0 <= row < len(self._children):
            return self._children[row]
        return None

    def title(self):
        return self._title

    def widgetClass(self):
        return self._widgetClass

    def icon(self):
        return self._icon


class CategoryModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(CategoryModel, self).__init__(parent)

    def index(self, row, column, parent: QModelIndex):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parentItem = parent.internalPointer() if parent.isValid() else self._root
        childItem = parentItem.childAt(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem is self._root:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent: QModelIndex):
        if parent.column() > 0:
            return 0
        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self._root
        result = parentItem.childCount()
        return result

    def columnCount(self, parent: QModelIndex):
        return 1

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return QVariant()
        item = index.internalPointer()
        if index.column() == 0:
            if role == Qt.DisplayRole:
                return item.title()
            elif role == Qt.DecorationRole:
                if item.icon():
                    return QIcon(item.icon())
        return QVariant()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root.title()
        return QVariant()

    def load_json(self, filepath):
        with open(filepath, 'r') as f:
            content = json.load(f)
            self._root = CategoryItem('root')
            for item_data in content:
                self.add_node(self._root, item_data)

    def add_node(self, parent, item_data):
        child = parent.appendChild(item_data)
        if 'children' in item_data:
            for child_data in item_data['children']:
                self.add_node(child, child_data)
        return child


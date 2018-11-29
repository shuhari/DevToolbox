from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from category_model import CategoryItem, CategoryModel


class CategoryWidget(QWidget):

    categorySelected = pyqtSignal(CategoryItem)

    def __init__(self, parent=None):
        super(CategoryWidget, self).__init__(parent)

        categories_path = QApplication.instance().resolve_path('data/categories.json')
        model = CategoryModel()
        model.load_json(categories_path)

        self.tree = QTreeView()
        self.tree.header().hide()
        self.tree.setModel(model)
        self.tree.clicked.connect(self.on_tree_clicked)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tree)
        self.setLayout(layout)

    @pyqtSlot(QModelIndex)
    def on_tree_clicked(self, index: QModelIndex):
        item = index.internalPointer()
        if item:
            self.categorySelected.emit(item)


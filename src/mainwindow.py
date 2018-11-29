from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import qrc_resources
from strings import _
from category_model import CategoryItem
from category_widget import CategoryWidget
from central_widget import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowIcon(QIcon(":/images/app.png"))
        self.setWindowTitle(_('app_title'))
        self.setMinimumSize(800, 600)
        self.setFont(QFont('MS Shell Dlg 2', 10))

        self.setupUi()

    def setupUi(self):
        self.category_widget = CategoryWidget()
        self.category_widget.categorySelected.connect(self.on_categorySelected)

        left_dock = QDockWidget(_('categories'), self)
        left_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        left_dock.setMinimumWidth(100)
        left_dock.setWidget(self.category_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, left_dock)

        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)

    @pyqtSlot(CategoryItem)
    def on_categorySelected(self, item):
        widgetCls = item.widgetClass()
        if widgetCls:
            self.central_widget.show_widget(widgetCls)

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


DEFAULT_MAX_COUNT = 1000


class LogListWidget(QListView):
    def __init__(self, parent=None):
        super(LogListWidget, self).__init__(parent)
        model = QStandardItemModel(self)
        self.setModel(model)
        self.setMaxCount(DEFAULT_MAX_COUNT)

    def setMaxCount(self, count):
        self._maxCount = count

    def info(self, msg):
        self.add_log(':/images/info.png', msg)

    def warn(self, msg):
        self.add_log(':/images/warn.png', msg)

    def error(self, msg):
        self.add_log(':/images/error.png', msg)

    def add_log(self, icon_path, msg):
        model = self.model()
        if model.rowCount() >= self._maxCount:
            model.removeRow(0)
        item = QStandardItem(QIcon(icon_path), msg)
        model.appendRow(item)
        index = model.index(model.rowCount(), 0)
        self.scrollTo(index)

    def clear(self):
        self.model().clear()

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import qrc_resources
from strings import _


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowIcon(QIcon(":/images/app.png"))
        self.setWindowTitle(_('app_title'))

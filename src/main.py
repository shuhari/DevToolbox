import sys

from app import App
from mainwindow import MainWindow
import qrc_resources


if __name__ == '__main__':
    app = App()

    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())

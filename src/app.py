import os
import sys

from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication


class App(QApplication):
    def __init__(self):
        super(App, self).__init__(sys.argv)
        self.load_translators()

    def load_translators(self):
        dir_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'translations'))
        translator = QTranslator(self)
        translator.load("strings_zh.qm", dir_name)
        self.installTranslator(translator)

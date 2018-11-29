import os
import sys

from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication


class App(QApplication):
    def __init__(self):
        super(App, self).__init__(sys.argv)
        self.load_translators()

    def resolve_path(self, suffix):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), suffix))

    def load_translators(self):
        translator = QTranslator(self)
        translator.load("strings_zh.qm", self.resolve_path('translations'))
        self.installTranslator(translator)

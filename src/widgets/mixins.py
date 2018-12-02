from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TextColorMixin:
    """Set normal/text color"""
    def __init__(self):
        self.normal_palette = QPalette()
        self.normal_palette.setColor(QPalette.Text, Qt.blue)

        self.error_palette = QPalette()
        self.error_palette.setColor(QPalette.Text, Qt.red)

    def setColoredText(self, widget, text, success):
        if isinstance(widget, QLineEdit):
            widget.setText(text)
        elif isinstance(widget, QTextEdit):
            widget.setPlainText(text)
        if success:
            widget.setPalette(self.normal_palette)
        else:
            widget.setPalette(self.error_palette)

import lorem
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from strings import _


class RandomTextWidget(QWidget):
    def __init__(self, parent=None):
        super(RandomTextWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        btn_sentence = QPushButton(_('sentence'))
        btn_paragraph = QPushButton(_('paragraph'))
        btn_text = QPushButton(_('text'))

        self.sentence_edit = QLineEdit()
        self.sentence_edit.setReadOnly(True)

        self.paragraph_edit = QTextEdit()
        self.paragraph_edit.setReadOnly(True)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        form = QFormLayout()
        form.addRow(btn_sentence, self.sentence_edit)
        form.addRow(btn_paragraph, self.paragraph_edit)
        form.addRow(btn_text, self.text_edit)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addStretch()
        self.setLayout(vbox)

        btn_sentence.clicked.connect(self.on_sentence)
        btn_paragraph.clicked.connect(self.on_paragraph)
        btn_text.clicked.connect(self.on_text)

    @pyqtSlot()
    def on_sentence(self):
        sentence = lorem.sentence()
        self.sentence_edit.setText(sentence)

    @pyqtSlot()
    def on_paragraph(self):
        paragraph = lorem.paragraph()
        self.paragraph_edit.setText(paragraph)

    @pyqtSlot()
    def on_text(self):
        text = lorem.text()
        self.text_edit.setText(text)

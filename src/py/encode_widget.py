from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils.encoders import EncodeMethod


class EncodeWidget(QWidget):
    def __init__(self, parent=None):
        super(EncodeWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.method_base64 = self.create_method_radio('BASE64', EncodeMethod.base64)
        self.method_md5 = self.create_method_radio('MD5', EncodeMethod.md5)
        self.method_url = self.create_method_radio('URL', EncodeMethod.url)
        self.method_html = self.create_method_radio('HTML', EncodeMethod.html)

        btnEncode = QPushButton('&Encode')
        btnDecode = QPushButton('&Decode')

        self.src_edit = QTextEdit()
        self.src_edit.setFixedHeight(300)

        self.dest_edit = QTextEdit()
        self.dest_edit.setFixedHeight(300)

        method_box = QHBoxLayout()
        method_box.addWidget(QLabel('Method:'))
        method_box.addWidget(self.method_base64)
        method_box.addWidget(self.method_md5)
        method_box.addWidget(self.method_url)
        method_box.addWidget(self.method_html)
        method_box.addStretch()

        btnBox = QVBoxLayout()
        btnBox.addStretch()
        btnBox.addWidget(btnEncode)
        btnBox.addWidget(btnDecode)
        btnBox.addStretch()

        center_box = QHBoxLayout()
        center_box.addWidget(self.src_edit, 1)
        center_box.addLayout(btnBox)
        center_box.addWidget(self.dest_edit, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(method_box)
        vbox.addLayout(center_box)
        vbox.addStretch()
        self.setLayout(vbox)

        btnEncode.clicked.connect(self.on_encode)
        btnDecode.clicked.connect(self.on_decode)

    def create_method_radio(self, text, value):
        radio = QRadioButton(text)
        radio.setProperty('value', value)
        return radio

    def on_initialized(self):
        self.method_base64.setChecked(True)

    def get_method(self):
        if self.method_md5.isChecked():
            return EncodeMethod.md5
        elif self.method_url.isChecked():
            return EncodeMethod.url
        elif self.method_html.isChecked():
            return EncodeMethod.html
        return EncodeMethod.base64

    @pyqtSlot()
    def on_encode(self):
        pass

    @pyqtSlot()
    def on_decode(self):
        pass

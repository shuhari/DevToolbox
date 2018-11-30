import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils import hashers
from strings import _


class FileHashThread(QThread):

    finished = pyqtSignal(list)

    def __init__(self, file_path, methods, parent=None):
        super(FileHashThread, self).__init__(parent)
        self.file_path = file_path
        self.methods = methods

    def run(self):
        lines = []
        try:
            lines.append(_('check_file_hash_header').format(self.file_path))
            self.get_hash_result(lines, 'md5', hashers.md5)
            self.get_hash_result(lines, 'sha1', hashers.sha1)
            self.get_hash_result(lines, 'sha256', hashers.sha256)
        except Exception as e:
            lines.append(str(e))
        self.finished.emit(lines)

    def get_hash_result(self, lines, method, fn):
        if method in self.methods:
            hash_result = fn(self.file_path)
            lines.append('{0}: {1}'.format(method.upper(), hash_result))


class FileHashWidget(QWidget):
    def __init__(self, parent=None):
        super(FileHashWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        file_label = QLabel(_('file'))
        self.file_edit = QLineEdit()
        self.file_edit.setReadOnly(True)
        self.browse_btn = QPushButton('...')

        method_label = QLabel(_('method'))
        self.method_md5 = QCheckBox('MD5')
        self.method_md5.setChecked(True)
        self.method_sha1 = QCheckBox('SHA1')
        self.method_sha1.setChecked(True)
        self.method_sha256 = QCheckBox('SHA256')
        self.method_sha256.setChecked(True)
        self.check_btn = QPushButton(_('check'))

        file_box = QHBoxLayout()
        file_box.addWidget(self.file_edit, 1)
        file_box.addWidget(self.browse_btn)

        result_label = QLabel(_('result'))
        self.result_edit = QTextBrowser()
        self.result_edit.setReadOnly(True)
        self.result_edit.setFixedHeight(300)

        method_box = QHBoxLayout()
        method_box.addWidget(self.method_md5)
        method_box.addWidget(self.method_sha1)
        method_box.addWidget(self.method_sha256)
        method_box.addStretch()
        method_box.addWidget(self.check_btn)

        form = QFormLayout()
        form.addRow(file_label, file_box)
        form.addRow(method_label, method_box)
        form.addRow(result_label, self.result_edit)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addStretch()
        self.setLayout(vbox)

        self.browse_btn.clicked.connect(self.on_browse)
        self.check_btn.clicked.connect(self.on_check)

    @pyqtSlot()
    def on_browse(self):
        filePath, filter = QFileDialog.getOpenFileName(self,
                                                       'Select file',
                                                       '',
                                                       'All files (*.*)')
        if filePath:
            self.file_edit.setText(filePath)

    def on_thread_running(self, running):
        enabled = not running
        self.browse_btn.setEnabled(enabled)
        self.check_btn.setEnabled(enabled)

    @pyqtSlot()
    def on_check(self):
        try:
            file_path = self.file_edit.text().strip()
            if not os.path.exists(file_path):
                raise ValueError(_('msg_file_not_exist').format(file_path))
            methods = []
            if self.method_md5.isChecked():
                methods.append('md5')
            if self.method_sha1.isChecked():
                methods.append('sha1')
            if self.method_sha256.isChecked():
                methods.append('sha256')
            self.on_thread_running(True)
            self.result_edit.setText(_('msg_checking_file_hash'))
            thread = FileHashThread(file_path, methods, self)
            thread.finished.connect(self.on_thread_finished)
            thread.start()
        except Exception as e:
            self.result_edit.setText(str(e))

    @pyqtSlot(list)
    def on_thread_finished(self, lines):
        self.result_edit.setText('\n'.join(lines))
        self.on_thread_running(False)

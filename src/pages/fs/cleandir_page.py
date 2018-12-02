import os
import glob

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils.fileutils import enum_directory, is_empty_dir, delete_dir, delete_file
from widgets.loglist import LogListWidget
from strings import _


class CleanThread(QThread):

    notify = pyqtSignal(bool, str)

    def __init__(self, dir_name, deletable_files, parent=None):
        super(CleanThread, self).__init__(parent)
        self.dir_name = dir_name
        deletable_patterns = deletable_files.split(';')
        deletable_patterns = [x.strip() for x in deletable_patterns
                              if x]
        self.deletable_patterns = deletable_patterns
        self.dir_found = 0
        self.delete_success = 0
        self.delete_failed = 0

    def run(self):
        try:
            self.process_dir(self.dir_name)
            msg = _('msg_clean_summary').format(self.dir_found, self.delete_success, self.delete_failed)
            self.notify.emit(True, msg)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.notify.emit(False, str(e))

    def process_dir(self, dir_name):
        print('process dir:', dir_name)
        for sub_dir in enum_directory(dir_name, dirs=True):
            self.process_dir(sub_dir)
        self.delete_files(dir_name)
        if is_empty_dir(dir_name):
            self.dir_found += 1
            try:
                delete_dir(dir_name)
                self.delete_success += 1
                self.notify.emit(True, _('msg_delete_dir_success').format(dir_name))
            except Exception as e:
                self.delete_failed += 1
                self.notify.emit(False, _('msg_delete_dir_failed').format(dir_name, e))

    def delete_files(self, dir_name):
        for file_path in enum_directory(dir_name, files=True):
            if self.is_deletable(file_path):
                try:
                    delete_file(file_path)
                except Exception as e:
                    self.notify.emit(False, _('msg_delete_file_failed').format(file_path, e))

    def is_deletable(self, file_path):
        _, file_name = os.path.split(file_path)
        for pattern in self.deletable_patterns:
            if glob.fnmatch.fnmatch(file_name, pattern):
                return True
        return False


class CleanDirPage(QWidget):
    def __init__(self, parent=None):
        super(CleanDirPage, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.log_list = LogListWidget()
        self.dir_edit = QLineEdit()
        self.dir_edit.setReadOnly(True)
        self.browse_btn = QPushButton('...')
        self.deletable_edit = QLineEdit()
        self.clean_btn = QPushButton(_('clean'))

        dir_box = QHBoxLayout()
        dir_box.addWidget(self.dir_edit, 1)
        dir_box.addWidget(self.browse_btn)

        clean_box = QHBoxLayout()
        clean_box.addWidget(self.deletable_edit)
        clean_box.addWidget(self.clean_btn)

        form = QFormLayout()
        form.addRow(QLabel(_('directory')), dir_box)
        form.addRow(QLabel(_('deletable_files')), clean_box)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self.log_list, 1)
        self.setLayout(vbox)

        self.browse_btn.clicked.connect(self.on_browse)
        self.clean_btn.clicked.connect(self.on_clean)

    def on_initialized(self):
        self.log_list.clear()

    @pyqtSlot()
    def on_browse(self):
        initial_dir = self.dir_edit.text().strip()
        dir_name = QFileDialog.getExistingDirectory(self,
                                                    _('select_dir_title'),
                                                    initial_dir)
        if dir_name:
            self.dir_edit.setText(dir_name)

    @pyqtSlot()
    def on_clean(self):
        try:
            dir_name = self.dir_edit.text().strip()
            if not dir_name or not os.path.isdir(dir_name):
                raise ValueError(_('msg_directory_not_exist'.format(dir_name)))
            deletable_files = self.deletable_edit.text().strip()
            thread = CleanThread(dir_name, deletable_files, self)
            thread.notify.connect(self.on_thread_notify)
            thread.finished.connect(self.on_thread_finished)
            self.on_thread_running(True)
            thread.start()
        except Exception as e:
            self.log_list.error(str(e))

    @pyqtSlot()
    def on_thread_finished(self):
        self.on_thread_running(False)
        self.log_list.info(_('msg_thread_finished'))

    @pyqtSlot(bool, str)
    def on_thread_notify(self, success, msg):
        if success:
            self.log_list.info(msg)
        else:
            self.log_list.error(msg)

    def on_thread_running(self, running):
        enabled = not running
        self.browse_btn.setEnabled(enabled)
        self.clean_btn.setEnabled(enabled)

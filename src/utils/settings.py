import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class CleanDirSettings:
    def __init__(self):
        self.group = 'clean_dir'
        self.dirname = None
        self.deletable_files = None

    def load(self, settings: QSettings):
        settings.beginGroup(self.group)
        self.dirname = settings.value('dir_name')
        self.deletable_files = settings.value('deletable_files')
        settings.endGroup()

    def save(self, settings):
        settings.beginGroup(self.group)
        settings.setValue('dir_name', self.dirname)
        settings.setValue('deletable_files', self.deletable_files)
        settings.endGroup()


class AppSettings(QSettings):
    def __init__(self, parent):
        assert isinstance(parent, QApplication)
        config_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)
        file_path = os.path.join(config_path, 'settings.ini')
        super(AppSettings, self).__init__(file_path, QSettings.IniFormat, parent)
        self.cleandir = CleanDirSettings()

    def load(self):
        self.cleandir.load(self)

    def save(self):
        self.cleandir.save(self)
        self.sync()

from PyQt5.QtWidgets import QWidget, QApplication


class BasePage(QWidget):
    def app_settings(self):
        return QApplication.instance().settings

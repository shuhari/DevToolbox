from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import *


DATETIME_PYTHON_FORMAT = '%Y-%m-%d %H:%M:%S'
DATETIME_QT_FORMAT = 'yyyy-MM-dd HH:mm:ss'


class DateTimeWidget(QWidget):
    def __init__(self, parent=None):
        super(DateTimeWidget, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        lblftime = QLabel('strftime')
        lblptime = QLabel('strptime')

        self.ftime_value = QDateTimeEdit()
        self.ftime_value.setCalendarPopup(True)
        self.ftime_value.setDisplayFormat(DATETIME_QT_FORMAT)

        self.ftime_format = QLineEdit()
        self.ftime_result = QLineEdit()

        self.ptime_value = QLineEdit()
        self.ptime_format = QLineEdit()
        self.ptime_result = QLineEdit()
        self.ptime_result.setReadOnly(True)

        self.comment = QTextBrowser()

        form1 = QFormLayout()
        form1.addRow(QLabel("Value"), self.ftime_value)
        form1.addRow(QLabel("Format"), self.ftime_format)
        form1.addRow(QLabel("Result"), self.ftime_result)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(lblftime)
        vbox1.addLayout(form1)

        form2 = QFormLayout()
        form2.addRow(QLabel("Value"), self.ptime_value)
        form2.addRow(QLabel("Format"), self.ptime_format)
        form2.addRow(QLabel("Result"), self.ptime_result)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(lblptime)
        vbox2.addLayout(form2)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox1, 1)
        hbox.addLayout(vbox2, 1)

        layout = QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(self.comment, 1)

        self.setLayout(layout)

        self.ftime_value.dateTimeChanged.connect(self.on_ftime_sourceChanged)
        self.ftime_format.textChanged.connect(self.on_ftime_sourceChanged)
        self.ptime_value.textChanged.connect(self.on_ptime_sourceChanged)
        self.ptime_format.textChanged.connect(self.on_ptime_sourceChanged)

    def on_initialized(self):
        self.normal_palette = QPalette()
        self.normal_palette.setColor(QPalette.Text, Qt.blue)

        self.error_palette = QPalette()
        self.error_palette.setColor(QPalette.Text, Qt.red)

        now = datetime.now()
        self.ftime_value.setDateTime(now)
        self.ptime_value.setText(now.strftime(DATETIME_PYTHON_FORMAT))
        self.ptime_format.setText(DATETIME_PYTHON_FORMAT)

        self.on_ftime_sourceChanged()
        self.on_ptime_sourceChanged()

    def on_activated(self):
        html_path = QApplication.instance().resolve_path('data/datetime_comment.html')
        html = open(html_path, 'r', encoding='utf8').read()
        self.comment.setHtml(html)

    @pyqtSlot()
    def on_ftime_sourceChanged(self):
        try:
            value = self.ftime_value.dateTime().toPyDateTime()
            format = self.ftime_format.text().strip()
            result = value.strftime(format)
            self.ftime_result.setText(result)
            self.ftime_result.setPalette(self.normal_palette)
        except Exception as e:
            self.ftime_result.setText(str(e))
            self.ftime_result.setPalette(self.error_palette)

    @pyqtSlot()
    def on_ptime_sourceChanged(self):
        try:
            value = self.ptime_value.text().strip()
            format = self.ptime_format.text().strip()
            result = datetime.strptime(value, format)
            self.ptime_result.setText(result.strftime(DATETIME_PYTHON_FORMAT))
            self.ptime_result.setPalette(self.normal_palette)
        except Exception as e:
            self.ptime_result.setText(str(e))
            self.ptime_result.setPalette(self.error_palette)


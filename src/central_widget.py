import importlib

from PyQt5.QtWidgets import *


class CentralWidget(QStackedWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

    def show_widget(self, widget_cls):
        try:
            widget = self.find_widget(widget_cls)
            if not widget:
                widget = self.create_widget(widget_cls)
            if self.currentWidget():
                self.currentWidget().hide()
            widget.show()
            self.setCurrentWidget(widget)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def find_widget(self, widget_cls):
        for i in range(self.count()):
            widget = self.widget(i)
            if str(widget.property('uid')) == widget_cls:
                return widget
        return None

    def create_widget(self, widget_cls):
        module_name, class_name = widget_cls.split(':')
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        widget = cls()
        widget.setProperty('uid', widget_cls)
        widget.setVisible(False)
        self.addWidget(widget)
        return widget

"""
Use stacked widget to manage multiple widgets.
each widget has a 'uid' property corresponding to selected category.
a widget may have optional methods:

- on_initialized: called once when the widget it first time created
- on_activated: called each time a widget become active page
- on_deactivated: called each time a widget become deactive page
"""
from PyQt5.QtWidgets import *

from utils.data_parser import create_page


class CentralWidget(QStackedWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

    def show_widget(self, widget_cls):
        try:
            widget = self.find_widget(widget_cls)
            if not widget:
                widget = self.create_page(widget_cls)
            if self.currentWidget():
                self.activate_page(self.currentWidget(), False)
                self.currentWidget().hide()
            widget.show()
            self.setCurrentWidget(widget)
            self.activate_page(widget, True)
            widget.setFocus()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def find_widget(self, widget_cls):
        for i in range(self.count()):
            widget = self.widget(i)
            if str(widget.property('uid')) == widget_cls:
                return widget
        return None

    def create_page(self, page_cls):
        page = create_page(page_cls)
        page.setProperty('uid', page_cls)
        page.setVisible(False)
        self.addWidget(page)
        self.init_page(page)
        return page

    def call_page_method(self, page, method_name):
        method = getattr(page, method_name, None)
        if method:
            method()

    def init_page(self, widget):
        self.call_page_method(widget, 'on_initialized')

    def activate_page(self, widget, active):
        method_name = 'on_activated' if active else 'on_deactivated'
        self.call_page_method(widget, method_name)

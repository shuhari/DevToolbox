"""
Use _() to translate keyed text to native language.
example:

from strings import _
btn.text = _('text_key')
"""
from PyQt5.QtCore import QObject


class Strings(QObject):

    def app_title(self):
        return self.tr("Developer's Toolbox")

    def categories(self):
        return self.tr("Categories")

    def datetime(self):
        return self.tr('Date/Time')

    def random_text(self):
        return self.tr('Random text')

    def value(self):
        return self.tr('Value')

    def format(self):
        return self.tr('Format')

    def result(self):
        return self.tr('Result')

    def sentence(self):
        return self.tr('Sentence')

    def paragraph(self):
        return self.tr('Paragraph')

    def text(self):
        return self.tr('Text')


class StringReader:
    _strings = None

    def __call__(self, *args, **kwargs):
        if len(args) != 1:
            raise ValueError('StringReader.__call__ expect 1 args, get {}'.format(len(args)))
        if self._strings is None:
            self._strings = Strings()
        return getattr(self._strings, args[0])()


_ = StringReader()  # since load string is used often, give it a short name

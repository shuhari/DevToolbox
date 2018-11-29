from PyQt5.QtCore import QObject, QCoreApplication


class Strings(QObject):

    def app_title(self):
        return self.tr("Developer's Toolbox")

    def categories(self):
        return self.tr("Categories")


class StringReader:
    _strings = None

    def __call__(self, *args, **kwargs):
        if len(args) != 1:
            raise ValueError('StringReader.__call__ expect 1 args, get {}'.format(len(args)))
        if self._strings is None:
            self._strings = Strings()
        return getattr(self._strings, args[0])()


_ = StringReader()  # since load string is used often, give it a short name

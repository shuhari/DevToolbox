import importlib

from strings import _


def parse_title(title):
    if title.startswith(':'):
        key = title[1:]
        return _(key)
    else:
        return title


def create_page(page_cls):
    module_name, class_name = page_cls.split(':')
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    widget = cls()
    return widget

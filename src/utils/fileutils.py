import os

from win32.lib import win32con
from win32 import win32api


def enum_directory(dir_name, dirs=False, files=False):
    """Return enumerator of sub directories or files"""
    for file_name in os.listdir(dir_name):
        full_path = os.path.abspath(os.path.join(dir_name, file_name))
        if dirs and os.path.isdir(full_path):
            yield full_path
        if files and os.path.isfile(full_path):
            yield full_path


def is_empty_dir(dir_name):
    subdirs = enum_directory(dir_name, dirs=True)
    files = enum_directory(dir_name, files=True)
    if len(list(subdirs)) == 0 and len(list(files)) == 0:
        return True
    return False


def clear_attributes(file_name, to_remove=win32con.FILE_ATTRIBUTE_SYSTEM |
                                          win32con.FILE_ATTRIBUTE_HIDDEN |
                                          win32con.FILE_ATTRIBUTE_READONLY):
    attrs = win32api.GetFileAttributes(file_name)
    new_attrs = attrs & ~to_remove
    if new_attrs != attrs:
        win32api.SetFileAttributes(file_name, new_attrs)


def delete_dir(dir_path):
    clear_attributes(dir_path)
    os.rmdir(dir_path)


def delete_file(file_path):
    clear_attributes(file_path)
    os.unlink(file_path)

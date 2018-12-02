from unittest import TestCase

from utils.fileutils import is_empty_dir, clear_attributes


class FileUtilsTest(TestCase):
    def test_is_empty_dir(self):
        self.assertFalse(is_empty_dir(r'c:\Windows'))

    def test_clear_attributes(self):
        clear_attributes(__file__)


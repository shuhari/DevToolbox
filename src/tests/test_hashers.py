from unittest import TestCase

from utils import hashers


class HasherTest(TestCase):
    def test_md5(self):
        result = hashers.md5(__file__)
        self.assertIsInstance(result, str)

    def test_sha1(self):
        result = hashers.sha1(__file__)
        self.assertIsInstance(result, str)

    def test_sha256(self):
        result = hashers.sha256(__file__)
        self.assertIsInstance(result, str)

from unittest import TestCase

from utils.encoders import EncodeMethod, create_encoder


class EncoderTest(TestCase):
    def assert_encode_decode(self, method, value, can_decode=True):
        encoder = create_encoder(method)

        encoded = encoder.encode(value)
        self.assertIsInstance(encoded, str)

        if can_decode:
            decoded = encoder.decode(encoded)
            self.assertIsInstance(decoded, str)
            self.assertEqual(decoded, value)

    def test_base64(self):
        self.assert_encode_decode(EncodeMethod.base64, '1234')

    def test_md5(self):
        self.assert_encode_decode(EncodeMethod.md5, '1234', can_decode=False)

    def test_url(self):
        self.assert_encode_decode(EncodeMethod.url, 'a url+str?=b')

    def test_html(self):
        self.assert_encode_decode(EncodeMethod.html, '<a test></a>')

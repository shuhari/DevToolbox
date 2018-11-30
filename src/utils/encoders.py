from base64 import b64encode, b64decode
import hashlib
import urllib.parse
import html


class EncodeMethod:
    base64 = 1
    md5 = 2
    url = 3
    html = 4


class Encoder:
    def __init__(self):
        self.encoding = 'utf8'

    def encode(self, value):
        raise NotImplementedError("Encoder '{0}' not support encode".format(self.__class__.__name__))

    def decode(self, value):
        raise NotImplementedError("Encoder '{0}' not support decode".format(self.__class__.__name__))

    def to_bytes(self, value):
        if isinstance(value, bytes):
            return value
        elif isinstance(value, str):
            return value.encode(self.encoding)
        raise ValueError('Unknown value to bytes: ' + value)

    def to_str(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, bytes):
            return value.decode(self.encoding)
        raise ValueError('Unknown value to str: ' + value)


class Base64Encoder(Encoder):
    def encode(self, value):
        return self.to_str(b64encode(self.to_bytes(value)))

    def decode(self, value):
        return self.to_str(b64decode(value))


class Md5Encoder(Encoder):
    def encode(self, value):
        return hashlib.md5(self.to_bytes(value)).hexdigest()


class UrlEncoder(Encoder):
    def encode(self, value):
        return urllib.parse.quote(value, errors=None)

    def decode(self, value):
        return urllib.parse.unquote(value, errors=None)


class HtmlEncoder(Encoder):
    def encode(self, value):
        return html.escape(value)

    def decode(self, value):
        return html.unescape(value)


def create_encoder(method):
    encoders = {
        EncodeMethod.base64: Base64Encoder(),
        EncodeMethod.md5: Md5Encoder(),
        EncodeMethod.url: UrlEncoder(),
        EncodeMethod.html: HtmlEncoder(),
    }
    assert method in encoders, 'Encode method {0} not registerd'.format(method)
    return encoders[method]

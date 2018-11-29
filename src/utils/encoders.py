class EncodeMethod:
    base64 = 1
    md5 = 2
    url = 3
    html = 4


class Encoder:
    def encode(self, value):
        raise NotImplementedError()

    def decode(self, value):
        raise NotImplementedError()


class Base64Encoder(Encoder):
    pass


class Md5Encoder(Encoder):
    pass


class UrlEncoder(Encoder):
    pass


class HtmlEncoder(Encoder):
    pass


def create_encoder(method):
    encoders = {
        EncodeMethod.base64: Base64Encoder(),
        EncodeMethod.md5: Md5Encoder(),
        EncodeMethod.url: UrlEncoder(),
        EncodeMethod.html: HtmlEncoder(),
    }
    assert method in encoders, 'Encode method {0} not registerd'.format(method)
    return encoders[method]

import hashlib


def calc_hash(hash, file_path):
    BUFSIZE = 4096
    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(BUFSIZE)
            if not buf:
                break
            hash.update(buf)
    return hash.hexdigest()


def md5(file_path: str):
    return calc_hash(hashlib.md5(), file_path)


def sha1(file_path: str):
    return calc_hash(hashlib.sha1(), file_path)


def sha256(file_path: str):
    return calc_hash(hashlib.sha256(), file_path)

import base64

from hypothesis.strategies import binary


def keys():
    return binary(min_size=16).map(base64.b64encode)


def assert_valid(key):
    assert len(key) >= 24
    assert base64.b64decode(key)

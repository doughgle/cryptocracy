import base64

from hypothesis.strategies import binary


def keys():
    return binary(min_size=16).map(base64.b64encode)


def assert_valid(key):
    try:
        assert len(key) >= 24
        assert base64.b64decode(key)
    except AssertionError as e:
        e.message = "invalid key: '%s'. valid example: IKUCwiMT5X1CruqyabR13Q==" % key
        raise e

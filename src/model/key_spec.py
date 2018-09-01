import base64
import unittest

from hypothesis import given
from hypothesis.strategies import binary

keys = binary(min_size=16).map(base64.b64encode)


class TestDataTypeSpecs(unittest.TestCase):
    @given(keys)
    def test_key_spec(self, key):
        assert_valid(key)


def assert_valid(key):
    assert len(key) >= 24
    assert base64.b64decode(key)

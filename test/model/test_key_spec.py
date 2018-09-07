import unittest
from hypothesis import given

from src.model.key_spec import keys, assert_valid


class TestDataTypeSpecs(unittest.TestCase):
    @given(keys())
    def test_key_spec(self, key):
        assert_valid(key)

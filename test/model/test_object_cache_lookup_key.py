import unittest

from hypothesis import given

from cryptocracy.model.object_cache_lookup_key import lookup_keys, assert_valid


class TestObjectCacheLookupKeySpecs(unittest.TestCase):
    @given(lookup_keys())
    def test_key_spec(self, key):
        assert_valid(key)

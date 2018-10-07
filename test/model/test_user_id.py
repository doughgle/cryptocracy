import unittest
from hypothesis import given
from hypothesis.strategies import emails

from src.model.user_id import assert_valid


class TestDataTypeSpecs(unittest.TestCase):
    @given(emails())
    def test_user_id(self, user_id):
        assert_valid(user_id)

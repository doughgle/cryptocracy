import unittest

from hypothesis import given

from cryptocracy.model.policy_expression_spec import policy_expressions, assert_valid


class TestPolicyExpressionSpec(unittest.TestCase):

    @given(policy_expressions())
    def test_policy_expression_spec(self, policy_expression):
        assert_valid(policy_expression)

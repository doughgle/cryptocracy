import unittest

from hypothesis import given
from hypothesis.strategies import text, composite, sampled_from, characters, one_of, integers


def policy_expressions():
    return one_of(attributes(), inequalities(), policy_expression())


@composite
def policy_expression(draw):
    left = draw(policy_expressions())
    right = draw(policy_expressions())
    gate = draw(gates())
    return u'(' + u' '.join((left, gate, right)) + u')'


def attributes():
    return text(min_size=1, alphabet=characters(whitelist_categories='L', max_codepoint=0x7e))


@composite
def inequalities(draw):
    attr = draw(attributes())
    oper = draw(inequality_operators())
    numb = draw(integers())
    return u' '.join((attr, oper, str(numb)))


def inequality_operators():
    return sampled_from((u'<', u'>', u'<=', u'>='))


def gates():
    return sampled_from((u'or', u'and'))


class TestPolicyExpressionSpec(unittest.TestCase):

    @given(policy_expressions())
    def test_policy_expression_spec(self, policy_expression):
        expr = policy_expression
        print expr
        assert expr # not empty
        assert expr.count(u'(') == expr.count(u')')

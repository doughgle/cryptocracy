import re

from src.model.exceptions import InvalidInput

pattern_str = '''[a-zA-Z0-9!#$%&'*+-/=^_`{|}~]{1,64}@[a-zA-Z0-9!#$%&'*+-/=^_`{|}~]+\.(com|net||org||biz|info)'''
pattern = re.compile(pattern_str)


def assert_valid(user_id):
    try:
        assert re.match(pattern, user_id) is not None
    except (AssertionError, TypeError) as e:
        e.message = "invalid user_id: '%s'. valid example: a@a.com" % user_id
        raise InvalidInput(e)

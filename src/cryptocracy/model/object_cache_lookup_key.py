import hashlib

from hypothesis.strategies import composite, emails, text


@composite
def lookup_keys(draw):
    user_id = draw(emails())
    url = draw(text(min_size=6))
    return make_lookup_key(url, user_id)


def make_lookup_key(url, user_id):
    key_str = u'_'.join((user_id, url))
    bytes = key_str.encode('UTF-8')
    return hashlib.sha256(bytes).hexdigest()


def assert_valid(key):
    assert len(key) > 10
    int(key, base=16)

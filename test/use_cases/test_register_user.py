import os
import tempfile
import unittest

import pytest
from flask import Response, Flask
from hypothesis import given
from hypothesis._strategies import emails

from key_authority import ka_service
from key_authority.ka_service import create_app
from src.model.abe_scheme import CharmHybridABE
from src.model.exceptions import InvalidInput
from src.model.key_spec import assert_valid as assert_valid_key
from src.model.result import RESULT
from src.model.user_id import assert_valid as assert_valid_user_id
from src.use_cases.register_user import RegisterUserUseCase, RegisterUserRequest


@given(user_id=emails())
def test_valid_request_returns_valid_response(http_test_client, user_id):
    abe_scheme = CharmHybridABE()
    params, msk = abe_scheme.setup()
    pku, sku = abe_scheme.user_keygen(params)
    register_user = RegisterUserUseCase(http_test_client)
    request = RegisterUserRequest(user_id, pku)

    response = register_user.run(request)

    assert user_id == response['user_id']
    assert_valid_key(response['user_public_key'])
    assert_valid_user_id(response['user_id'])


def test_invalid_user_id_raises_exception():
    with pytest.raises(InvalidInput):
        RegisterUserRequest("alice", b"aW52YWxpZHB1YmxpY2tleQo=")


def test_invalid_user_public_key_raises_exception():
    with pytest.raises(InvalidInput):
        RegisterUserRequest("alice@a.com", b"invalid key")


def test_returns_failure_result_when_already_registered(http_test_client):
    abe_scheme = CharmHybridABE()
    params, msk = abe_scheme.setup()
    pku, sku = abe_scheme.user_keygen(params)
    register_user = RegisterUserUseCase(http_test_client)
    request = RegisterUserRequest("alice@a.com", pku)

    response = register_user.run(request)
    response = register_user.run(request)

    assert RESULT.FAILURE == response['result']
    assert response['error'] is not None


@pytest.fixture
def http_test_client():
    Flask.response_class = JsonPatchedResponse
    app = create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        ka_service.db.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


class JsonPatchedResponse(Response):
    """
    Adapts `json` property to `json()` method so that the interface matches the
    `requests` library.
    Used to replace the response object in :attr:`~flask.Flask.response_class`.
    """
    def json(self):
        return self.get_json()


if __name__ == '__main__':
    unittest.main()

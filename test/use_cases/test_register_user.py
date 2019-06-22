import unittest

import pytest
from hypothesis import given
from hypothesis._strategies import emails

from cryptocracy.boundaries.key_authority_service import KeyAuthorityService
from cryptocracy.model.abe_scheme import CharmHybridABE
from cryptocracy.model.exceptions import InvalidInput
from cryptocracy.model.key_spec import assert_valid as assert_valid_key
from cryptocracy.model.result import RESULT
from cryptocracy.model.user_id import assert_valid as assert_valid_user_id
from cryptocracy.use_cases.register_user import RegisterUserUseCase, RegisterUserRequest


@given(user_id=emails())
def test_valid_request_returns_valid_response(http_test_client, user_id):
    abe_scheme = CharmHybridABE()
    params, msk = abe_scheme.setup()
    pku, sku = abe_scheme.user_keygen(params)
    ka_service = KeyAuthorityService(http_test_client)
    register_user = RegisterUserUseCase(ka_service)
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
    ka_service = KeyAuthorityService(http_test_client)
    register_user = RegisterUserUseCase(ka_service)
    request = RegisterUserRequest("alice@a.com", pku)

    response = register_user.run(request)
    response = register_user.run(request)

    assert RESULT.FAILURE == response['result']
    assert response['error'] is not None


if __name__ == '__main__':
    unittest.main()

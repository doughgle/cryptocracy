import unittest

from src.boundaries.key_authority_service import KeyAuthorityService
from src.boundaries.proxy_key_store import ProxyKeyStore
from src.model.abe_scheme import NullCipher
from src.model.result import RESULT
from src.use_cases.add_user import AddUserRequest
from src.use_cases.add_user import AddUserUseCase
from src.use_cases.register_user import RegisterUserUseCase, RegisterUserRequest


def test_add_user_stores_proxy_key(http_test_client):

    ka_service = KeyAuthorityService(http_test_client)
    # pre-register alice's public key
    register = RegisterUserUseCase(ka_service)
    user_id = "alice@a.org"
    pku_b64 = b'''eJw1kLEOwjAMRH8l6pwhLk3s8CsIVYDY2ApICPHv3Dnu4jrn88ul32ldb4/Ltq3rdEzT9fO8b1NOUN+Xx
    +vu6qmWnKrlZDUnmXHQjkZQTNlAdkuDMOfUbZwbDOqGBQJ3xVhgW9AsOtTG3oHCAlWhdC6WJRQpwXN2jUtFDhw1lp0spUfI
    0Gpo3K7klRrhNZ7UYTYnoVgZ6UT4Ih1B+ArG5e0OU6xZHwZ+VYLZYjCc+Bm6p6uA62FMbP+HJeAe2EHMITNHMq7xVMQ2Of/
    +vDpS9Q=='''
    response = register.run(RegisterUserRequest(user_id, pku_b64))
    assert RESULT.SUCCESS == response['result']

    # pre-register AWS's public key
    user_id = "cryptocracy@amazonaws.com"
    pku_b64 = b'''eJw9UUEOgzAM+0rFuYe6NG3YV6YJsYkbN7ZJ07S/L2kCB0JlJ7bTfod5fi/ba53n4RKulGIgjqG1GHiKA
    WheGIKWGCZFE2sZBZFDJUEVAA4KnSctp4i2I2cneDSDSaXFlAWj3gFT42x/Es8iRJ2sofubTHJWkMqO6gKAJqumAWSj1akL
    w2cVaD1j9mFFSObaaKqsGh6w52cngHTuRr5R0bCqjeINLR15yHRqdVqDaUC/FNglnh9uMci7PLZl3/u7DPfPc92H3x/NUVKO'''
    response = register.run(RegisterUserRequest(user_id, pku_b64))
    assert RESULT.SUCCESS == response['result']

    proxy_key_store = ProxyKeyStore()
    abe_scheme = FakeProxyKeyABE()
    add_user = AddUserUseCase(ka_service, abe_scheme, proxy_key_store)
    attributes = '["female", "age=25"]'
    request = AddUserRequest(user_id, attributes)

    response = add_user.run(request)

    assert {"result": RESULT.SUCCESS, "user_id": user_id} == response
    assert "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f" == proxy_key_store.get(user_id)


class FakeProxyKeyABE(NullCipher):

    def proxy_keygen(self, cloud_server_public_key, user_public_key, attribute_list):
        return "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f"


if __name__ == '__main__':
    unittest.main()

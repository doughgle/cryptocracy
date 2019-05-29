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
    msk, params = abe_scheme.setup()
    add_user = AddUserUseCase(ka_service, abe_scheme, proxy_key_store)
    attributes = '["female", "age=25"]'
    request = AddUserRequest(msk, params, user_id, attributes)

    response = add_user.run(request)

    assert {"result": RESULT.SUCCESS, "user_id": user_id} == response
    assert "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f" == proxy_key_store.get(user_id)


class FakeProxyKeyABE(NullCipher):

    def setup(self):
        return ('eJyVjzEOwjAMRa8SZe6QlMROuQpCUYoqMXRAakFCVe/Ot03ZGeI4z47/9+bHaW3' \
               '+7DZf621uy1IrXn58r9PiOwf6avNzUnpJpXMZh3BijJ0rSNIJMAkghADCeJWAm1FlqUh/QJZBi5CQJUQJvWGts' \
               '+DIv5p20TFlgHK87nDV5sf9b9cFg3JvIgXjk26hEtDPKi0J2YK2E0JmM03Z/tNgTLuJD/v9sQN9veog+N0/HK1NuQ==',
                'eJyVVcuO2zAM/BUj5xwkWRLl/kpRGGkRZA85FNi2QLHYf69mOPT6uD3EkSWKjxly/HZ5XL4sb5d9//G8vb7u+3y7fP/76'
                '/56uS5z98/t+fvO3a91uy5tXJfNrsto16X3uZ7vOef5KPPR5u6Yp9u07HOdEx/puti0tTotyrQo'
                '/p8zH3a6zO0y7budfNe56HyZXsbm0W2F6+5pMBhPp5nNuw2/6j7aGpnkzfNjCJjR'
                '/ZgvI3tMJitj2eCIgeDHeDzdGH4zW2sOSE5HHUlheS8rmntgyOFF5FRjAaO8'
                '+lUTWjlN711AMj2s87f3ScujfJYzeARnAIl4kwATWsyXmQPR0YJLZMYbzt9c1VXlmq9h67jODRtBJtDr4hFwtoCLIMKEp'
                '+bVNDsHdGhrZJUFLqOAOBKOXfQh2sEieXROD4s0PBqsSB/eu1gYq4gluk5kUkS4rKuORhFTHgQo0kdxhwJu9d5s6l56dkabGEW5'
                '/Dlx9/3x2G/Pny+3TxOYnUBPqOqBpJvwReQ6VGBbT8NQNQje2D2aFMkBHXraUjSoOz'
                '+skD3xi7qbimOBrLSLGZ9YpYE7Fn1O0FIggpkZVZRYJFFcGZAIQ1hcYS4kC+FBDRUniWQL1Ql5gGusSVBMGUeq'
                '+IxWCwo1edshKiYZCN7QQSN6sZUAdbiTmBbXOEkN+wZ00eshB45ddKZmPVqtHDKIfSTeNGAokwkAihogs'
                '+UQAwrxMbMhxA6bkHZ9qSIhq1OsygsQAzjAtKWTukGQEd1icJJayautjjziOXybQ8fyKNsmcGO6YQ5HWyTFAqRq3jvDT9E3mpSX'
                '//0qeU9U5xIlR1hOaFVoDgqxqCFII8g9f4iIomYmubrwjLpXz1qZg58c9SsPymXX9OVQ0ypJAuxDQtq1Z0Uxx5HgMSUpBDJ0S0Nb4m'
                'shiWrxrdl0dWizjxMlbLyPtxSXxha9I4mmAmd97kIl/FtcpWz6LL3/Aw49lIc=')

    def proxy_keygen(self, msk, params, cloud_server_public_key, user_public_key, attribute_list):
        return "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f"


if __name__ == '__main__':
    unittest.main()

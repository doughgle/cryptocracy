import os
import unittest

from src.model import key_spec
from src.model.abe_scheme import CharmHybridABE
from src.model.result import RESULT
from src.use_cases.generate_key_pair import GenerateKeyPairUseCase, GenerateKeyPairRequest


class GenerateKeyPairTest(unittest.TestCase):

    def tearDown(self):
        os.remove("./user.pub")
        os.remove("./user.key")

    def test_generate_key_pair(self):
        abe_scheme = CharmHybridABE()
        params, msk = abe_scheme.setup()
        generate_key_pair = GenerateKeyPairUseCase(abe_scheme)
        response = generate_key_pair.run(
            GenerateKeyPairRequest(params, "./user.pub", "./user.key"))
        self.assertEqual(RESULT.SUCCESS, response["result"])
        key_spec.assert_valid(response["public_key"])
        key_spec.assert_valid(response["secret_key"])


if __name__ == '__main__':
    unittest.main()

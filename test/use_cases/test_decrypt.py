import os
import unittest

from cryptocracy.model.abe_scheme import CharmHybridABE
from cryptocracy.model.result import RESULT, STATUS
from cryptocracy.use_cases.decrypt_file import DecryptRequest, DecryptResponse, DecryptUseCase


class DecryptTest(unittest.TestCase):

    def test_authorized_decrypt_succeeds(self):
        abe_scheme = CharmHybridABE()
        alice_sku = b'eJw1i0kKgDAMRa8Suu6iCR29ikip4s5dVRDx7v46LH54+cOpcp6WUmvOqiM1HutclSa4e1m2+XF7GzU5yDtNEQqC30NGE3PAMY0MbJZGwh9FrFJCU761/CmDLKbJvIlHK4ATFjG8GXMLeLhuxz8jcA=='
        partial_ct_b64 = b'eJyVVMtSGzEQ/BXXnn2QtDt6UMWBkAdgCCFACBWnXGa9BmIICTYkhPK/Rz0zMs4xh93VSqNRT/e0nqvWVRu952pyfdnNF3lYzRf3G9SaiXddmkZPU0qpaa2fmPF0Eloy1Pix997Y2I7JXUzcNI7rNkV3Ucc22XFr2qrfq27nlyXd87Da/TTMf8Pq8Pyt/37p9l49tgc0mF3bnydXs1+bm8O8ZVgdHL5+gziHn639dxgbjLevf1x19yfd74Wk+VY/3A/O3s937+727Hk6O/pAs6c0G0w/xjdHM/Nnsv/ZT0/3B8eT05x6CTzjmxWenYOt7dHxzparlnnhkQnY5vdo1N6M5/PRCKEXT4tujq2j0eP45qHj2S9k+z2K/V7IT8QT8n+dvxmotU1+uRxhTcIrz4VG/8ghIM943+81EbM5MHJwXoqUV3JYworNEzjIOmQ1AVNxPbXPU8FKduxIQEGSLvKJtNqdw5taAFvnZJCMPNYCmZHN1nhZRWaGGpDSaWFNPqPhshii1WWSioAkOF3gTIgPSVHHWkBL0ag3R/ioxQtxlhQQThFAWh42IDk2BC/ZrK0FqdRBUqXwBOwxKQ1B+QYWVq0pLJNm91oUBqCd6yGlCxFAjjMpaIpawQXNz0+SANYLqQAsmMKgV5W8/niSPFILqeoxKhuM0KDEoHVQGaDVmEv7InJQ6lScVZakQPnFlEi8K0UEbRorRfCR6GnEoq+B19uvcEo3WnT3t/9rFL/Gn0CxKi+VNkNIoz5i2LzaCHvgKdTCovdrLcWtJJ3DRbPWjbqxqOdX59SqEq1I8nIID7AhrtlaDMS9abTp4E7WKKkz4BtMctsLrUZPAu8I4xvC/iPgWmNYWyRN5SYpHUgiPLawj7zKDaq4hUTxutwHpM71QhJysF9r6To2Ti29D4645bGbL40kwdJAwERqK2iG6phzo10R1e0r6aLK53256kiqYXGC3j1NySHUgkhUyAYpnoCdqS6bw9oNQPWLcZtVmxhJL15pyrXaaG+I1FaZA0r2b1jNOuEylN5H/WICpdOTOkJuQyd6ky9hSSbgj+XyL0yjd/0='
        decrypt = DecryptUseCase(abe_scheme)
        request = DecryptRequest(alice_sku, partial_ct_b64, 'plaintext')

        response = decrypt.run(request)

        exp_resp = DecryptResponse(RESULT.SUCCESS, STATUS.OK, output_file='plaintext')
        self.assertEqual(exp_resp, response)
        os.remove('plaintext')

    def test_unauthorized_decrypt_is_forbidden(self):
        abe_scheme = CharmHybridABE()
        params, msk = abe_scheme.setup()
        pku, sku = abe_scheme.user_keygen(params)
        partial_ct_b64 = b'eJx1VE1PFEEQ/SububqH7p7+JOGwAnENIlGUSFyzGWZmgYRVw66gEv67/epj5cJhJt1dVV1V79Xrx+a' \
                         b'+2Zs8NuNyO96tablc3ne3v8blsu6+BjudhDydWNNOJ6lMJznUz+Mg1Z+N+Dls6y/E3RG8q6d1prpbnNRFqqe5' \
                         b'+sXqkuvaFxjqL3hxTQg2WNQvIl09SE6sPkm2IpehoCLxqDTWlImqrWE' \
                         b'+S7U4sPpD7hAkQZTCKQM3hFutlNrKTSgkJCnTWLbkKKjExEkpj6ku2chFiCF/JANoqX6' \
                         b'+GoqUZk3hohmeLO60i1nsVBhKILtFgiI4JKowSEdFwxGAHdIGxx+wptTkldmYpA8igmqJ2qWiSHxyiY7ZQ1egFB' \
                         b'/4IjYlE7DIhKPAlYzg7rVUkBis3M5mJb3QDjaHPK0cY1ESV0mEFgEaoNBgMEtBohkVLzATVkHS0DglvoYGJjN2TDXItN' \
                         b'+mkyqB/rbbbEgCzeWf7bhpnurxwcv6oEtbZpjS0Uh6Rgi6iP/lIn2jXqK1cHhUXB3veXIECG4usFcwMvaRpw6jBVijSg' \
                         b'9tJSvgFKUSBNGp1aliYGganAyxZUAYeFUEoUm8e5lOkk12ghoapcGi6XQ6+SpvFm9hFmk86DVJTFWQt4IE0ooYWa8qQG' \
                         b'ou63OSZZIoG+vRyeOAqnnStLusoqFY7sg+S+7lMvgViaapNEoBIEFzJF7xAgP8AESZ1mI0Th5CEK/tqOb5VdC5Zi6sMF' \
                         b'BEsDgFRoijsdwJgq7Wq2hCGCV9Z33SVyXu0JfXNrgd2YnRDpIC95AVrZKU7bP3mzsS3fH8vSgQKKR3JJHu9gqGzfZub3' \
                         b'4yO1iezWeuqeb1Znf+uGhm794s6ramWDRvz7FcNK9ezw7/XnQn5nv/sJ4f9x+ODq/nD/v7iwZeBzc/r8e7T+PvLXufr8' \
                         b'vqx8lR9/n4/ZeP7uy6P43nF1fqfXJ6eAQ/94Tcw83VuNlq+rxyuevGYTXaNtowdL7tBzuk1vnB52EVetOvfOm6eGnL0N' \
                         b'mUhlRyZ0JcjdmEVNv9B57AcUk='
        decrypt = DecryptUseCase(abe_scheme)
        request = DecryptRequest(sku, partial_ct_b64)

        response = decrypt.run(request)
        exp_resp = DecryptResponse(RESULT.FAILURE, STATUS.FORBIDDEN, message='Invalid mac. Your data was tampered '
                                                                             'with or your key is wrong')
        self.assertEqual(exp_resp, response)

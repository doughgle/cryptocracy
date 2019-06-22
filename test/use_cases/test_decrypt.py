import os
import unittest

from cryptocracy.model.abe_scheme import CharmHybridABE
from cryptocracy.model.result import RESULT, STATUS
from cryptocracy.use_cases.decrypt_file import DecryptRequest, DecryptResponse, DecryptUseCase


class DecryptTest(unittest.TestCase):

    def test_authorized_decrypt_succeeds(self):
        abe_scheme = CharmHybridABE()
        alice_sku = b'eJw1TkEOgCAM+8rCmYNDQPErxhA13LihJsb4dzuCh7F27coeFeO15jPFqCaa7ajJoUaL3mvibtBkK8CUGWyQYhBj4POQg8gO4Fe60B5h4mcD4CXbSwq8ocYhwdn2CzMWPC+acNKe11LqSWq7j1TU+wG0siQO'
        partial_ct_b64 = b'eJx1VNtOGzEQ/ZVon/Mw47XXNhIPKFzV0pa2KpWaKlqCF6iCVCUBFRD/jue2Sh942Is945k5Z874pXls9iYvTVlsy/qefxeLx371UBaLuvoVcDoJaTpByPWFrq5CfeJ0Eqsl0deTgaxQVx39OKg/kbbpBXWVuupIzkl3U/Wj2IiUoHrEupHJkGyzPj7/F6gGSUETpbgbiWqqdfioh7kgSkoPQks7oAByNcVWnYFQkBkor3OSIdLJGi/Sfz0XCDdHcurFqPg0YtB8sdWfDFJfBrN4y4DeokDUonxSBjQpAaayqb6E6hnBMgFFcCh+Oe10hZEzuqyhicOkmJgJ7CSmb9WdichCO3czShFU1MidxEPBQZ5dMHDJSI/mj/qiqFReVIaT6YYCOj3LaNja7hRGx0MrYkreGOjkLPcCRxa9RpLkWTEiBMmM2CpdWdFRH6PRJqoAo4YduWMd/p5O6igsV/1mw6PQXD1ty6Z5rduz9+eEcHTd2CsUzLxK2k9CFkCp5b5RVuYYLL0Inkqick0hyZmMCDuL04CwYFR6LAGwETFxk1y6MKJFbRzNarJHtUMUsyhIZWlnUmhBRmrK2G0RAujkjMPnFDGoh10DnFqQoGEP0hoqnGUSpJY0dkM1x53meyToVUNWVpUbJ9/mFeSMV5apK8k0y2llCJLk4Rq0Zm6mlcriCyZ4Ip5vJNAbZOyb7GZ98WA6m3/RGqiC1SvqVRJ0aukC44ENY+akwEQXRriMRNbjLI5x+kHRdMJxNhkRchYeigM3wO3cuzxJGQyQF1qJDbmAk2xkbdP780EDsnQ8IfebGzJstuu9l3lz8PFkXpc1xbyZ3f29Levv5d+WtubNp6cveLF6Dog/L7vtn82HdXt7dLG/P2/I++yHeGVYppPD44fD51lcnx1/vbwNQ7oxr/PPh0fk517rsulXY+7T84PZ4tvpgaP967ubstmaqQff+XZohwzZOXBYfMHroS9XLlzjsMwlDm0fylD67HrfxwEwDqGDkAv0GCrcN1j1cec='
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

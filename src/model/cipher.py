from charm.core.engine.util import objectToBytes, bytesToObject
from charm.core.math.pairing import hashPair as sha2, GT
from charm.schemes.abenc.abenc_yllc15 import YLLC15
from charm.toolbox.pairinggroup import PairingGroup
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction


class NullCipher(object):

    def setup(self):
        raise NotImplementedError

    def user_keygen(self, pk, mk, object):
        raise NotImplementedError

    def proxy_keygen(self, cloud_server_public_key,
                     user_public_key,
                     user_id,
                     attribute_list):
        raise NotImplementedError

    def encrypt(self, plaintext, policy_expression):
        raise NotImplementedError

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, user_id, ciphertext):
        return "intermediate_value"

    def decrypt(self, user_private_key, intermediate_value):
        raise NotImplementedError


class CharmABE(object):

    def __init__(self):
        group = PairingGroup('SS512')
        self._cpabe = YLLC15(group)

    def setup(self):
        self._params, self._msk = self._cpabe.setup()
        return self._params, self._msk

    def user_keygen(self, user_id):
        return self._cpabe.ukgen(self._params, user_id)

    def proxy_keygen(self,
                     cloud_server_public_key,
                     user_public_key,
                     user_id,
                     attribute_list):
        return self._cpabe.proxy_keygen(self._params,
                                        self._msk,
                                        cloud_server_public_key,
                                        user_public_key,
                                        attribute_list)

    def encrypt(self, plaintext, policy_expression):
        symm_key = self._cpabe.group.random(GT)
        c1 = self._cpabe.encrypt(self._params, symm_key, policy_expression)
        cipher = AuthenticatedCryptoAbstraction(sha2(symm_key))
        c2 = cipher.encrypt(plaintext)
        ciphertext = {'c1': c1, 'c2': c2}
        return objectToBytes(ciphertext, self._cpabe.group)

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, user_id, ciphertext):
        ct = bytesToObject(ciphertext, self._cpabe.group)
        c1, c2 = ct['c1'], ct['c2']
        intermediate_value = self._cpabe.proxy_decrypt(self._params, cloud_server_private_key, proxy_key_user, c1)
        if intermediate_value is False:
            raise Exception("failed to decrypt!")
        partial_ct = {'v': intermediate_value, 'c2': c2}
        partial_ct_b64 = objectToBytes(partial_ct, self._cpabe.group)
        return partial_ct_b64

    def decrypt(self, user_private_key, partial_ct_b64):
        partial_ct = bytesToObject(partial_ct_b64, self._cpabe.group)
        symm_key = self._cpabe.decrypt(self._params, user_private_key, partial_ct['v'])
        if symm_key is False:
            raise Exception("failed to decrypt!")
        cipher = AuthenticatedCryptoAbstraction(sha2(symm_key))
        return cipher.decrypt(partial_ct['c2'])

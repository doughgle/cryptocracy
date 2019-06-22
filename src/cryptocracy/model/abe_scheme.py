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

    def proxy_keygen(self, master_secret_key, params, cloud_server_public_key, user_public_key, attribute_list):
        raise NotImplementedError

    def encrypt(self, plaintext, policy_expression):
        raise NotImplementedError

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, user_id, ciphertext):
        return "intermediate_value"

    def decrypt(self, user_private_key, intermediate_value):
        raise NotImplementedError


class CharmHybridABE(object):
    """
    Outputs are serialized to base64 encoded bytes.
    Inputs are deserialized to group elements.
    """

    def __init__(self):
        group = PairingGroup('SS512')
        self._cpabe = YLLC15(group)
        self._params, self._msk = self._cpabe.setup()

    def setup(self):
        self._params, self._msk = self._cpabe.setup()
        return objectToBytes(self._params, self._cpabe.group), objectToBytes(self._msk, self._cpabe.group)

    def user_keygen(self, params):
        params = bytesToObject(params, self._cpabe.group)
        pk, sk = self._cpabe.ukgen(params)
        return objectToBytes(pk, self._cpabe.group), objectToBytes(sk, self._cpabe.group)

    def proxy_keygen(self, master_secret_key, params, cloud_server_public_key, user_public_key, attribute_list):
        pkcs = bytesToObject(cloud_server_public_key, self._cpabe.group)
        pku = bytesToObject(user_public_key, self._cpabe.group)
        msk = bytesToObject(master_secret_key, self._cpabe.group)
        params = bytesToObject(params, self._cpabe.group)
        proxy_key = self._cpabe.proxy_keygen(params, msk, pkcs, pku, attribute_list)
        return objectToBytes(proxy_key, self._cpabe.group)

    def encrypt(self, params, plaintext, policy_expression):
        params = bytesToObject(params, self._cpabe.group)
        symm_key = self._cpabe.group.random(GT)
        c1 = self._cpabe.encrypt(params, symm_key, policy_expression)
        cipher = AuthenticatedCryptoAbstraction(sha2(symm_key))
        c2 = cipher.encrypt(plaintext)
        ciphertext = {'c1': c1, 'c2': c2}
        return objectToBytes(ciphertext, self._cpabe.group)

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, ciphertext):
        skcs = bytesToObject(cloud_server_private_key, self._cpabe.group)
        ct = bytesToObject(ciphertext, self._cpabe.group)
        pxku = bytesToObject(proxy_key_user, self._cpabe.group)
        c1, c2 = ct['c1'], ct['c2']
        intermediate_value = self._cpabe.proxy_decrypt(skcs, pxku, c1)
        if not intermediate_value:
            raise DecryptionFailed("ERROR: failed to proxy-decrypt!")
        partial_ct = {'v': intermediate_value, 'c2': c2}
        return objectToBytes(partial_ct, self._cpabe.group)

    def decrypt(self, user_private_key, partial_ct_b64):
        sku = bytesToObject(user_private_key, self._cpabe.group)
        partial_ct = bytesToObject(partial_ct_b64, self._cpabe.group)
        # public scheme params are not required for decrypt
        symm_key = self._cpabe.decrypt(None, sku, partial_ct['v'])
        if not symm_key:
            raise DecryptionFailed("ERROR: failed to decrypt!")
        cipher = AuthenticatedCryptoAbstraction(sha2(symm_key))
        return cipher.decrypt(partial_ct['c2'])


class DecryptionFailed(Exception):
    pass

#!/usr/bin/env python
"""
Usage: cryptocracy setup [options]
       cryptocracy generate keypair [--public-key-file=<pku>] [--secret-key-file=<sku>] [options]
       cryptocracy register <email_address> [--public-key-file=<pku>] [options]
       cryptocracy add user <email_address> <attributes_json_array> [options]
       cryptocracy list (user|file) [options]
       cryptocracy revoke user <email_address> [options]
       cryptocracy encrypt <input_file> <read_policy_expression> <output_file> [options]
       cryptocracy decrypt <file> [--secret-key-file=<secret_key_b64>] [options]
       cryptocracy upload <source_url> [<dest_key>] [options]
       cryptocracy download <url> <user_id> [options]

Options:
  --params=FILE                  Path to the scheme public parameters file to use for CLI commands. [default: $HOME/.cryptocracy/params]
  --msk=FILE                     Path to the master secret key for the scheme. [default: $HOME/.cryptocracy/msk]
  --public-key-file=<pku>        Destination path for user public key generation [default: $HOME/.cryptocracy/user.pub]
  --secret-key-file=<sku>        Destination path for user secret key generation [default: $HOME/.cryptocracy/user.key]
  --email-address=ADDRESS        Identity of the caller for upload download commands.
  -v, --verbose                  Show debug information.
  -h --help                      Show this screen.
  --version                      Show version.

"""
import functools

from cryptocracy.boundaries.key_authority_service import KeyAuthorityService
from cryptocracy.use_cases.decrypt_file import DecryptUseCase, DecryptRequest

__version__ = '0.2.2'

import os
import traceback

import requests
from docopt import docopt

from cryptocracy.boundaries.object_store import AwsObjectStore
from cryptocracy.boundaries.proxy_key_store import AwsProxyKeyStore
from cryptocracy.model.abe_scheme import CharmHybridABE
from cryptocracy.model.result import RESULT
from cryptocracy.use_cases.add_user import AddUserUseCase, AddUserRequest
from cryptocracy.use_cases.download_file import DownloadFileUseCase, DownloadFileRequest
from cryptocracy.use_cases.encrypt_file import EncryptFileUseCase, EncryptFileRequest
from cryptocracy.use_cases.generate_key_pair import GenerateKeyPairUseCase, GenerateKeyPairRequest
from cryptocracy.use_cases.list_users import ListUsersUseCase, ListUsersRequest
from cryptocracy.use_cases.register_user import RegisterUserUseCase, RegisterUserRequest
from cryptocracy.use_cases.revoke_user import RevokeUserUseCase, RevokeUserRequest
from cryptocracy.use_cases.setup import SetupUseCase, SetupRequest
from cryptocracy.use_cases.upload_file import UploadFileUseCase, UploadFileRequest


def main():
    try:
        (setup,
         generate_key_pair,
         register_user,
         add_user,
         revoke_user,
         list_users,
         download_file,
         encrypt_file,
         upload_file,
         decrypt_file) = init_use_cases()

        cryptocracy_home = create_cryptocracy_home()

        args = docopt(__doc__, version=__version__)
        if args['--verbose']:
            print(args)
        user_id = args['<email_address>']
        response = "Coming soon..!"
        if args['setup']:
            response = setup.run(SetupRequest())
            save_setup(cryptocracy_home, response)
        if args['generate'] and args['keypair']:
            response = generate_key_pair.run(GenerateKeyPairRequest(params=load(args['--params']),
                                                                    public_key_file=args['--public-key-file'],
                                                                    secret_key_file=args['--secret-key-file']))
        if args['register']:
            response = register_user.run(RegisterUserRequest(user_id=user_id,
                                                             pku_b64=load(args['--public-key-file'])))
        if args['user']:
            if args['add']:
                response = add_user.run(AddUserRequest(msk=load(args['--msk']),
                                                       params=load(args['--params']),
                                                       user_id=user_id,
                                                       attributes=args['<attributes_json_array>']))
            elif args['revoke']:
                response = revoke_user.run(RevokeUserRequest(user_id=user_id))
            elif args['list']:
                response = list_users.run(ListUsersRequest())
        if args['upload']:
            response = upload_file.run(UploadFileRequest(args['<source_url>']))
        if args['download']:
            response = download_file.run(DownloadFileRequest(user_id=args['<user_id>'],
                                                             request_url=args['<url>']))
        if args['encrypt']:
            response = encrypt_file.run(
                EncryptFileRequest(input_file=args['<input_file>'],
                                   read_policy_expression=args['<read_policy_expression>'],
                                   output_file=args['<output_file>'],
                                   params=load(args['--params'])))
        if args['decrypt']:
            request = DecryptRequest(secret_key_b64=load(args['--secret-key-file']),
                                     partial_ct_b64=load(args['<file>']),
                                     output_file=args['<file>'])
            response = decrypt_file.run(request)

        print(response)
    except Exception as err:
        print(err)
        traceback.print_tb(err.__traceback__)


def init_use_cases():
    proxy_key_store = AwsProxyKeyStore(os.getenv('CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME'))
    abe_scheme = CharmHybridABE()
    ka_service = KeyAuthorityService(requests, server_address='localhost:5000')
    setup = SetupUseCase(abe_scheme)
    generate_key_pair = GenerateKeyPairUseCase(abe_scheme)
    register_user = RegisterUserUseCase(ka_service)
    add_user = AddUserUseCase(ka_service, abe_scheme, proxy_key_store)
    revoke_user = RevokeUserUseCase(proxy_key_store)
    list_users = ListUsersUseCase(proxy_key_store)

    object_store = AwsObjectStore(os.getenv('CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME'))
    object_cache = AwsObjectStore(os.getenv('CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME'))
    upload_file = UploadFileUseCase(object_store)
    download_file = DownloadFileUseCase(functools.partial(load, "$HOME/.cryptocracy/cloud.key"),
                                        proxy_key_store,
                                        object_store,
                                        object_cache,
                                        abe_scheme=abe_scheme)

    encrypt_file = EncryptFileUseCase(abe_scheme)
    decrypt_file = DecryptUseCase(abe_scheme)
    return (setup,
            generate_key_pair,
            register_user,
            add_user,
            revoke_user,
            list_users,
            download_file,
            encrypt_file,
            upload_file,
            decrypt_file)


def save_setup(cryptocracy_home, response):
    if response['result'] == RESULT.SUCCESS:
        with open(os.open(os.path.join(cryptocracy_home, 'msk'), os.O_CREAT | os.O_WRONLY, 0o600), 'wb') as f:
            f.write(response['msk'])
        with open(os.open(os.path.join(cryptocracy_home, 'params'), os.O_CREAT | os.O_WRONLY, 0o644), 'wb') as f:
            f.write(response['params'])


def create_cryptocracy_home():
    home = os.path.expanduser("~")
    cryptocracy_home = os.path.join(home, '.cryptocracy')
    os.makedirs(cryptocracy_home, mode=0o700, exist_ok=True)
    return cryptocracy_home


def load(config_file):
    """
    :param config_file: a Cryptocracy param file holding a single value.
    :return: the file contents as (base64-encoded) bytes
    """
    with open(os.path.expandvars(config_file), 'rb') as c:
        return c.read()


if __name__ == '__main__':
    main()

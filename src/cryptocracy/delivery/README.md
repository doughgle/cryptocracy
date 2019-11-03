# Delivery mechanisms

## Command Line Interface (CLI)

Make `cryptocracy` executable and execute it like in the following example with `--help` to see usage and options:

Cryptocracy has a command line interface for performing secure file sharing operations. 
In version 0.1.2, for example, the commands and options shown from the help menu of the CLI look like this:

```bash
Usage: cryptocracy setup [options]
       cryptocracy generate keypair [--public-key-file=<pku>] [--secret-key-file=<sku>] [options]
       cryptocracy register <email_address> [--public-key-file=<pku>] [options]
       cryptocracy add user <email_address> <attributes_json_array> [options]
       cryptocracy list (user|file) [options]
       cryptocracy revoke user <email_address> [options]
       cryptocracy encrypt <input_file> <policy_expression> <output_file> [options]
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
```

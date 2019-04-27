# Delivery mechanisms

## Command Line Interface (CLI)

Make cryptocracy executable and execute it like in the following example with `--help` to see usage and options:

```bash
src/delivery/cli$ ./cryptocracy --help
Usage: cryptocracy setup [options]
       cryptocracy generate keypair [--public-key-file=<pku>] [--secret-key-file=<sku>] [options]
       cryptocracy add user <email_address> <user_public_key> <attribute_expression> [options]
       cryptocracy list (user|file) [options]
       cryptocracy revoke user <email_address> [options]
       cryptocracy encrypt <input_file> <policy_expression> <output_file> [options]
       cryptocracy decrypt <file> [options]
       cryptocracy upload <source_url> [<dest_key>] [options]
       cryptocracy download <url> <user_id> [options]

Options:
  --params=FILE                  Path to the scheme public parameters file to use for CLI commands. [default: $HOME/.cryptocracy/params]
  --public-key-file=<pku>        Destination path for user public key generation [default: $HOME/.cryptocracy/user.pub]
  --secret-key-file=<sku>        Destination path for user secret key generation [default: $HOME/.cryptocracy/user.key]
  --email-address=ADDRESS        Identity of the caller for upload download commands.
  -v, --verbose                  Show debug information.
  -h --help                      Show this screen.
  --version                      Show version.
```
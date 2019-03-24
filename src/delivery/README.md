# Delivery mechanisms

## Command Line Interface (CLI)

Make proxy-crypt executable and execute it like in the following example with `--help` to see usage and options:
```bash
$ cli/proxy-crypt --help
Usage: proxy-crypt user add <email_address> <user_public_key> <attribute_expression> [options]
       proxy-crypt user list [options]
       proxy-crypt user revoke <email_address> [options]
       proxy-crypt (encrypt|decrypt) <file> [options]
       proxy-crypt (upload|download) <url> --email-address=ADDRESS [options]

Options:
  --proxy-crypt-config=FILE      Path to the config file to use for CLI commands. [default: $HOME/.proxy-crypt]
  --email-address=ADDRESS        Identity of the caller for upload download commands.
  -v, --verbose                  Show debug information.
  -h --help                      Show this screen.
  --version                      Show version.
```

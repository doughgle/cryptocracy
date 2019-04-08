# Delivery mechanisms

## Command Line Interface (CLI)

Make cryptocracy executable and execute it like in the following example with `--help` to see usage and options:
```bash
$ cli/cryptocracy --help
Usage: cryptocracy user add <email_address> <user_public_key> <attribute_expression> [options]
       cryptocracy user list [options]
       cryptocracy user revoke <email_address> [options]
       cryptocracy (encrypt|decrypt) <file> [options]
       cryptocracy (upload|download) <url> --email-address=ADDRESS [options]

Options:
  --cryptocracy-config=FILE      Path to the config file to use for CLI commands. [default: $HOME/.cryptocracy]
  --email-address=ADDRESS        Identity of the caller for upload download commands.
  -v, --verbose                  Show debug information.
  -h --help                      Show this screen.
  --version                      Show version.
```

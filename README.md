# Cryptocracy

> Democratise cryptographic access control to your data stored in an untrusted cloud.

[![Build Status](https://travis-ci.com/doughgle/cryptocracy.svg?branch=master)](https://travis-ci.com/doughgle/cryptocracy)

This project is a reference design for using Attribute-Based Encryption (ABE) for the purpose of confidential one-to-many file-sharing in an untrusted public cloud.
For now, it depends on infrastructure hosted on Amazon Web Services (AWS) (you'll need an AWS account). 
It leverages the popular Charm Crypto Python Framework for the Extended Proxy-Assisted Attribute-Based Encryption implementation. It demonstrates practical considerations and offers a starting point so that you can evaluate ABE technology for your application.

## Features

+ share files securely in an untrusted public cloud.
+ ensure data privacy against the cloud service provider.
+ express fine-grained access policies, per file, as code.
+ revoke users to deny access or achieve temporal access control.
+ leverage the power of cloud for many-to-many file sharing at scale. 

## Requirements

+ An AWS account
+ Linux
+ Terraform
+ Python 3.5+
+ Charm Crypto Library (and its pre-requisite libraries)

## Getting Started

Define your AWS creds. In this example, as environment variables. See AWS docs for alternatives.  
```sh
$ export AWS_ACCESS_KEY_ID="FOO"
$ export AWS_SECRET_ACCESS_KEY="BAR"
$ export AWS_DEFAULT_REGION="ap-southeast-1"
```

Create the infrastructure.
```bash
$ terraform init
$ terraform workspace new playground
$ terraform apply
```

See [Terraform README](terraform-infra/README.md) for more details.

## CLI
```bash
$ ./proxy-crypt
Usage: proxy-crypt setup
       proxy-crypt generate keypair
       proxy-crypt add user <email_address> <user_public_key> <attribute_expression> [options]
       proxy-crypt list (user|file) [options]
       proxy-crypt revoke user <email_address> [options]
       proxy-crypt encrypt <file> <policy_expression> [options]
       proxy-crypt decrypt <file> [options]
       proxy-crypt upload <source_url> [<dest_key>] --email-address=ADDRESS [options]
       proxy-crypt download <url> --email-address=ADDRESS [options]
```

## Developing

With virtualenvwrapper installed, you can create a new virtualenv primed with the pip dependencies. 
```bash
$ mkproject -a /path/to/proxy-crypt -r requirements.txt --python=python3 cryptocracy
```

Install Charm crypto

```bash
$ workon charm-crypto-py3
$ ./configure.sh --python=$(which python) --extra-cflags=-I/usr/local/include --extra-ldflags=-L/usr/local/lib
$ make install
$ sudo ldconfig
$ make test
```

### Clean
```sh
$ python setup.py clean --all
```

### Install locally for development
```bash
$ pip install -e .
```

### Test
#### Run Unit Tests
```sh
$ python setup.py test
```

#### Run Integration Tests


### Package
```sh
$ python setup.py sdist
```

### Register in PyPi
```
$ python setup.py register
```

### Publish to PyPi
```
$ python setup.py upload
```

## Use Cases
See [use-cases.md](src/use_cases/README.md) for use case descriptions.

## Disclaimer

This software is licensed with LGPL-3.0. Consider carefully if it may be fit for your purpose. Always read the license.
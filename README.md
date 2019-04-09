# Cryptocracy

> Democratise cryptographic access control to your data stored in an untrusted cloud.

This project is a reference design for using Attribute-Based Encryption (ABE) for the purpose of secure one-to-many file-sharing in an untrusted public cloud.
For now, it depends on infrastructure hosted on Amazon Web Services (AWS) (you'll need an AWS account). 
It leverages the popular Charm Crypto Python Framework for the Extended Proxy-Assisted Attribute-Based Encryption implementation. It demonstrates practical considerations and offers a starting point so that you can evaluate ABE technology for your application.

[![Build Status](https://travis-ci.com/doughgle/cryptocracy.svg?branch=master)](https://travis-ci.com/doughgle/cryptocracy)
[![Tested with Hypothesis](https://img.shields.io/badge/hypothesis-tested-brightgreen.svg)](https://hypothesis.readthedocs.io/)

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
+ Python >= 3.4
+ Charm Crypto Library (and its pre-requisite libraries)

## Getting Started

Define your AWS creds. In this example, as environment variables. See AWS docs for alternatives.  
```sh
$ export AWS_ACCESS_KEY_ID="FOO"
$ export AWS_SECRET_ACCESS_KEY="BAR"
$ export AWS_DEFAULT_REGION="ap-southeast-1"
```

##### Create the infrastructure

From the terraform-infra directory, execute the following commands to setup the infrastructure for Cryptocracy.
```bash
terraform-infra$ terraform init
terraform-infra$ terraform workspace new playground
terraform-infra$ terraform apply
```

If Terraform succeeds, you'll see something like the following:

```bash
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

object_cache_bucket_name = object-cache-playground-2c6b29f4-d10b-3419-ce66-a5fa80a197de
object_store_bucket_name = encrypted-files-playground-2c6b29f4-d10b-3419-ce66-a5fa80a197de
proxy_key_store_table_name = proxy-key-table-playground
```

Copy the values from the Terraform outputs and create environment variables for each one:

```bash
$ export CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME=encrypted-files-playground-2c6b29f4-d10b-3419-ce66-a5fa80a197de
$ export CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME=object-cache-playground-2c6b29f4-d10b-3419-ce66-a5fa80a197de
$ export CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME=proxy-key-table-playground
```
 
See [Terraform README](terraform-infra/README.md) for more details.

##### Setup the Key Authority

```bash
src/delivery/cli$ ./cryptocracy setup
```

This will generate 2 files - `params` and `msk`.
> `params` is the public parameters for the scheme.
> `msk` is the master secret key for the scheme.

It will put them in your Cryptocracy home directory (`$HOME/.cryptocracy` by default).
The Key Authority can now share the public parameters file with all of the users of Cryptocracy.

Once a Data Owner has the `params`, they can begin encrypting files with access policies.
They can also generate a user key pair. 

## CLI
```bash
$ ./cryptocracy
Usage: cryptocracy setup
       cryptocracy generate keypair
       cryptocracy add user <email_address> <user_public_key> <attribute_expression> [options]
       cryptocracy list (user|file) [options]
       cryptocracy revoke user <email_address> [options]
       cryptocracy encrypt <file> <policy_expression> [options]
       cryptocracy decrypt <file> [options]
       cryptocracy upload <source_url> [<dest_key>] --email-address=ADDRESS [options]
       cryptocracy download <url> --email-address=ADDRESS [options]
```

## Developing

With virtualenvwrapper installed, you can create a new virtualenv primed with the pip dependencies. 
```bash
$ mkproject -a /path/to/cryptocracy -r requirements.txt --python=python3 cryptocracy
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
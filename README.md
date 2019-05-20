# Cryptocracy

> Democratise cryptographic access control to your data stored in an untrusted cloud.

This project is a reference design for using Attribute-Based Encryption (ABE) for the purpose of secure one-to-many file-sharing in an untrusted public cloud.
For now, it depends on infrastructure hosted on Amazon Web Services (AWS) (you'll need an AWS account). 
It leverages the popular Charm Crypto Python Framework for the Extended Proxy-Assisted Attribute-Based Encryption implementation.
It demonstrates practical considerations and offers a starting point so that you can evaluate ABE technology for your application.

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

#### Create the infrastructure

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

object_cache_bucket_name = object-cache-playground-cab79872-ccda-4987-8115-d024dd19618d
object_store_bucket_name = encrypted-files-playground-cab79872-ccda-4987-8115-d024dd19618d
proxy_key_store_table_name = proxy-key-table-playground
```

Copy the values from the Terraform outputs and create environment variables for each one.
Note that variable names are capitalised and prefixed with `CRYPTOCRACY`.
Also remember not to put spaces between variable name and value.  

```bash
$ export CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME=encrypted-files-playground-cab79872-ccda-4987-8115-d024dd19618d
$ export CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME=object-cache-playground-cab79872-ccda-4987-8115-d024dd19618d
$ export CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME=proxy-key-table-playground
```
 
See [Terraform README](terraform-infra/README.md) for more details.

#### Setup the Key Authority

```bash
(KA)src/delivery/cli$ ./cryptocracy setup
```

This will generate 2 files - `params` and `msk`.
> `params` is the public parameters for the scheme.
> `msk` is the master secret key for the scheme.

It will put them in your Cryptocracy home directory (`$HOME/.cryptocracy` by default).
The Key Authority can now share the public parameters file with all of the users of Cryptocracy.

Here, we'll upload it to our S3 bucket:

```bash
(KA)src/delivery/cli$ ./cryptocracy upload ~/.cryptocracy/params 
{'result': <RESULT.SUCCESS: 1>, 'url': 'https://encrypted-files-playground-cab79872-ccda-4987-8115-d024dd19618d.s3.amazonaws.com/params?Signature=9DIXUT0PLP83TVH2REWVTLSVDQAFZIW&AWSAccessKeyId=QOJC73Y43KCG0B45H5W1C&Expires=1554989651'}
```

Once a Data Owner has the `params`, they can begin encrypting files with access policies.
They can also generate a user key pair. 

#### Encrypt your first file

Now we're on the Data Owner's machine.
First, we need to get the public scheme parameters from the bucket.
Since the public parameters are in plaintext, we can simply download using the url given upon upload.

```bash
(DO)$ wget 'https://encrypted-files-playground-cab79872-ccda-4987-8115-d024dd19618d.s3.amazonaws.com/params?Signature=9DIXUT0PLP83TVH2REWVTLSVDQAFZIW&AWSAccessKeyId=QOJC73Y43KCG0B45H5W1C&Expires=1554989651' -O ~/.cryptocracy/params
```

Let's start from the beginning. 
We'll create a file `hello` with the plaintext contents `hello world`:

```bash
(DO)src/delivery/cli$ echo "hello world" > hello
```

Now we can encrypt our plaintext `hello` with a policy expression.
Since we know that the file contains a common and safe greeting amongst humans, 
we'll specify an access policy of `(human or earthling)`.
We'll output the resulting ciphertext to `hello.enc`.

```bash
(DO)src/delivery/cli$ ./cryptocracy encrypt hello '(human or earthling)' hello.enc
{'result': <RESULT.SUCCESS: 1>, 'output_file': 'hello.enc'}
``` 

Inspecting the ciphertext, you can see that its base64 encoded.
That's convenient for transport and storage!

```bash
(DO)src/delivery/cli$ cat hello.enc ; echo
eJztVk1vGzcQ/SuCTg2gA8nlZ4AcFDmJHEQJ2rpF4TpYrPVlAbLjSkra1PB/L998rJRb00sPyWGlXXI4nJn33pAPw7kbPh08DG/36/o/3B92Tx+uhue/XtWvq+H6+ebd7HZ69+ky/zi9XC1fxxIm62fProajOjt7d/YCdg4fk839zXJ3sfzrwEuvV2d/v/zt/PL12d6HafNHsx1fzP7UpeM3r2BmHuvXcLFZL/cH3d44Z1dNSCWErkvWLVbBzYtfxXSd56lrukVc5tiFRbeyC2uSLdb4sFr5xXUy3i3gsdv22Uxn40n783Tsho91Ym4p2wn9tu182+33bQvb68+H5R5r2/ZTt/24pNHfgx0NQh4NYhwNchkNrK0v1tS3HEaD5EeDkjBQR1MdCPXJRsywJll81JFQTT0cuPpRMkbrwhT5sYYWiYeEaVMXZPJNP3Uo1JcMvwG21XGqi2L1mRoOBQH6xJHgoeUWMRoxqk9wGCyyOpymlJzshPiQXzDsxCcNyPFO5CDqDOJGsigFtmDTzANYT0nRLnBq2UeIkgZKQyHXd9+IlTX0RhHV8WzZEwLoU87iqOExKi2clCJpEk4SMibwnhteQfUn35iBOXI5QpR6VIzkeyxn5lppFhSME3tC3Yslwuo9wQTkABq0j3VSPDIBDDzccJRUC5rWMIiNmnlUmmU25dIhSy/lC0E3AYeAN1UEoGNR1hIhymjfQx+T9n63uV3+W3kg3pBlX+ucJJfkA4xlvhmGkOuNQJwVWgatTo8J8u8LIeyMJ8qJ8kALqCmqQpywXF/a1fM4b9jIHsSiLFWlLYxwCjCy2hoRrSkSJQWVpeIcV1AJFWErQ2VZgkG4TA1B1Ed+AXOQf8iLasSqB/WzoMVTVnhWTvoNLQD4cJvtF8jdf9hu5p/b2vK08/1w8/G2uxt82A2W3e5ws93crZ8AwXnbHQ67PWE8/WU2fgskvxLuKCGSmkT6qFGWNkRgUSFES1RkJ1ViipNIMncZUVlQfKRjhr5pROkGwDLLxkQkm7VZWAWUf0Ac0IFo7owMc8dT4qHcRdlKGyXpjNiDNR0VXjkCUP+sqvlSYUVkSbsxuF5aKh8R0sGpcSTpFUFPCWmY8ELUtVE7Qzg2fnoI8a8XaJJGC6YRi+SMQE1Ji1m7skwy/1F26r1WkjfauAVfr+ZW+r508HxaipL6chjWL/VtkUTWBsFANMdgWABSvKLokl7jsW/DOspJk/Wotf1Rq6JmGgiQWE+neJIZZopjL6Rats96EjlJOmt3ojA8MyUKJ3D6nGrzfcXkxfini+mb87evvkvtG5Ca8kWP6hxVG335+XYj0PhGdZdYGUWoTqdI6Wsmd8osN7SkkrYSeArHw1DuLkkK2ZwCQzV2uiroacc3CrnygcX9NZWcQWZ6oGe9A2a5b3D4epZrp0iSGG8hCBRzPNkgP+zk9cqj0Zn+Hkiks2qv5GMi+/6nHOE6vcf819vMd839z5p7fPwHAAbsGQ==
```

#### Upload the ciphertext
Now it's encrypted, we can safely upload it to our object store:

```bash
(DO)src/delivery/cli$ ./cryptocracy upload hello.enc 
{'result': <RESULT.SUCCESS: 1>, 'url': 'https://encrypted-files-playground-b60f37bb-ee49-41d4-91a4-26ebde416e61.s3.amazonaws.com/hello.enc?Signature=v6THLqiGQ6HhD8Yxof%2FHlAtn9yQ%3D&Expires=1555080419&AWSAccessKeyId=QOJC73Y43KCG0B45H5W1C'}
```

#### Register User with the Key Authority

On the User's machine, the user must first generate a key pair:

```bash
(User)src/delivery/cli$ ./cryptocracy generate keypair
{'secret_key_file': '$HOME/.cryptocracy/user.key', 'result': <RESULT.SUCCESS: 1>, 'secret_key': b'eJwtjjEOwzAIRa+CPDOYJDa4V4kiK628ZXMTqap693ySDoAfH775hlqPddtbreFB82RMCVGUSaQwWUSIw8SkA9QMiIDsKqCgKlZkiD42erJb1vE/e1vhYcU7ME+wMlS9vAH+c5aFCQe9trX366Dw/LxbD78TeyUjwg==', 'public_key': b'eJw1UUFOxDAM/ErUcw6ZNk4cvoJW1YL2trcCEkL8HY9tDm4Tj8czdn628/y6Pz8f57m9lFdptYjWMlYty2JILYpa0GYk0YYhdgEOKzVILTuVCcKw07QSPTKI7NZ1ehdm9iSvlQfWAZ04e9ltkuBqTjeGGNxXqkn8XVF7BID0wSZCymDWPp122x4wW/cjExyNpSqhG3b2f7eSg6OZgEgo+4ieVhdoQedOGBxYW2zOQZnhYGiadINoCC/eG5DcDmkDt1rsXd6f9+vyd9nevj8e1/b7B9SfUpU=', 'public_key_file': '$HOME/.cryptocracy/user.pub'}
```

By default the keypair will be created in the Cryptocracy home directory (`$HOME/.cryptocracy`).

Next, the user registers their public key with the Key Authority:

```bash
(User)src/delivery/cli$ ./cryptocracy register alice@a.com
{'result': <RESULT.SUCCESS: 1>, 'user_id': 'alice@a.com', 'user_public_key': 'eJw9UUEOwjAM+0q18w7N1iYpX0FoGmi33QZICPF3nC7tIVEbJ7abfodlea/7a1uW4RKuOY4h6xgoCtKEmyIYl1TGIAjOAGh2lGiyZBMEoNQD+bygohjJjEhWBMwoqIHoUoR0gshNl5DMieklSJViRTBIOgfF9CMO2dzE2VN2KEnrz42XoutXn564PQcexPSqjWZI3EGlrlZjf6uVJ5uyzejpo0QnVu59zaewO7I1aj5XYLvR0tsmt1TZbU1MtzHgfx77ehz1f4b757kdw+8PEiJT5Q==', 'error': None}
```

By default, the `register` command will register `$HOME/.cryptocracy/user.pub` as the public_key_file for the user.

#### Register Cloud Service Provider (CSP) with the Key Authority
For a Cloud Service Provider, the registration procedure is almost the same as for a user.

First the CSP generates a key pair:

```bash
(CSP)src/delivery/cli$ ./cryptocracy generate keypair --public-key-file $HOME/.cryptocracy/cloud.pub --secret-key-file $HOME/.cryptocracy/cloud.key
{'secret_key_file': '$HOME/.cryptocracy/cloud.key', 'result': <RESULT.SUCCESS: 1>, 'secret_key': b'eJwtjjEOwzAIRa+CPDOYJDa4V4kiK628ZXMTqap693ySDoAfH775hlqPddtbreFB82RMCVGUSaQwWUSIw8SkA9QMiIDsKqCgKlZkiD42erJb1vE/e1vhYcU7ME+wMlS9vAH+c5aFCQe9trX366Dw/LxbD78TeyUjwg==', 'public_key': b'eJw1UUFOxDAM/ErUcw6ZNk4cvoJW1YL2trcCEkL8HY9tDm4Tj8czdn628/y6Pz8f57m9lFdptYjWMlYty2JILYpa0GYk0YYhdgEOKzVILTuVCcKw07QSPTKI7NZ1ehdm9iSvlQfWAZ04e9ltkuBqTjeGGNxXqkn8XVF7BID0wSZCymDWPp122x4wW/cjExyNpSqhG3b2f7eSg6OZgEgo+4ieVhdoQedOGBxYW2zOQZnhYGiadINoCC/eG5DcDmkDt1rsXd6f9+vyd9nevj8e1/b7B9SfUpU=', 'public_key_file': '$HOME/.cryptocracy/cloud.pub'}
```

Then, the CSP registers its public key with the Key Authority:

```bash
(CSP)src/delivery/cli$ ./cryptocracy register cryptocracy@amazonaws.com --public-key-file $HOME/.cryptocracy/cloud.pub 
{'error': None, 'result': <RESULT.SUCCESS: 1>, 'user_id': 'cryptocracy@amazonaws.com', 'user_public_key': 'eJw9UUEOgzAM+0rFuYe6NG3YV6YJsYkbN7ZJ07S/L2kCB0JlJ7bTfod5fi/ba53n4RKulGIgjqG1GHiKAWheGIKWGCZFE2sZBZFDJUEVAA4KnSctp4i2I2cneDSDSaXFlAWj3gFT42x/Es8iRJ2sofubTHJWkMqO6gKAJqumAWSj1akLw2cVaD1j9mFFSObaaKqsGh6w52cngHTuRr5R0bCqjeINLR15yHRqdVqDaUC/FNglnh9uMci7PLZl3/u7DPfPc92H3x/NUVKO'}
```

#### Add an ABE Decryption Key for the User

The Key Authority defines attributes for the user and adds their key to the system.
In this example Alice is given the attribute `human` in her proxy key so that she will be able to decrypt `hello.enc` which has the policy `(human or earthling)`.

```bash
(KA)src/delivery/cli$ ./cryptocracy add user alice@a.com '["human", "female", "age=25"]'
{'user_id': 'alice@a.com', 'result': <RESULT.SUCCESS: 1>}
```

## Disclaimer

This software is licensed with LGPL-3.0. Consider carefully if it may be fit for your purpose. Always read the license.
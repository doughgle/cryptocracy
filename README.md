# Cryptocracy

> Democratise cryptographic access control to your data stored in an untrusted cloud.

This project is a reference design for using Attribute-Based Encryption (ABE) for the purpose of secure one-to-many file-sharing in an untrusted public cloud.
For now, it depends on infrastructure hosted on Amazon Web Services (AWS) - for that, you'll need an AWS account. In future, it will support other public clouds. It will enable you to distribute keys and decryption stages across multiple clouds.
It leverages the popular Charm Crypto Python Framework for the Extended Proxy-Assisted Attribute-Based Encryption implementation.
It demonstrates practical considerations and offers a starting point so that you can evaluate ABE technology for your application.

[![Build Status](https://travis-ci.com/doughgle/cryptocracy.svg?branch=master)](https://travis-ci.com/doughgle/cryptocracy)
[![Tested with Hypothesis](https://img.shields.io/badge/hypothesis-tested-brightgreen.svg)](https://hypothesis.readthedocs.io/)
[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/doughgle/cryptocracy.svg)](https://cloud.docker.com/repository/docker/doughgle/cryptocracy/builds)

## Features

+ share files securely in an untrusted public cloud.
+ ensure data privacy against the cloud service provider.
+ express fine-grained access policies, per file, as code.
+ revoke users to deny access or achieve temporal access control.
+ leverage the power of cloud for many-to-many file sharing at scale. 

## Requirements

+ An AWS account
+ Docker for Linux
+ Terraform

## Getting Started

Define your AWS creds. In this example, as environment variables. See the AWS docs for alternatives.  
```bash
$ export AWS_ACCESS_KEY_ID="FOO"
$ export AWS_SECRET_ACCESS_KEY="BAR"
$ export AWS_DEFAULT_REGION="ap-southeast-1"
```

### Create the infrastructure

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

> `object_store_bucket_name` stores encrypted files (ciphertexts).

> `object_cache_bucket_name` stores user-specific, partially-decrypted ciphertexts.

> `proxy_key_store_table_name` stores user-specific, Attribute-Based Encryption (ABE) proxy decryption keys. 

Copy the values from the Terraform outputs and create environment variables for each one.
Note that variable names are capitalised and prefixed with `CRYPTOCRACY`.
Also remember not to put spaces between variable name and value.  

```bash
$ export CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME=encrypted-files-playground-cab79872-ccda-4987-8115-d024dd19618d
$ export CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME=object-cache-playground-cab79872-ccda-4987-8115-d024dd19618d
$ export CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME=proxy-key-table-playground
```
 
See [Terraform README](terraform-infra/README.md) for more details.

---

### Setup the Key Authority

Pull the Cryptocracy docker image and run it with a shell as the entry process 
and the names of the environment variables you exported earlier:

```bash
$ docker run --env AWS_DEFAULT_REGION \
             --env AWS_ACCESS_KEY_ID \
             --env AWS_SECRET_ACCESS_KEY \
             --env CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME \
             --env CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME \
             --env CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME \
             -it doughgle/cryptocracy bash
```

The following steps are executed on a *Key Authority machine* `(KA)`.

```bash
(KA)cryptocracy@c592c9a96d34:/app/cryptocracy$ cryptocracy setup
```

This will generate 2 files - `params` and `msk`.
> `params` is the public parameters for the scheme.

> `msk` is the master secret key for the scheme.

It will put them in your Cryptocracy home directory (`$HOME/.cryptocracy` by default).
The Key Authority can now share the public parameters file with all of the users of Cryptocracy.

Here, we'll upload `params` to our S3 bucket:

```commandline
(KA)cryptocracy@c592c9a96d34:/app/cryptocracy$ cryptocracy upload $HOME/.cryptocracy/params 
{'result': <RESULT.SUCCESS: 1>, 'url': 'https://encrypted-files-playground-cab79872-ccda-4987-8115-d024dd19618d.s3.amazonaws.com/params?Signature=9DIXUT0PLP83TVH2REWVTLSVDQAFZIW&AWSAccessKeyId=QOJC73Y43KCG0B45H5W1C&Expires=1554989651'}
```

Once a Data Owner has the `params`, they can begin encrypting files with access policies.
They can also generate a user key pair. 

---

### Encrypt your first file

The following steps are executed on a *Data Owner's machine* `(DO)`.

Again, pull the Cryptocracy docker image and run it with a shell as the entry process 
and the names of the environment variables you exported earlier:

```bash
$ docker run --env AWS_DEFAULT_REGION \
             --env AWS_ACCESS_KEY_ID \
             --env AWS_SECRET_ACCESS_KEY \
             --env CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME \
             --env CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME \
             --env CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME \
             -it doughgle/cryptocracy bash
```

First, we need to get the public scheme parameters from the bucket.
Since the public parameters are in plaintext, we can simply download using the url given by the Key Authority.

```bash
(DO)cryptocracy@7cbd4d44ae20:~$ wget -O $HOME/.cryptocracy/params 'https://encrypted-files-playground-cab79872-ccda-4987-8115-d024dd19618d.s3.amazonaws.com/params?Signature=9DIXUT0PLP83TVH2REWVTLSVDQAFZIW&AWSAccessKeyId=QOJC73Y43KCG0B45H5W1C&Expires=1554989651'
```

Let's start from the beginning. 
We'll create a file `hello` with the plaintext contents `hello world`:

```bash
(DO)cryptocracy@7cbd4d44ae20:~$ echo 'hello world' > hello
```

Now we can encrypt our plaintext `hello` with a policy expression.
Since we know that the file contains a common and safe greeting amongst humans, 
we'll specify an access policy of `(human or earthling)`.
We'll output the resulting ciphertext to `hello.enc`.

```bash
(DO)cryptocracy@7cbd4d44ae20:~$ cryptocracy encrypt hello '(human or earthling)' hello.enc
{'output_file': 'hello.enc', 'result': <RESULT.SUCCESS: 1>}
``` 

Inspecting the ciphertext, you can see that its base64 encoded.
That's convenient for transport and storage!

```bash
(DO)cryptocracy@7cbd4d44ae20:~$ cat hello.enc ; echo
eJztV8luE0EQ/RVrTiD50D3T1QsSB2MQRpAgwiaB0Wg8niSWHIhss4TI/07X1jY34AbiYLu3qeW9VzXt26qvq3uj2+pqe5F/q+1uc+92Xk2ePZ7nqRmP5tXJ84ePcFLj5MkbHM6r8wf99fnNy9XJ6c3y8vtpl96en315cf/+vMJT09X15bB5NXzb8enXZ2524d3CPrQvplfd0+W7b4vhK57e5/NVty6+ZyeTaftyNqlxfbm6GLY73eqWnet9akI3QA1L2yyHtGigX5jamtoDpABL8L2Pi/48xR5C6GNXBxsH2/VdqvbZZG8p22l7vVldDTRu237dbbdti44WN7thi77b9ku3/jzQ6nuXxiOI41Fs8seNRynPUwbHWj8e+YiDPIsZoZQnAfKCwYW8mwLu5uc8DfIRyIMY2Jg1IEdqm3fQfOKjwbNBa/JGcGLV5gHkVRf5FOAmztGE8XySfFNoGRcONIpPPpM4TnrIWvaJ/kIQf2g+kJFwiMbl6ILFRUTCsnNrIseJxpzCgllh8pgqPoJjtKkmQhQs6AvdE4AEggSOawZhy6a8/YDcXX9ar/qbNmtBJXHn8vNV93H0aTMaus3ucr36eHEXyRN6/4xk5hMRb/jD3HgO3R0j6YQsMEKnhZKYEw4l5RQFThIDIE02qQiQVWAcyTZBYBuxFRQf3AdChxRTswekAVEqAmGlRfbrPcNP4yjcUJzR8Ar+4kcZjE5UwF9oEbdYyCB6SBxpUlJrVi/GkEpaRvXlRE5stVGlBVZCtD/RPP1VwjBxJIzURNIpqlGzVFGiXV+KNohuaYYwRqWDYCaYasNRIi8gVYAokUWjpZUK544BKfRQpdQKIMZAHDWMRARRUJRiRldYu1Ty+FgsUMljQpxl0tk0BQlsgUVBepGQuaYwvCAC9kncUrLUPKycc6UIEcTindIkjFBILFvpB6UCjlUPIlySfpQ4qBdaWQBRbNJmlRhUkk0tedKuMMBBR43cHFeEssJaM4dgtIeAdE607LXNgaKFVoPsJGmnBA3qh0BHvF0j9cRgoF8seO0G/FCQPmaOPVN42k6gNNTSJr12wEYaiyk6bOQrieYIcStNWiqlb7vdbrOlenk0OXs1e/bk9DFWxv9+9/f0u9+/gEjLACXAJZUHiKYjHLpAVOkh6hxnlBkBXcsbGFMKpbkBI4nhkvmkpW7lQlELCEEgb8RUUnQbSZ2vJsBOqBioOoI241T6NsiI+mEqe0dXEGogWjTh+DJhtI9Rn1HD1GodR8pp6zWLJIfn8OlUNN7o3SRJdz3m6kNmZfb6ZHL6v8T+4RJD/2C0XYurEim/B2w4aNEX+aFzqjx9gajyvb5wgvx38EoGFajeqcuFgC/WwNYIeiP3fvKclAy+v5jDnwV6oTLJQbYwRH4xCdNBWCR1RBWZvnMYZb0hOMmI5BqURPqLcnzDF/aQLcqslncWqJzc4Z9KkjsVNyAQqpJU2H6//wELLOvq
```

### Upload the ciphertext
Now it's encrypted, we can safely upload it to our object store:

```bash
(DO)cryptocracy@7cbd4d44ae20:~$ cryptocracy upload hello.enc 
{'result': <RESULT.SUCCESS: 1>, 'url': 'https://encrypted-files-playground-b60f37bb-ee49-41d4-91a4-26ebde416e61.s3.amazonaws.com/hello.enc?Signature=v6THLqiGQ6HhD8Yxof%2FHlAtn9yQ%3D&Expires=1555080419&AWSAccessKeyId=QOJC73Y43KCG0B45H5W1C'}
```

The upload command responds with an expiring URL which can be shared with others so they can download the ciphertext.  

---

### Register User with the Key Authority

Exit the container.
```bash
cryptocracy@7cbd4d44ae20:~$ exit
exit
```

To simulate the *User's machine* `(User)`, pull the Cryptocracy docker image and run it with a shell as the entry process 
and the names of the environment variables you exported earlier:

```bash
$ docker run --env AWS_DEFAULT_REGION \
             --env AWS_ACCESS_KEY_ID \
             --env AWS_SECRET_ACCESS_KEY \
             --env CRYPTOCRACY_OBJECT_CACHE_BUCKET_NAME \
             --env CRYPTOCRACY_PROXY_KEY_STORE_TABLE_NAME \
             --env CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME \
             -it doughgle/cryptocracy bash
```

First, we need to get the public scheme parameters from the bucket.
Since the public parameters are in plaintext, we can simply download using the url given by the Key Authority.

```bash
(User)cryptocracy@55144ac2dc63:/app/cryptocracy$ wget -O ~/.cryptocracy/params 'https://encrypted-files-playground-2c6b29f4-d10b-3419-ce66-a5fa80a197de.s3.amazonaws.com/params?Signature=eZ0yhKoV7cgGD2jCWyx%2FQMvHmAE%3D&Expires=1561214855&AWSAccessKeyId=AKIAJ25YUGY4JXICK2CQ'
```

The user must first generate a key pair:

```bash
(User)cryptocracy@55144ac2dc63:/app/cryptocracy$ cryptocracy generate keypair
{'secret_key': b'eJw9jbEOgzAMRH/FyuwhDg0O/RWEIkBsbAEkVPXfew6FwWfdu5P9cTnP61hKzu5Nbjq3pTgm0GNc96XS/pWYIqbz2C2T+MZE4CKTdn8jAbnWKJqAx8CULJdgROH83b5QuEr1ZEKuT9EeiZrgQCvD9weY6SRw', 'result': <RESULT.SUCCESS: 1>, 'public_key_file': '$HOME/.cryptocracy/user.pub', 'public_key': b'eJxFULtuwzAM/BXBswfSFiUqvxIURlpky+YmQBDk33N8uB1EUbzj6cjXtG0/t8u+b9t0KtP38/e6T3NB9XG53a9ePQvNRXQu2uIwCwJZYM5nXS0BKKi0MZfuSLcAqBtMKAsqFbcuQe0j3rwYn1BVb0QyRio0UyFOKV5gZ8BObweE/81jWqKj/w8zAxTK7t8VxvEVgtRwo2gRF9H024xPmgYrkqahKEC6BF/XmGzkYa65Dl+D9fuCyNXWf/82fl9iYzbLoKSbPXdibEf56/0BHzBShA==', 'secret_key_b64': '$HOME/.cryptocracy/user.key'}
```

By default the keypair will be created in the Cryptocracy home directory (`$HOME/.cryptocracy`) with the user identity prefix `user`.

Next, the user registers their public key with the Key Authority:

```bash
(User)src/delivery/cli$ ./cryptocracy register alice@a.com
{'result': <RESULT.SUCCESS: 1>, 'user_id': 'alice@a.com', 'user_public_key': 'eJw9UUEOwjAM+0q18w7N1iYpX0FoGmi33QZICPF3nC7tIVEbJ7abfodlea/7a1uW4RKuOY4h6xgoCtKEmyIYl1TGIAjOAGh2lGiyZBMEoNQD+bygohjJjEhWBMwoqIHoUoR0gshNl5DMieklSJViRTBIOgfF9CMO2dzE2VN2KEnrz42XoutXn564PQcexPSqjWZI3EGlrlZjf6uVJ5uyzejpo0QnVu59zaewO7I1aj5XYLvR0tsmt1TZbU1MtzHgfx77ehz1f4b757kdw+8PEiJT5Q==', 'error': None}
```

By default, the `register` command will register `$HOME/.cryptocracy/user.pub` as the public_key_file for the user.

---

### Register Cloud Service Provider (CSP) with the Key Authority
For a *Cloud Service Provider* `(CSP)`, the registration procedure is almost the same as for a user.

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

---

### Add an ABE Decryption Key for the User

The *Key Authority* `(KA)` defines attributes for the user and adds their key to the system.
In this example Alice is given the attribute `human` in her proxy key so that she will be able to decrypt `hello.enc` which has the policy `(human or earthling)`.

```bash
(KA)src/delivery/cli$ ./cryptocracy add user alice@a.com '["human", "female", "age=25"]'
{'user_id': 'alice@a.com', 'result': <RESULT.SUCCESS: 1>}
```

### Download a ciphertext

Using the download URL given by the Data Owner, Alice can try to download the ciphertext. If Alice is authorised, 
Cryptocracy will respond with a download URL which can be used with `curl`, `wget` or in the web browser to download the 
partially decrypted ciphertext.    

```bash
(User)src/delivery/cli$ ./cryptocracy download 'https://encrypted-files-playground-2c6b29f4-d10b-3419-ce66-a5fa80a197de.s3.amazonaws.com/hello.enc?AWSAccessKeyId=QOJC73Y43KCG0B45H5W1C&Signature=mwICvgV79noEI3NiVblUJjbwdT0%3D&Expires=1559137356' alice@a.com
{'content': None, 'message': None, 'download_url': 'https://object-cache-playground-2c6b29f4-d10b-3419-ce66-a5fa80a197de.s3.amazonaws.com/d21393c5208d68339b19a45e07aca4477d7ef1a35317b54bb370b211073d4b14?Expires=1559138257&Signature=YNVu0%2BJySuUFENykN9D4oCWk1nU%3D&AWSAccessKeyId=QOJC73Y43KCG0B45H5W1C', 'result': <RESULT.SUCCESS: 1>, 'status': <STATUS.OK: 1>}
```

In this example, she downloads the file to `~/Downloads`.

### Decrypt the ciphertext

Finally, Alice can decrypt the ciphertext using her secret key.

```bash
(User)src/delivery/cli$ ./cryptocracy decrypt ~/Downloads/d21393c5208d68339b19a45e07aca4477d7ef1a35317b54bb370b211073d4b14 --secret-key-file ~/.cryptocracy/alice.key
{'message': '', 'status': <STATUS.OK: 1>, 'result': <RESULT.SUCCESS: 1>, 'output_file': '~/Downloads/d21393c5208d68339b19a45e07aca4477d7ef1a35317b54bb370b211073d4b14'}
```

Success! Inspecting the `output_file`, we can see the original message
that only `(human or earthling)` were authorised to read.

```bash
(User)src/delivery/cli$ cat ~/Downloads/d21393c5208d68339b19a45e07aca4477d7ef1a35317b54bb370b211073d4b14
hello world
```

## Disclaimer

This software is licensed with LGPL-3.0. Consider carefully if it may be fit for your purpose. Always read the [license](LICENSE).
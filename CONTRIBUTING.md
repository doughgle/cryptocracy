# Contributing to Cryptocracy

Thank you for considering contributing to Cryptocracy! :+1:

### Ways to contribute

- Report an Issue
- Fix an Issue :+1:
- Write another delivery mechanism (e.g. web, mobile) :+1::+1:
- Write a boundary implementation and Terraform configuration for another Cloud. :+1::+1::+1:

## Developing

Install the pre-requisite Charm Crypto:

```bash
$ workon charm-crypto-py3
$ ./configure.sh --python=$(which python) --extra-cflags=-I/usr/local/include --extra-ldflags=-L/usr/local/lib
$ make install
$ sudo ldconfig
$ make test
```

With virtualenvwrapper installed, you can create a new virtualenv primed with the pip dependencies. 
```bash
$ mkproject -a /path/to/cryptocracy -r requirements.txt --python=python3 cryptocracy
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
$ pytest
```

### Package
```sh
$ python setup.py sdist
```

## Use Cases
See [use-cases.md](src/use_cases/README.md) for use case descriptions.

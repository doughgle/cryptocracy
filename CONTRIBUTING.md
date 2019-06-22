# Contributing to Cryptocracy

Thank you for considering contributing to Cryptocracy! :+1:

### Ways to contribute

- Ask (and answer) questions
- Report an issue
- Analyse an issue (and share your analysis)
- Fix an issue :+1:
- Write another delivery mechanism (e.g. web, mobile) :+1::+1:
- Write a boundary implementation and Terraform configuration for another Cloud. :+1::+1::+1:

## Developing

Clone this repository:

```commandline
$ git clone https://github.com/doughgle/cryptocracy
```

> Consider using a Python virtualenv to isolate Python package dependencies from the system python.

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

Create a source distribution and a binary distribution as a Python Wheel. 
```sh
$ python setup.py sdist bdist_wheel
```

## Publish to TestPyPI
```sh
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/cryptocracy-<specific version>*
```

## Test the install from TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ cryptocracy
```

# Test a Docker image build with package from TestPyPI

Replace the `pip install` step with TestPyPI repo index 
```dockerfile
RUN pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple cryptocracy
```

## Use Cases
See [use-cases.md](cryptocracy/use_cases/README.md) for use case descriptions.

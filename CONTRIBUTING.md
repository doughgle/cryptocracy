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

## Software Architecture

The high level structure of the software draws inspiration from the books Clean Architecture (Martin, 2017) and Object-Oriented Software Engineering: A Use Case Driven Approach (Jacobson, 1992). The code is organised into Use Cases, Delivery Mechanisms, Input Specifications and Boundaries.

### Use Cases
Each use case is implemented as a function which takes a Request object and returns a Response object. Requests and responses are simply data structures with data fields that are specific to the use case. This design decouples the use cases from the delivery mechanism.

See [use_cases/README.md](src/cryptocracy/use_cases/README.md) for use case descriptions.

### Delivery Mechanisms
Delivery mechanisms wrap the use cases and translate the request and response objects to and from the use cases. The delivery mechanism is technology and application specific. CLI, mobile and web delivery can co-exist with this architecture.

See [delivery/README.md](src/cryptocracy/delivery/README.md) for more details.

### Input Specifications
Input specifications define the data types, formats and ranges that are valid for different inputs. Examples are encryption keys, access policy expressions, and attribute expressions.

### Boundaries
Boundaries represent the interfaces with other systems. They have well-defined interfaces which are depended upon by the Use Cases. Boundaries facilitate interaction with multiple clouds and fast testing of use case behaviour with in-memory implementations.

See [boundaries/README.md](src/cryptocracy/boundaries/README.md) for more details.
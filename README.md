# Proxy Crypt
> Delegate attribute-based decryption to a proxy server without the need to implicitly trust that server.

## Use Cases
See [use-cases.md](src/use_cases/README.md).

### Use CLI
```bash
$ ./proxy-crypt
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

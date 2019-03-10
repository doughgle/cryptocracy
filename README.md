# Proxy Crypt
> Delegate attribute-based decryption to a proxy server without the need to implicitly trust that server.

## Use Cases
See [use-cases.md](src/use_cases/README.md).



## Developing

Install pyopenabe.so into site-packages of your virtualenv.

```bash
$ workon proxy-crypt
(proxy-crypt) /openabe$ pip install -r bindings/python/requirements.txt
(proxy-crypt) /openabe$ . ./env && make -C bindings/python install
```

Install Charm crypto

```bash
$ workon charm-crypto-py3
$ ./configure.sh --python=$(which python) --extra-cflags=-I/usr/local/include --extra-ldflags=-L/usr/local/lib
$ make install
$ sudo ldconfig
$ make test

```

Clean
```sh
$ python setup.py clean --all
```

Install locally for development
```bash
$ pip install -e .
```

Use CLI
```bash
$ ./proxy-crypt
```

Test
```sh
$ python setup.py test
```


Package
```sh
$ python setup.py sdist
```

Register in PyPi
```
$ python setup.py register
```

Publish to PyPi
```
$ python setup.py upload
```

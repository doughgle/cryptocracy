# Proxy Crypt
> Delegate attribute-based decryption to a proxy server without the need to implicitly trust that server.

## Use Cases
See [use-cases.md](./src/use_cases/use-cases.md).

## Developing
Clean
```sh
$ python setup.py clean --all
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

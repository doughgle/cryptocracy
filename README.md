# Proxy Crypt
> Delegate attribute-based decryption to a proxy server without the need to implicitly trust that server.

## Use Cases
See [use-cases.md](src/use_cases/use-cases.md).



## Developing

Install pyopenabe

```bash
$ workon proxy-crypt
(proxy-crypt) dough@ubdg:/media/dough/Storage/repos/tools/openabe$ pip install -r bindings/python/requirements.txt
(proxy-crypt) dough@ubdg:/media/dough/Storage/repos/tools/openabe$ . ./env && make -C bindings/python install
```

Clean
```sh
$ python setup.py clean --all
```

Install locally for development
```bash
$ pip install -e .
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

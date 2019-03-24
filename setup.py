from setuptools import setup, find_packages

setup(
    name='proxy-crypt',
    version='0.1.0',
    description='Delegate attribute-based decryption to a \
    proxy server without the need to implicitly trust that server.',
    url='github.com/doughgle',
    packages=find_packages(),
    install_requires=[],
    author='Douglas Hellinger',
    author_email='some@email.com'
    )

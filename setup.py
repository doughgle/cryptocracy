from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "docopt>=0.6.2",
    "Flask>=1.0.2",
    "requests>=2.21.0",
    "boto3>=1.9.111"
]

setup(
    name='cryptocracy',
    version='0.3.0',
    description='''Client-side attribute-based encryption (ABE)/ access control (ABAC) - 
    Democratise cryptographic access control to your data stored in an untrusted cloud.''',
    url='https://github.com/doughgle/cryptocracy',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.4',
    author='Douglas Hellinger',
    entry_points={
        'console_scripts': ['cryptocracy = cryptocracy.delivery.cli.cryptocracy:main']
    }
)
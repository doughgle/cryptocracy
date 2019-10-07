#!/usr/bin/env bash
# Update the package repository
apt-get -qq update

# Install Base Tools
apt-get install -y git wget make gcc
# Make sure python development tools are installed
apt-get install -y python3-dev python3-setuptools
# Install GMP (The GNU Multiple Precision Arithmetic Library)
apt-get install -y libgmp10 libgmp-dev
wget http://security.ubuntu.com/ubuntu/pool/universe/g/gmp4/libgmp3c2_4.3.2+dfsg-2ubuntu1_amd64.deb
dpkg -i libgmp3c2_4.3.2+dfsg-2ubuntu1_amd64.deb
# Install PBC (The Pairing-Based Cryptography Library)
wget http://voltar.org/pbcfiles/libpbc0_0.5.12_amd64.deb
wget http://voltar.org/pbcfiles/libpbc-dev_0.5.12_amd64.deb
dpkg -i libpbc0_0.5.12_amd64.deb
dpkg -i libpbc-dev_0.5.12_amd64.deb
# Install OpenSSL
apt-get install -y openssl libssl-dev
# Download charm
git clone https://github.com/JHUISI/charm.git

# Install charm
pip install -r charm/requirements.txt
(cd ./charm && ./configure.sh)
make -C ./charm
make install -C ./charm
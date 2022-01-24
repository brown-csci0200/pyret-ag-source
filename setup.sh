#!/usr/bin/env bash

apt update
cd /autograder

# Install node and npm
curl -sL https://deb.nodesource.com/setup_8.9 -o nodesource_setup.sh
bash nodesource_setup.sh
apt install -y make python3 jq build-essential nodejs npm unzip

# Unpack pyret zip
unzip "source/pyret-ag-source/pyret-lang.zip" -d pyret-lang

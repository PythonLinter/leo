#!/usr/bin/env bash

# Preparing the config file
CONFIG_FILE="${HOME}/.config/leo.yml"
CONFIG_DIRECTORY=$(readlink -f ` dirname ${CONFIG_FILE}`)
mkdir -p ${CONFIG_DIRECTORY}

echo "
db:
  url: postgresql://postgres:postgres@localhost/leo_dev
  test_url: postgresql://postgres:postgres@localhost/leo_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres
  echo: false
" > ${CONFIG_FILE}

pip3 install -U pip setuptools wheel coverage coveralls
pip install "git+https://github.com/pylover/nanohttp@develop"
pip install "git+https://github.com/pylover/restfulpy@develop"
pip3 install --no-cache -e .

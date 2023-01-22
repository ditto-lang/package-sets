#! /usr/bin/env bash

# shellcheck shell=bash

# Enable bash "strict mode"
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
shopt -s inherit_errexit
IFS=$'\n\t'

set -x

./scripts/update.js > packages.toml
./scripts/test.sh packages.toml
git add packages.toml
git commit --all -m 'Bump'
./scripts/readme.sh > README.md
git add README.md
git commit -m 'Update README snippet'

#! /usr/bin/env nix-shell
#! nix-shell -i bash -p yq ninja

# shellcheck shell=bash

# Enable bash "strict mode"
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
shopt -s inherit_errexit
IFS=$'\n\t'

mk_ditto_toml() {
    local -r packages_toml=$1
    cat <<TOML
name = "packages-test"
targets = []
dependencies = $(tomlq keys "$packages_toml")

[[package-set.extends]]
path = "$(realpath "$packages_toml")"
TOML
}

main() {
    local -r packages_toml=$1
    local -r tempdir=$(mktemp -d)
    echo "tempdir is $tempdir"
    mk_ditto_toml "$packages_toml" | tee "$tempdir/ditto.toml"
    mkdir "$tempdir/ditto-src"
    pushd "$tempdir"
    DITTO_CACHE_DIR=.ditto-cache DITTO_NINJA=ninja ditto make
    tree .ditto
}

main "$@"

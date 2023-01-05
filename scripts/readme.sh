#! /usr/bin/env bash

# shellcheck shell=bash

# Enable bash "strict mode"
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
shopt -s inherit_errexit
IFS=$'\n\t'

main() {
    local -r commit=$(git rev-parse HEAD)
    cat <<TOML
\`\`\`toml
[[package-set.extends]]
url = "https://raw.githubusercontent.com/ditto-lang/package-sets/$commit/packages.toml"
sha256 = "$(git show "$commit:packages.toml" | sha256sum | awk '{print $1}')"
\`\`\`
TOML
}

main "$@"

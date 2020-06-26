.PHONY: all
all: compile format

.PHONY: compile
compile: ## Compile packages.json
	@(set -euo pipefail; ./build.py | tee packages.json)

	@#FIXME: use ditto for this?
	@nix-hash --type sha256 --base32 packages.json | tee packages.sha256

.PHONY: format
format: ## Format all the things
	find . -iname '*.dhall' -exec sh -c 'echo {}; dhall --ascii format --inplace {}' \;

# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

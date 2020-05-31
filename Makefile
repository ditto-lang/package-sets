.PHONY: compile
compile: ## Compile packages.json
	cat ./package.dhall | dhall-to-json | jq -S | tee packages.json

.PHONY: format
format: ## Format all the things
	find . -iname '*.dhall' -exec sh -c 'echo {}; dhall --ascii format --inplace {}' \;

# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

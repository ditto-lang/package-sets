with import ./nixpkgs { }; mkShell { buildInputs = [ dhall dhall-json jq ]; }

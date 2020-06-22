with import ./nixpkgs { }; mkShell { buildInputs = [ gnumake dhall dhall-json jq ]; }

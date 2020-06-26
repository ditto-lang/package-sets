with import ./nixpkgs { };
mkShell { buildInputs = [ gnumake python3 dhall-json ]; }

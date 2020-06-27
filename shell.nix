with import ./nixpkgs { };
mkShell {
  buildInputs = [
    gnumake
    python3
    dhall # for `dhall format`
    dhall-json
  ];
}

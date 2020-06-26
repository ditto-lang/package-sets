-- TODO: we should construct this in ./build.py I reckon
toMap
  ./src/ditto-lang.dhall
: List { mapKey : Text, mapValue : ./src/Package.dhall }

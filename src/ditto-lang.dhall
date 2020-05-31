let mkPackage =
          \(args : { name : Text, version : Text, rev : Text })
      ->  { name = args.name
          , repo = "https://github.com/ditto-lang/${args.name}.git"
          , version = args.version
          , rev = args.rev
          }

in    [ mkPackage
          { name = "core"
          , version = "0.1.0"
          , rev = "d3a467832bbe7af63adc36a589b5eb31a4dc5bcf"
          }
      ]
    : List ./Package.dhall

-- `repo`: url for the git repo
-- `dependencies`: list of dependency names
-- `version`: version identifier for the benefit of humans
-- `rev`: git revision
-- `sha256`: hash of the repo contents (without .git) at the given revision
--
-- NOTE: it's annoying that we have to duplicate `dependencies` here and in the
-- package configuration, but doing so makes the install process simpler and faster.
-- So it's worth it.

{ repo : Text
, dependencies : List Text
, version : Text
, rev : Text
, sha256 : Text
}

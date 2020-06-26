#!/usr/bin/env python3

import json
import subprocess
import sys

def dhall_to_json(file, *args):
    with open(file, "r") as handle:
       dhall = handle.read()

    completed_process = subprocess.run(
        ["dhall-to-json", *args],
        input=dhall.encode("utf-8"),
        stdout=subprocess.PIPE,
        check=True
    )
    return json.loads(completed_process.stdout)

def main(argv=()):
    package_set = {}
    map_items = dhall_to_json("packages.dhall", "--no-maps")
    for map_item in map_items:
        key, value = map_item["mapKey"], map_item["mapValue"]
        if key in package_set:
            sys.exit(f"duplicate definitions of package \"{key}\"")
        package_set[key] = value
    print(json.dumps(package_set, indent=2, sort_keys=True))

if __name__ == '__main__':
    main(argv=sys.argv[1:])

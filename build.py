#!/usr/bin/env python3

import json
import subprocess
import sys

def dhall_to_json(file, *args):
    with open(file, "r") as handle:
       dhall = handle.read()

    try:
        completed_process = subprocess.run(
            ["dhall-to-json", *args],
            input=dhall.encode("utf-8"),
            stdout=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError:
        # Don't print stack trace
        sys.exit(1)

    return json.loads(completed_process.stdout)

def lint(package_set):
    errors = []
    for name, package in package_set.items():
        for dep in package["dependencies"]:
            if not dep in package_set:
                errors.append(f"\"{name}\" depends on \"{dep}\", but \"{dep}\" is missing")

    if len(errors) > 0:
        print("Linting failed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        sys.exit(1)

def main(argv=()):
    package_set = {}
    map_items = dhall_to_json("packages.dhall", "--no-maps")
    for map_item in map_items:
        key, value = map_item["mapKey"], map_item["mapValue"]
        if key in package_set:
            sys.exit(f"duplicate definitions of package \"{key}\"")
        package_set[key] = value
    lint(package_set)
    print(json.dumps(package_set, indent=2, sort_keys=True))

if __name__ == '__main__':
    main(argv=sys.argv[1:])

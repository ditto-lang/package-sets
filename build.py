#!/usr/bin/env python3

import json
import os
import subprocess
import sys

def dhall_to_json(dhall_expr, *args):
    try:
        completed_process = subprocess.run(
            ["dhall-to-json", *args],
            input=dhall_expr.encode("utf-8"),
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

def make_dhall_expr():
    dhall_files = []
    for root, _, files in os.walk("./src"):
        dhall_files.extend(os.path.join(root, file) for file in files if file != "Package.dhall")
    value = " # ".join(f"toMap {dhall_file}" for dhall_file in dhall_files)
    type = "List { mapKey : Text, mapValue : ./src/Package.dhall }"
    return f"{value} : {type}"

def main(argv=()):
    package_set = {}
    dhall = make_dhall_expr()
    map_items = dhall_to_json(dhall, "--no-maps")
    for map_item in map_items:
        key, value = map_item["mapKey"], map_item["mapValue"]
        if key in package_set:
            sys.exit(f"duplicate definitions of package \"{key}\"")
        package_set[key] = value
    lint(package_set)
    print(json.dumps(package_set, indent=2, sort_keys=True))

if __name__ == '__main__':
    main(argv=sys.argv[1:])

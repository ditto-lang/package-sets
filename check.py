#!/usr/bin/env python3

import sys
import asyncio
import json
import subprocess

check = "✔"
cross = "✘"

def print_err(*args, **kwargs):
    """
    Helper function to print to stderr.
    """
    print(*args, file=sys.stderr, **kwargs)

def hash_path(path):
    """
    Returns the sha256 hash of the given file path.
    """
    try:
        process = subprocess.run(
            ["nix-hash", "--type", "sha256", "--base32", path],
            stdout=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError:
        # Don't print stack trace
        sys.exit(1)

    return process.stdout.decode("utf-8").strip()

async def git_ping(repo):
    """
    Check whether a git repository exists at the given url.
    """
    process = await asyncio.create_subprocess_exec(
        "git", "ls-remote", repo, "CHECK_GIT_REMOTE_URL_REACHABILITY",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )

    # Wait for it to finish
    await process.communicate()

    return process.returncode == 0

async def git_hash(repo, rev):
    """
    Returns the sha256 hash of a repo at the given url.
    """
    process = await asyncio.create_subprocess_exec(
        "nix-prefetch-git", repo, rev,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )

    # Wait for it to finish
    stdout, _stderr = await process.communicate()
    if process.returncode != 0:
        sys.exit("nix-prefetch-git failed")

    return json.loads(stdout)["sha256"]


def check_packages_hash():
    print("Checking packages.sha256...")

    with open("packages.sha256") as f:
        want = f.readline().strip()

    got = hash_path("packages.json")
    if want != got:
        print_err(f"hashes don't match: got {got}: wanted {want}")
        sys.exit(1)

    print(f"{check} Hashes match")

async def check_repos_exist(packages):
    print("Checking all repositories exist...")

    async def check_exists(name, details):
        exists = await git_ping(details["repo"])
        return name, exists

    coroutines = [check_exists(name, details) for name, details in packages.items()]
    results = await asyncio.gather(*coroutines)

    missing = list(filter(lambda result: not result[1], results))
    if len(missing) != 0:
        for name, _ in missing:
            print_err(f"{cross} {name} is missing")
        sys.exit(1)

    for name, _ in results:
        print(f"{check} {name}")

async def check_repo_hashes(packages):
    print("Checking repositories hashes...")

    async def check_hash(name, details):
        want = details["sha256"]
        got = await git_hash(details["repo"], details["rev"])
        matches = want == got
        return name, matches, (want, got) if not matches else None

    coroutines = [check_hash(name, details) for name, details in packages.items()]
    results = await asyncio.gather(*coroutines)

    dodgey = list(filter(lambda result: not result[1], results))
    if len(dodgey) != 0:
        for name, _, (want, got) in dodgey:
            print_err(f"{cross} {name} hash doesn't match: got {got}: wanted {want}")
        sys.exit(1)

    for name, _, _ in results:
        print(f"{check} {name}")


async def main(argv=()):
    check_packages_hash()

    with open("packages.json") as f:
        packages = json.load(f)

    # First check that all the listed repositories actually exist.
    # Do this before checking hashes because it's cheaper and better
    # to fail fast here.
    await check_repos_exist(packages)
    await check_repo_hashes(packages)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(argv=sys.argv[1:]))

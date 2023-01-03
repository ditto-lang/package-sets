#!/usr/bin/env node

const crypto = require("node:crypto");

function makeGitHubPackageEntry({ name, owner, repo, revision, sha256 }) {
  return `[${name}]
github = { owner = "${owner}", repo = "${repo}" }
revision = "${revision}"
sha256 = "${sha256}"`;
}

async function fetchGitHubPackageEntry({
  owner,
  repo,
  name = repo,
  branch = "main",
}) {
  const commitsResponse = await fetch(
    `https://api.github.com/repos/${owner}/${repo}/commits/${branch}`
  );
  const { sha: revision } = await commitsResponse.json();
  const zipResponse = await fetch(
    `https://github.com/${owner}/${repo}/archive/${revision}.zip`
  );
  const zip = await zipResponse.arrayBuffer();
  const hashSum = crypto.createHash("sha256");
  hashSum.update(Buffer.from(zip));
  const sha256 = hashSum.digest("hex");
  return [
    name,
    makeGitHubPackageEntry({ name, owner, repo, revision, sha256 }),
  ];
}

async function main() {
  const entries = await Promise.all([
    fetchGitHubPackageEntry({
      owner: "ditto-lang",
      repo: "std",
    }),
    fetchGitHubPackageEntry({
      owner: "ditto-lang",
      repo: "js-ref",
    }),
    fetchGitHubPackageEntry({
      owner: "ditto-lang",
      repo: "js-unknown",
    }),
    fetchGitHubPackageEntry({
      owner: "ditto-lang",
      repo: "js-exception",
    }),
  ]);
  entries.sort(([name, _], [otherName, __]) => name.localeCompare(otherName));
  for (const [_, entry] of entries) {
    console.log(entry);
    console.log("");
  }
}

main();

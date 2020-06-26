#!/usr/bin/env node

const packages = require("./packages.json");

let exitCode = 0;
for ([name, pkg] of Object.entries(packages)) {
  for (dep of Object.values(pkg.dependencies)) {
    if (!(dep in packages)) {
      console.error(`Missing "${dep}" (dependency of "${name}")`);
      if (exitCode === 0) {
        exitCode = 1;
      }
    }
  }
}

process.exit(exitCode);

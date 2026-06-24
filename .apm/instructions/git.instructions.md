---
description: "How to use git"
applyTo: "**"
---

THESE ARE CRITICAL INSTRUCTIONS WHEN WORKING WITH GIT.

## Remotes

- Always run `git remote -v` before pushing, rebasing, or comparing branches.
- Identify which remote belongs to the user and which belong to other people. Never push to a remote that is not the user's own fork without explicit confirmation.
- Check the remote name carefully before every `git push` — remote names can be misleading (e.g., a person's first name mapping to a different GitHub user).

## Pushing

- Only push to the user's own fork (typically `origin`, but VERIFY). Never push directly to another person's branch or remote.

## Rebasing and comparing against main

- User forks are often out of date. Do not assume `origin/main` is current.
- Use the upstream remote (e.g., `upstream/main` or the authoritative org remote) as the source of truth for main.
- When diffing or rebasing, use `git merge-base` to find the correct common ancestor rather than assuming a branch tip is current.

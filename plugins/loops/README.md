# loops

Autonomous loops that shepherd work to completion.

See the [main installation guide](../../README.md#installation) for Claude
Code, Codex, and standalone Agent Skills setup.

## Skills

- **pr-loop**: Shepherd a GitHub PR to a mergeable state — merge the base branch when behind, fix CI failures, address review comments from trusted reviewers and authorized bots, resolve threads, and loop until green or idle.

## Usage

Invoke the `pr-loop` skill with a full GitHub pull request URL, or ask it to
detect the open pull request for the current branch. The skill defines its own
termination condition: all CI green, all review comments resolved, the branch
up to date with its base, and 30 minutes idle — or a hard cap of 25 iterations.

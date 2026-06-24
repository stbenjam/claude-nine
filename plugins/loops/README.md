# loops

Autonomous loops that shepherd work to completion.

## Skills

- **pr-loop**: Shepherd a GitHub PR to a mergeable state — merge the base branch when behind, fix CI failures, address review comments from trusted reviewers and authorized bots, resolve threads, and loop until green or idle.

## Usage

Run every loop skill under the `/loop` command — prefix the skill invocation with `/loop`:

```
/loop /pr-loop https://github.com/org/repo/pull/42
```

`/loop` drives the repeated iterations; the skill itself defines when to stop. Each skill specifies its own termination condition (for `pr-loop`: all CI green, all review comments resolved, the PR up to date with its base, and 30 minutes idle — or a hard cap of 25 iterations). You don't pass an interval — the skill self-paces and ends the loop when its termination condition is met.

## Installation

```
/plugin install loops@claude-nine
```

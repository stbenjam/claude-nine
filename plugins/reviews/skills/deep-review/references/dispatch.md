# Phase 2 — Specialist dispatch details

**Sub-agents and serial reviewers MUST NOT modify any files, and
MUST NOT run remote-write git commands** (`git push`, force-push
variants, push to protected branches, or pushes to any remote).
They are read-only reviewers.

## Findings JSON schema

Append this schema to each specialist prompt:

```json
[
  {
    "file": "src/example.py",
    "line": 42,
    "severity": "BLOCKING",
    "title": "Short title",
    "body": "Description of the issue",
    "suggestion": "Recommended action or null",
    "reproducer_needed": true
  }
]
```

**Severity values**: `BLOCKING` | `SUGGESTION` | `NOTE`

If no issues found, return an empty array and state what was checked.

## Prompt path resolution

Resolve specialist prompts from the skill directory (repository
root relative):
`plugins/reviews/skills/deep-review/references/specialists/{specialist}.md`.
Prefer that absolute-from-repo-root path over a bare
`references/specialists/...` path — agents may not share the
skill's working directory.

## Parallel mode

Launch **all enabled specialist sub-agents in a single message** so
they run concurrently, using the Agent tool with
`run_in_background: true`.

Each sub-agent gets:
- The prompt: "You are a {specialist}. Read
  `plugins/reviews/skills/deep-review/references/specialists/{specialist}.md`
  for your review instructions."
- The merge base ref
- The PR number or branch name being reviewed
- Any prior review findings (if detected in Step 1.4)
- The findings JSON schema above

Sub-agents have full read access to the locally checked-out
codebase. They explore the code on their own — read files, grep,
run git commands, etc. Apply the read-only contract at the top of
this file.

Use `subagent_type: "general-purpose"`. Do NOT set the `model`
parameter.

## Serial mode (`--serial`)

Run all enabled specialists **inline in the main agent**, one after
another. Do **not** launch sub-agents for specialist dispatch.
(Phase 4 reproducer sub-agents are still launched even in serial
mode — the no-sub-agent constraint applies only to specialists.)

Then for each specialist in roster order, state the specialist name
as a heading, read
`plugins/reviews/skills/deep-review/references/specialists/{specialist}.md`
for review instructions, review through that lens, and produce
findings in the same JSON format. Context from earlier specialists'
file reads and findings carries over automatically.

**Do NOT modify any files, and do NOT push to any remote.** Serial
mode is read-only, same as parallel.

## External reviewers

If external reviewers were requested, launch them in parallel with
(or before, in serial mode) the specialist dispatch.

**CodeRabbit** (`--coderabbit`):
```bash
timeout 300 coderabbit review --agent --base "$MERGE_BASE" 2>&1
```

**Codex** (`--codex`):
```bash
timeout 300 codex review 2>&1
```

External reviewer output is captured as-is and included in the
arbiter's synthesis input as a peer specialist. If a command fails
(non-zero exit, tool not found, timeout), record the error and
continue — never block the panel on an external tool failure.

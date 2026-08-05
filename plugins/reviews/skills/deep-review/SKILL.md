---
name: "deep-review"
description: "Use when a deeper level of code review is requested. Multi-agent panel code review with specialist reviewers and forced runtime reproducers for all BLOCKING bug findings. Optionally posts to GitHub/GitLab as a PENDING review."
argument-hint: "[--serial] [--comment] [--coderabbit] [--codex] [-reviewer,...] [pr-url-or-number]"
---

# Deep Review — Multi-Specialist Panel Review with Reproducers

Review a branch's changes with parallel specialist subagent reviewers,
each examining the code through a different lens. Verify every bug
finding with a runtime reproducer. Optionally post to GitHub/GitLab
as a PENDING review.

No PR/MR is required — the review works on any branch with commits
ahead of its base.

**Two execution modes:**

- **Parallel (default)**: Each specialist runs as a dedicated sub-agent
  concurrently. Thorough but expensive — each sub-agent independently
  derives its own view of the codebase.
- **Serial (`--serial`)**: All specialists run inline in the main agent,
  one after another. Significantly cheaper because the codebase context
  is derived once and shared across all specialists. Trade-off: reviews
  run sequentially, and later specialists can see prior specialists'
  findings (which may bias their analysis).

## Arguments

Invoke `deep-review` with optional flags and a PR URL or number.

| Argument | Description |
|----------|-------------|
| `--serial` | Run all specialists inline instead of as parallel sub-agents |
| `--comment` | Post the verdict as a PR comment after review. Requires a PR identifier |
| `--coderabbit` | Include CodeRabbit as an external reviewer |
| `--codex` | Include OpenAI Codex as an external reviewer |
| `-reviewer` | Exclude a specialist (e.g., `-writer,-qa`). All enabled by default |
| pr identifier | GitHub/GitLab PR URL or bare PR number. Optional |

Examples:

- `deep-review` — all reviewers, review current branch
- `deep-review --serial` — cheaper serial mode
- `deep-review -qa,-writer` — skip QA and Technical Writer
- `deep-review --comment 42` — review PR #42, post verdict as comment
- `deep-review --coderabbit https://github.com/org/repo/pull/42`
- `deep-review https://gitlab.com/org/repo/-/merge_requests/7`

## Specialist Panel

All are enabled unless excluded with `-`:

| Specialist | Lens | Reproducer? |
|------------|------|-------------|
| **bugs** | Functional bugs: missing calls, wrong logic, unhandled edge cases | Yes — mandatory |
| **adversarial** | Break the code: bad inputs, race conditions, boundary values | Yes — mandatory |
| **security** | Vulnerabilities, credential handling, dependency trust, supply chain integrity | When claiming a concrete exploit |
| **architecture** | Structural patterns, SOLID, cross-file impact, module boundaries | No |
| **consistency** | Duplicate helpers, convention drift, style match with existing code | No |
| **qa** | Test coverage gaps, missing edge-case tests, concrete test suggestions | No |
| **writer** | Documentation accuracy, staleness, consistency with code changes | No |

### Routing Topology

```text
  bugs  adversarial  security  architecture  consistency  qa  writer
    \_______|__________|__________|___________|___________|____|
                                 |
                           [reproduce]  ← bug/security findings only
                                 |
                                 v
                           panel-arbiter
                         (final call)
```

- Specialists raise findings independently — no implicit consensus.
  Each runs as a separate sub-agent and cannot see the others' output.
- Reproducer agents verify bug/security claims before arbitration.
- Panel Arbiter synthesizes after all specialists and reproducers complete.

## Procedure

### Phase 1 — Setup

#### Step 1.1: Parse arguments

Split the argument string on whitespace. Flags (`--serial`,
`--comment`, `--coderabbit`, `--codex`) set modes. Tokens like
`-writer,-qa` exclude those specialists (validate against the
roster; unknown names warned and ignored). A PR URL or bare
integer is the PR identifier (for bare integers, detect platform
from git remote). Error if: all specialists excluded, `--comment`
without PR identifier, or multiple PR identifiers.

#### Step 1.2: Check out the PR and determine base ref

Follow [references/setup.md](references/setup.md): parse the PR/MR
URL into platform/project/id (never pass a raw URL as `$MR_IID`),
check out with quoted args, discover remotes via `git remote -v`,
and compute `$MERGE_BASE`.

**If a PR/MR was specified and checkout/metadata fails, error and
exit — never fall back to reviewing the current local branch.**

#### Step 1.3: Verify there are changes

Check that the branch has commits ahead of the base. If there are
no changes, stop: "No changes found between HEAD and the base
branch."

If a PR/MR exists, also fetch its description for context.

#### Step 1.4: Detect prior reviews (PR only)

Follow the GitHub/GitLab commands in
[references/setup.md](references/setup.md). Pass prior
`Generated by /deep-review` findings to specialists and the
arbiter so resolved items and regressions are handled.

### Phase 2 — Dispatch Specialists

Each specialist prompt lives under
[references/specialists/](references/specialists/). Dispatch rules,
JSON schema, parallel/serial modes, and external reviewers are in
[references/dispatch.md](references/dispatch.md).

| Specialist | Prompt |
|------------|--------|
| bugs | [references/specialists/bugs.md](references/specialists/bugs.md) |
| adversarial | [references/specialists/adversarial.md](references/specialists/adversarial.md) |
| security | [references/specialists/security.md](references/specialists/security.md) |
| architecture | [references/specialists/architecture.md](references/specialists/architecture.md) |
| consistency | [references/specialists/consistency.md](references/specialists/consistency.md) |
| qa | [references/specialists/qa.md](references/specialists/qa.md) |
| writer | [references/specialists/writer.md](references/specialists/writer.md) |

### Phase 3 — Completeness Gate

After all sub-agents and external reviewers return, verify all
enabled specialists produced findings (or an explicit "no issues"
with what was checked). A valid empty JSON array `[]` with an
explanation of what was checked is success — do **not** retry it.
If any specialist returned an error or a missing/malformed result,
re-dispatch it **once**. If the retry also fails, record the
failure and proceed.

External reviewer failures are non-blocking — note the error and
continue.

### Phase 4 — Reproduce

For every BLOCKING finding with `reproducer_needed: true`, launch
a reproducer subagent (up to 5 in parallel). See
[references/reproducer-prompt.md](references/reproducer-prompt.md)
for the prompt template and result processing rules.

### Phase 5 — Panel Arbiter

Perform synthesis directly in the main agent (not a sub-agent).

1. **Deduplicate** — merge duplicates, keep strongest reproducer
2. **Filter noise** — remove false positives, style nitpicks,
   speculative findings, and issues already addressed in the branch
3. **Resolve conflicts** — corroboration strengthens; adversarial
   concerns are blocking unless concretely refuted
4. **Assign disposition** — APPROVE (no BLOCKING), REQUEST_CHANGES
   (BLOCKING findings), or NEEDS_DISCUSSION (needs author input).
   Biases: security over ergonomics, consistency over elegance,
   reproduced bugs are always BLOCKING, do not manufacture findings
5. **Prioritize** — reproduced security bugs > reproduced functional
   bugs > unreproduced > architecture > style/docs
6. **Emit verdict** — use collapsible `<details>` blocks for
   specialist findings (each specialist collapsed with severity
   counts). Sections: Disposition, Specialist Findings, Panel
   Synthesis, Required Actions, Optional Follow-ups, Stats.
   Footer: `<sub>Generated by the deep-review skill</sub>`.
   Include collapsible reproducer details for confirmed BLOCKING bugs.

### Phase 6 — Post to PR (Optional)

When `--comment` was passed, follow
[references/pr-posting.md](references/pr-posting.md) to post the
verdict to the PR and optionally create inline review comments.
`$OWNER`, `$REPO`, `$PR_NUMBER` / `$PROJECT`, `$MR_IID` must already
be set from Step 1.2.

## Quality Gates

A change passes when: no unresolved functional bugs, no unrefuted
adversarial scenarios, no unmitigated vulnerabilities or supply
chain risks, sound architecture, no duplicate helpers, adequate
test coverage, documentation consistent with changes, and the
panel arbiter has ratified the disposition.

## Error Handling

- **`gh`/`glab` not authenticated**: Review can still run on a
  locally checked-out branch.
- **No PR exists**: Skip Phase 6; the verdict is the deliverable.
- **External tool not installed/timeout**: Skip, warn, continue.
- **Subagent timeout**: Report which specialist timed out, continue.
- **No changes**: Stop — "No changes found."
- **Inaccessible PR/MR**: Stop with an error; do not review another
  branch.
- **Review creation fails (422)**: Delete only comment/review IDs
  created by the current attempt, then retry. Never delete existing
  reviewer comments from other runs or authors.

## Guardrails

- Never submit a PR review without explicit user confirmation.
- Omit `"event"` from the initial review creation payload so the
  review stays PENDING.
- **Review agents MUST NOT modify any files in the working tree.**
- **Never `git push`, force-push, or push to protected branches
  (`main`/`master`) or any other remote.** Discover remotes with
  `git remote -v` when needed for reads.
- Reproducers run in /tmp. Do not push reproducer files.
- Do not run destructive operations in reproducers.
- Cap at 30 inline PR comments. Overflow goes to the review body.

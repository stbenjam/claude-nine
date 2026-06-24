---
match: ["openshift*/*", "kubernetes*/*"]
---

# OpenShift / Kubernetes Project Overrides

## CI wait strategy — long-running e2e jobs

Prow-based CI in these repos includes e2e jobs (`e2e-*` and similar)
that routinely take 1-3 hours. Polling every few minutes wastes
tokens and achieves nothing.

**Override Step 3.5 (pending CI):** when pending checks are Prow
e2e jobs, do not poll on the fast 2-3 minute cycle. Instead, use
the scheduling rule below.

**Override Step 5.3 (backoff schedule):** schedule the next
iteration for **1 hour later** via `CronCreate` — but only after
all review feedback has been addressed. While there are still
unresolved actionable comments, keep the default 10-minute loop
so feedback is addressed quickly. Switch to the hourly interval
once the only thing left to wait on is CI.

## Flaky test handling

Before concluding a CI failure is caused by your PR, use the
`ci` plugin skills to analyze the failure:

1. Use `/ci:analyze-prow-job-test-failure` to investigate the
   failing test — this checks test history, known flakes, and
   whether the failure correlates with your changes
2. Use `/ci:fetch-test-report` to check the test's pass rate
   across recent runs
3. If the test has a low pass rate (<95%) and the failure does
   not correlate with your changes, it is likely flaky —
   retrigger with `/retest` as a PR comment
4. If analysis reveals a **systemic issue** across OpenShift
   (not just this PR) that you could fix, notify the user via
   `notify_user` and ask for permission before attempting a fix

Do not skip investigation — always analyze before retriggering.

## Prow bot commands

You may use these Prow commands as PR comments:

- `/retest` — retrigger failed optional tests
- `/test <job-name>` — trigger a specific test job

**Never use:**

- `/override` — never override failing checks
- `/lgtm` or `/approve` — never self-approve
- Any command that bypasses CI or review requirements

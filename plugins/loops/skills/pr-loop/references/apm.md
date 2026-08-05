---
match: ["microsoft/apm"]
---

# APM Project Overrides

## Phase 2 — Always keep PR up to date

Override the default "merge base branch once" behavior. APM requires
PRs to be current with the base branch before merging.

**On every loop iteration**, re-run Phase 2 (Steps 2.1 and 2.2) to
check whether the PR is behind the base branch and merge if needed.

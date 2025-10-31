---
description: Approve pending GitHub Actions workflows and add /ok-to-test comments to PRs
argument-hint: <repo-owner/repo-name>
---

## Name
pr-automation:approve-workflows

## Synopsis
```
/pr-automation:approve-workflows <repo-owner/repo-name>
```

## Description
The `pr-automation:approve-workflows` command automates the process of reviewing and approving pending pull requests from external contributors. It performs two key tasks:

1. **Approves pending GitHub Actions workflows**: Finds all workflow runs that require approval (those with "action_required" conclusion) and approves them so they can execute.

2. **Adds /ok-to-test comments**: Identifies all open PRs with the "needs-ok-to-test" label and adds a `/ok-to-test` comment to trigger CI testing.

This command is particularly useful for repository maintainers who need to regularly process contributions from external collaborators.

## Implementation

Use the `pr-automation:approve-workflows` skill to implement this command. The skill is located at:
`~/.claude/plugins/pr-automation/skills/approve-workflows/SKILL.md`

Invoke the skill and pass the repository name as context.

## Return Value

- **Format**: Summary of actions taken
  - List of workflow runs approved
  - List of PRs that received /ok-to-test comments
  - Any errors or issues encountered

## Examples

1. **Approve workflows for a specific repository**:
   ```
   /pr-automation:approve-workflows openshift-eng/ai-helpers
   ```

2. **Use with current repository** (if in a git repo):
   ```
   /pr-automation:approve-workflows
   ```

## Arguments

- `$1` (optional): Repository in `owner/repo` format. If not provided, will attempt to detect from current directory's git remote.

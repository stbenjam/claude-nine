# PR Automation Plugin

Automates common pull request review tasks for repository maintainers, including approving GitHub Actions workflows and adding `/ok-to-test` comments to PRs from external contributors.

## Overview

This plugin helps maintainers efficiently process contributions from external collaborators by automating two key workflows:

1. **GitHub Actions Approval**: Automatically approves pending workflow runs that require manual approval
2. **Prow CI Testing**: Adds `/ok-to-test` comments to PRs labeled with "needs-ok-to-test"

## Installation

This is a personal plugin located at `~/.claude/plugins/pr-automation`.

To use it, ensure Claude Code can access your personal plugins directory.

## Commands

### `/pr-automation:approve-workflows`

Approve pending GitHub Actions workflows and add `/ok-to-test` comments to PRs that need testing.

**Usage:**
```
/pr-automation:approve-workflows <repo-owner/repo-name>
```

**Arguments:**
- `repo-owner/repo-name` (optional): Repository to process. If not provided, detects from current directory's git remote.

**Example:**
```
/pr-automation:approve-workflows openshift-eng/ai-helpers
```

**What it does:**
1. Finds all open PRs with the "needs-ok-to-test" label
2. Comments `/ok-to-test` on each PR to trigger CI testing
3. Finds all GitHub Actions workflow runs waiting for approval
4. Approves each pending workflow run
5. Reports timed-out workflows (informational only)

## Prerequisites

- **GitHub CLI (`gh`)**: Must be installed and authenticated
  - Install: https://cli.github.com/
  - Authenticate: `gh auth login`
- **Repository Access**: Must have write permissions to approve workflows
- **Git Repository**: When not specifying a repo, must be run from within a git repository

## Use Cases

- **Daily PR Review**: Quickly approve all pending workflows and enable CI for new external contributions
- **After Vacations**: Catch up on backlog of external contributor PRs requiring approval
- **Bulk Processing**: Handle multiple PRs at once instead of clicking through the GitHub UI
- **CI/CD Integration**: Automate approvals as part of a larger workflow

## How It Works

### GitHub Actions Workflows

External contributor PRs require manual approval before GitHub Actions workflows can run (security feature). This plugin:

1. Queries the GitHub Actions API for workflow runs with `status == "waiting"`
2. Calls the approval API endpoint for each waiting run
3. Reports runs with `conclusion == "action_required"` (already timed out)

### Prow CI Testing

Repositories using Prow CI require an `/ok-to-test` comment from a repo member before tests run. This plugin:

1. Queries all open PRs for the "needs-ok-to-test" label
2. Adds a comment with `/ok-to-test` to each PR
3. This triggers Prow to run CI jobs for that PR

## Output

The command provides a structured summary:

```
# PR Workflow Approval Summary

## PRs Marked as /ok-to-test (3)
- PR #116: CLID-473: subagent to generate weekly reports
- PR #105: Add claude interactive google service account creation
- PR #76: an olmv1 claude plugin for managing clusterextensions

## GitHub Actions Workflows Approved (2)
- Run 18977369749: Lint Plugins (branch: add_qa_assignee_query) ✓
- Run 18979766265: Lint Plugins (branch: gh2jira) ✓

## Timed Out Workflows (informational) (5)
These workflows timed out waiting for approval. New commits will trigger new runs.
- Run 18968492733: Lint Plugins (branch: raise_pr_debug_cluster)
...

## Status
✓ All pending approvals completed successfully
```

## Limitations

- Cannot retroactively approve timed-out workflows (must wait for new commits)
- Requires write access to the repository
- Limited to 100 PRs per query (GitHub API pagination)
- Assumes "needs-ok-to-test" label name (hardcoded)

## Security Considerations

This plugin approves workflows from external contributors. Maintainers should:

1. Review PR code before running this command
2. Ensure external contributions are safe to test
3. Verify PRs don't contain malicious workflow modifications
4. Consider using this only for trusted contributors or after manual review

## Troubleshooting

**Issue**: "Not Found (HTTP 404)" when approving workflows
- **Cause**: Workflow run was deleted or doesn't exist
- **Solution**: Ignore, the run is no longer relevant

**Issue**: "Forbidden (HTTP 403)" when approving workflows
- **Cause**: Insufficient permissions
- **Solution**: Ensure you have write access to the repository

**Issue**: No PRs or workflows found
- **Cause**: All approvals are up to date
- **Solution**: Nothing to do, all clear!

## Author

Created by stbenjam for personal use in managing OpenShift repositories.

## Version

0.0.1 - Initial release

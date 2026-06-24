---
name: review-queue
description: Generate a report of GitHub pull requests that need review attention. Use when the user asks about their PR review queue, which PRs need reviewing, the status of their open PRs across repositories, or invokes /git:review-queue.
user-invocable: true
---

# Review Queue

Generate a comprehensive report of pull requests that need attention. This skill operates in two modes: analyzing your own PRs across repositories, or providing a detailed breakdown of all open PRs in a specific repository. It integrates with GitHub's tide status to identify merge blockers, categorizes PRs by review state, and helps prioritize review work.

## Invocation

```
/git:review-queue [org/repo]
```

- `org/repo` (optional): Repository to analyze in format `owner/repo`. If omitted, reports your PRs across all repositories.

**Key capabilities:**
- Identify your PRs awaiting reviews, approvals, or blocked by CI
- Find fresh PRs in a repository that haven't been reviewed yet
- Track PRs you've previously commented on
- Filter out blocked PRs (merge conflicts, failing CI)
- Parse tide status to understand merge requirements
- Categorize PRs by review state and priority

This skill is particularly useful for:
- **Maintainers**: Get an overview of repository review queue
- **Contributors**: Track status of your own PRs across multiple repos
- **Reviewers**: Find PRs that need your attention based on your previous involvement

## Implementation

### Step 1: Determine Operation Mode

**Check for repository argument:**
```bash
if [ -n "$1" ]; then
  MODE="repository"
  TARGET_REPO="$1"
else
  MODE="my-prs"
fi
```

**Get current user:**
```bash
CURRENT_USER=$(gh api user --jq .login)
```

### Step 2: Fetch Pull Requests

#### Mode 1: My PRs

**Fetch PRs authored by current user across all repositories:**
```bash
gh search prs --author="$CURRENT_USER" --state=open --json number,title,repository,labels,createdAt,updatedAt,isDraft,reviewDecision,url --limit 100
```

**Filter and deduplicate:** Process JSON output to get unique PRs

#### Mode 2: Repository Mode

**Fetch all open PRs for the specified repository:**
```bash
gh pr list --repo "$TARGET_REPO" --state=open --limit 100 \
  --json number,title,author,labels,createdAt,updatedAt,isDraft,reviewDecision,mergeable,headRefOid,url,additions,deletions,changedFiles
```

### Step 3: Enrich PR Data

For each PR, gather additional context:

**1. Get tide status from status checks:**
```bash
# Extract commit SHA (headRefOid from PR data)
gh api "repos/$REPO_OWNER/$REPO_NAME/commits/$SHA/status" \
  --jq '.statuses[] | select(.context == "tide") | {state, description, target_url}'
```

**Tide status parsing:**
- State: `success` (ready to merge), `pending` (waiting), `failure` (blocked)
- Description contains: missing labels, failing jobs, merge conflicts
- Examples:
  - "Needs lgtm label and approved label"
  - "Job e2e-aws failed"
  - "PR has a merge conflict"

**2. Get review information:**
```bash
gh api "repos/$REPO_OWNER/$REPO_NAME/pulls/$PR_NUMBER/reviews" \
  --jq '[.[] | {user: .user.login, state, submitted_at}]'
```

**Review states:**
- `APPROVED`: Reviewer approved
- `CHANGES_REQUESTED`: Reviewer requested changes
- `COMMENTED`: Reviewer commented without approval

**3. Check if current user has commented (repository mode only):**
```bash
# Get all comments (issue comments + review comments)
gh api "repos/$REPO_OWNER/$REPO_NAME/issues/$PR_NUMBER/comments" \
  --jq '[.[] | .user.login] | unique'

gh api "repos/$REPO_OWNER/$REPO_NAME/pulls/$PR_NUMBER/comments" \
  --jq '[.[] | .user.login] | unique'
```

Check if `$CURRENT_USER` appears in either list.

**4. Get CI status summary:**
```bash
gh pr checks $PR_NUMBER --repo "$TARGET_REPO" --json name,state,conclusion
```

Count passing/failing/pending checks.

### Step 4: Categorize PRs

#### For "My PRs" Mode:

**Category 1: Awaiting Reviews**
- Criteria: No `approved` or `lgtm` labels
- No reviews with state `APPROVED`
- Not in draft state

**Category 2: Requested Changes**
- Criteria: Has reviews with state `CHANGES_REQUESTED`
- No subsequent commits after the change request

**Category 3: Blocked by CI**
- Criteria: Tide status shows failing required jobs
- OR: Required status checks are failing

**Category 4: Ready to Merge**
- Criteria: Has `approved` and `lgtm` labels
- Tide status is `success`
- All required checks passing

**Category 5: Awaiting Tide**
- Criteria: Has approvals but tide status is `pending`
- Typically waiting for merge queue

#### For "Repository" Mode:

**Category 1: PRs I've Reviewed**
- Criteria: Current user has comments or reviews on the PR
- Sort by last activity date (most recent first)

**Category 2: Fresh PRs - No Reviews Yet**
- Criteria: No comments except from:
  - PR author
  - Bot accounts (openshift-ci-robot, openshift-merge-robot, k8s-ci-robot, etc.)
- No reviews from any user
- Sort by age (oldest first for priority)

**Category 3: In Discussion**
- Criteria: Has comments/reviews from humans (not just bots/author)
- Does NOT have `approved` + `lgtm` labels
- Not in "Fresh PRs" category

**Category 4: Ready for Additional Review**
- Criteria: Has some approvals but may need more
- Tide shows additional labels needed
- Sort by age

**Category 5: Excluded from Review**
- PRs with merge conflicts (`mergeable: "CONFLICTING"`)
- Draft PRs (unless in "My PRs" mode)
- PRs with failing required CI (based on tide status)
- Show count summary only, don't list details

### Step 5: Generate Report

**Report structure:**

```markdown
# Review Queue Report
Repository: {org/repo} OR All Repositories
Generated: {timestamp}
Current User: @{username}

---

## My PRs Needing Attention ({count})

### Awaiting Reviews ({count})
{list PRs with metadata}

### Requested Changes ({count})
{list PRs with metadata}

### Blocked by CI ({count})
{list PRs with metadata}

### Ready to Merge ({count})
{list PRs with metadata}

---

## Repository: {org/repo} ({total} open PRs, {reviewable} needing review)

### PRs I've Reviewed ({count})
{list PRs with metadata}

### Fresh PRs - No Reviews Yet ({count})
{list PRs with metadata}

### In Discussion ({count})
{list PRs with metadata}

### Excluded from Review
- {count} with merge conflicts
- {count} drafts
- {count} with failing required CI
```

**PR metadata format:**
```markdown
- #{number} {title} (opened {X} days ago)
  Author: @{author}
  Tide: {tide_description}
  CI: {passing}/{total} checks passing
  Reviews: {approval_summary}
  Labels: {relevant_labels}
  Changes: +{additions}/-{deletions} across {files} files
  URL: {pr_url}
```

**Calculate PR age:**
```bash
# Use jq to calculate days since creation
echo "$PR_JSON" | jq -r '
  (.createdAt | fromdateiso8601) as $created |
  (now | floor) as $now |
  (($now - $created) / 86400 | floor) as $days |
  "\($days) days ago"
'
```

**Approval summary examples:**
- "2 approvals (@user1, @user2)"
- "1 approval, 1 change request (@user3)"
- "No reviews yet"

### Step 6: Add Interactive Options (Optional)

After displaying the report, optionally ask user:
```
Would you like to:
1. Open a specific PR in browser
2. Fetch a PR to address reviews (/utils:address-reviews)
3. Refresh the report
4. Exit
```

If user selects option 2, invoke the address-reviews command.

## Return Value

**Format:** Markdown report with categorized PR lists

**Content:**
- Summary statistics (total PRs, reviewable PRs, blocked PRs)
- Categorized PR lists with detailed metadata
- Actionable insights (which PRs need attention first)
- Tide status interpretation for each PR

**Example output:**

```markdown
# Review Queue Report
Repository: openshift/installer
Generated: 2025-10-31 14:23 UTC
Current User: @stbenjam

---

## My PRs Needing Attention (3)

### Awaiting Reviews (2)

- #5234 feat: add support for custom networking (opened 3 days ago)
  Author: @stbenjam
  Tide: Needs lgtm label and approved label
  CI: 5/6 checks passing (e2e-aws pending)
  Reviews: No reviews yet
  Labels: size/L
  Changes: +347/-123 across 8 files
  URL: https://github.com/openshift/installer/pull/5234

### Requested Changes (1)

- #5156 refactor: improve error handling in bootstrap (opened 5 days ago)
  Author: @stbenjam
  Tide: Needs lgtm label after addressing feedback
  CI: All 7 checks passing
  Reviews: 1 change request (@reviewer1, 2 days ago)
  Labels: size/M
  Changes: +156/-89 across 5 files
  URL: https://github.com/openshift/installer/pull/5156

---

## Repository: openshift/installer (28 open PRs, 15 needing review)

### Fresh PRs - No Reviews Yet (5)

- #5221 fix: prevent timeout errors during cluster creation (opened 4 days ago)
  Author: @contributor3
  Tide: Needs lgtm label and approved label
  CI: 7/8 checks passing (e2e-gcp pending)
  Reviews: No reviews yet
  Labels: size/M, bugfix
  Changes: +87/-34 across 4 files
  URL: https://github.com/openshift/installer/pull/5221

### Excluded from Review
- 3 PRs with merge conflicts
- 2 draft PRs
- 4 PRs with failing required CI
- 1 bot PR (renovate)

---

💡 Priority recommendations:
1. Review fresh PRs (5) - especially #5221 (4 days old)
2. Address change requests on your PR #5156
3. Follow up on PRs you've reviewed (#5167 has failing tests)
```

## Examples

All examples produce a report in the format shown under **Return Value** above. Each entry below lists the invocation and the distinguishing behavior to expect.

- **`/git:review-queue`** — My-PRs mode across all repositories. Groups your open PRs into Awaiting Reviews, Requested Changes, Blocked by CI, and Ready to Merge, and closes with a priority recommendation (oldest waiting PR / outstanding change requests first).
- **`/git:review-queue openshift/installer`** — Repository mode. Groups the repo's open PRs into PRs I've Reviewed, Fresh PRs (No Reviews Yet), and In Discussion, with an Excluded from Review summary (merge conflicts, drafts, failing required CI).
- **Repository with nothing to review** — when every open PR is a draft, has merge conflicts, or is awaiting CI, all categories are empty and the report ends with `✅ No PRs currently need review.`
- **Your PRs all in good state** — when no PR needs attention, My PRs Needing Attention is 0 and Ready to Merge lists approved / in-merge-queue PRs.
- **Large repository (>100 open PRs)** — only the 50 most recent are shown, prefixed with an `ℹ️` note suggesting `gh pr list` filters (`--label`, `--author "@me"`) to narrow the set.

## Notes

### Bot Account Detection

The following accounts are considered bots and their comments are excluded when determining "fresh PRs":
- `openshift-ci-robot`
- `openshift-merge-robot`
- `openshift-merge-bot`
- `k8s-ci-robot`
- `k8s-merge-robot`
- `dependabot[bot]`
- `renovate[bot]`
- Any account ending in `[bot]`

Exception: The PR author's own comments are always excluded regardless of account type.

### Tide Status Interpretation

Tide is Prow's merge automation system. Common tide status messages:

**Success states:**
- "Merge will happen soon" - In merge queue
- "Ready to merge" - Will merge on next tide cycle

**Pending states:**
- "Needs lgtm label" - Awaiting reviewer LGTM
- "Needs approved label" - Awaiting approver approval
- "Waiting for batch" - In merge pool, waiting turn

**Failure states:**
- "PR has a merge conflict" - Must resolve conflicts
- "Job {name} failed" - Required CI job failed
- "Missing required label" - Needs specific label to merge

### Performance Considerations

- For repositories with >100 PRs, only the 100 most recent are analyzed
- Batch API calls into a single GraphQL query (or paginated REST call) to avoid rate limits
- Results can be cached for 5-10 minutes for repeated queries
- Use `--json` output from `gh` CLI for efficient parsing

### GitHub Permissions

This skill requires:
- Read access to the repository
- GitHub CLI (`gh`) authenticated
- Access to GitHub Status API for tide information

### Caveats

- Tide status is specific to Prow-based CI systems (OpenShift, Kubernetes)
- For non-Prow repos, falls back to checking labels and review status
- Draft PRs are excluded in repository mode but shown in "My PRs" mode
- Bot PRs (renovate, dependabot) are excluded unless authored by you

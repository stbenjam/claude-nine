---
description: Generate a report of PRs needing reviews
argument-hint: [org/repo]
---

## Name
git:review-queue

## Synopsis
```
/git:review-queue [org/repo]
```

## Description
The `git:review-queue` command generates a comprehensive report of pull requests that need attention. It operates in two modes: analyzing your own PRs across repositories, or providing a detailed breakdown of all open PRs in a specific repository. The command integrates with GitHub's tide status to identify merge blockers, categorizes PRs by review state, and helps prioritize review work.

**Key capabilities:**
- Identify your PRs awaiting reviews, approvals, or blocked by CI
- Find fresh PRs in a repository that haven't been reviewed yet
- Track PRs you've previously commented on
- Filter out blocked PRs (merge conflicts, failing CI)
- Parse tide status to understand merge requirements
- Categorize PRs by review state and priority

This command is particularly useful for:
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

- #5189 fix: correct AWS region validation (opened 1 day ago)
  Author: @stbenjam
  Tide: Needs lgtm label, needs approved label
  CI: All 6 checks passing
  Reviews: No reviews yet
  Labels: size/S, bugfix
  Changes: +23/-15 across 2 files
  URL: https://github.com/openshift/installer/pull/5189

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

### PRs I've Reviewed (2)

- #5198 feat: support for additional Azure regions (opened 7 days ago)
  Author: @contributor1
  Your last comment: 3 days ago
  Tide: Needs approved label
  CI: All 8 checks passing
  Reviews: 1 lgtm (@stbenjam), awaiting approval
  Labels: size/M, azure
  Changes: +234/-67 across 12 files
  URL: https://github.com/openshift/installer/pull/5198

- #5167 fix: handle IPv6 configuration edge cases (opened 10 days ago)
  Author: @contributor2
  Your last comment: 5 days ago
  Tide: Needs lgtm label and approved label
  CI: 7/8 checks passing (unit-tests failing)
  Reviews: 2 comments (@stbenjam, @other-reviewer)
  Labels: size/L, networking
  Changes: +445/-178 across 15 files
  URL: https://github.com/openshift/installer/pull/5167

### Fresh PRs - No Reviews Yet (5)

- #5221 fix: prevent timeout errors during cluster creation (opened 4 days ago)
  Author: @contributor3
  Tide: Needs lgtm label and approved label
  CI: 7/8 checks passing (e2e-gcp pending)
  Reviews: No reviews yet
  Labels: size/M, bugfix
  Changes: +87/-34 across 4 files
  URL: https://github.com/openshift/installer/pull/5221

- #5215 feat: add retry logic for API calls (opened 5 days ago)
  Author: @contributor4
  Tide: Needs lgtm label and approved label, Job e2e-aws failed
  CI: 6/8 checks passing (2 jobs failing)
  Reviews: No reviews yet
  Labels: size/L
  Changes: +312/-156 across 9 files
  URL: https://github.com/openshift/installer/pull/5215

[... 3 more PRs ...]

### In Discussion (8)

- #5187 feat: improve logging throughout installer (opened 8 days ago)
  Author: @contributor5
  Tide: Needs approved label
  CI: All 8 checks passing
  Reviews: 1 lgtm (@reviewer2), 2 comments (@reviewer3, @reviewer4)
  Labels: size/XL, enhancement
  Changes: +678/-234 across 23 files
  URL: https://github.com/openshift/installer/pull/5187

[... 7 more PRs ...]

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

### Example 1: Check Your Own PRs

```
/git:review-queue
```

Output:
```markdown
# Review Queue Report
All Repositories
Generated: 2025-10-31 14:30 UTC
Current User: @alice

---

## My PRs Needing Attention (4)

### Awaiting Reviews (3)

- #234 [openshift/api] feat: add new validation rules (opened 2 days ago)
  Tide: Needs lgtm label and approved label
  CI: All 4 checks passing
  Reviews: No reviews yet
  URL: https://github.com/openshift/api/pull/234

- #567 [kubernetes/kubernetes] fix: correct scheduler behavior (opened 5 days ago)
  Tide: Needs lgtm label and approved label
  CI: 15/16 checks passing (integration-test pending)
  Reviews: No reviews yet
  URL: https://github.com/kubernetes/kubernetes/pull/567

- #89 [openshift/installer] docs: update installation guide (opened 1 day ago)
  Tide: Needs lgtm label and approved label
  CI: All 3 checks passing
  Reviews: No reviews yet
  URL: https://github.com/openshift/installer/pull/89

### Requested Changes (1)

- #445 [openshift/cluster-api] refactor: improve error handling (opened 7 days ago)
  Tide: Needs lgtm label after addressing feedback
  CI: All 6 checks passing
  Reviews: 1 change request (@bob, 3 days ago)
  URL: https://github.com/openshift/cluster-api/pull/445

---

💡 Priority: Address change request on PR #445, then follow up on #567 (oldest)
```

### Example 2: Check Repository Review Queue

```
/git:review-queue openshift/installer
```

Output:
```markdown
# Review Queue Report
Repository: openshift/installer
Generated: 2025-10-31 14:35 UTC
Current User: @bob

---

## Repository: openshift/installer (18 open PRs, 12 needing review)

### PRs I've Reviewed (1)

- #5234 feat: add support for custom networking (opened 3 days ago)
  Author: @alice
  Your last comment: 1 day ago
  Tide: Needs approved label
  CI: All 6 checks passing
  Reviews: 1 lgtm (@bob), awaiting approval
  URL: https://github.com/openshift/installer/pull/5234

### Fresh PRs - No Reviews Yet (6)

- #5267 fix: handle cluster deletion errors (opened 2 days ago)
  Author: @charlie
  Tide: Needs lgtm label and approved label
  CI: All 7 checks passing
  Reviews: No reviews yet
  Labels: size/S, bugfix
  Changes: +34/-12 across 2 files
  URL: https://github.com/openshift/installer/pull/5267

- #5245 feat: add support for proxy configuration (opened 6 days ago)
  Author: @diana
  Tide: Needs lgtm label and approved label
  CI: 8/9 checks passing (e2e-vsphere pending)
  Reviews: No reviews yet
  Labels: size/L, enhancement
  Changes: +423/-67 across 11 files
  URL: https://github.com/openshift/installer/pull/5245

[... 4 more PRs ...]

### In Discussion (5)

- #5198 feat: improve Azure integration (opened 9 days ago)
  Author: @eve
  Tide: Needs lgtm label
  CI: All 8 checks passing
  Reviews: 2 comments (@frank, @grace)
  Labels: size/XL, azure
  Changes: +789/-234 across 19 files
  URL: https://github.com/openshift/installer/pull/5198

[... 4 more PRs ...]

### Excluded from Review
- 2 PRs with merge conflicts
- 1 draft PR
- 3 PRs with failing required CI

---

💡 Priority recommendations:
1. Review fresh PR #5245 (6 days old, substantial changes)
2. Review fresh PR #5267 (small bugfix, easy win)
3. PR #5234 (you reviewed) needs approval from maintainer
```

### Example 3: Repository with No PRs Needing Review

```
/git:review-queue openshift/api
```

Output:
```markdown
# Review Queue Report
Repository: openshift/api
Generated: 2025-10-31 14:40 UTC
Current User: @henry

---

## Repository: openshift/api (4 open PRs, 0 needing review)

All open PRs are either:
- Draft PRs (2)
- Have merge conflicts (1)
- Awaiting CI results (1)

### Excluded from Review
- 2 draft PRs
- 1 PR with merge conflicts
- 1 PR with failing required CI

---

✅ No PRs currently need review. Check back later!
```

### Example 4: Your PRs All In Good State

```
/git:review-queue
```

Output:
```markdown
# Review Queue Report
All Repositories
Generated: 2025-10-31 14:45 UTC
Current User: @isabel

---

## My PRs Needing Attention (0)

### Ready to Merge (2)

- #678 [openshift/installer] feat: add new platform support (opened 4 days ago)
  Tide: In merge queue (position 3)
  CI: All 8 checks passing
  Reviews: 2 approvals (@jack, @karen)
  URL: https://github.com/openshift/installer/pull/678

- #345 [openshift/api] fix: validation bug (opened 2 days ago)
  Tide: Ready to merge
  CI: All 4 checks passing
  Reviews: 2 approvals (@lisa, @mike)
  URL: https://github.com/openshift/api/pull/345

---

✅ All your PRs are approved or in the merge queue!
```

### Example 5: Large Repository with Many PRs

```
/git:review-queue kubernetes/kubernetes
```

Output shows first 50 PRs with note:
```markdown
# Review Queue Report
Repository: kubernetes/kubernetes
Generated: 2025-10-31 14:50 UTC
Current User: @noah

---

## Repository: kubernetes/kubernetes (247 open PRs, showing 50 most recent)

ℹ️  Note: This repository has many open PRs. Showing most recent 50. Use filters to narrow down:
   - gh pr list --repo kubernetes/kubernetes --label "area/scheduler"
   - gh pr list --repo kubernetes/kubernetes --author "@me"

[... categorized list of 50 PRs ...]

---

💡 Tip: Focus on "Fresh PRs" in your area of expertise for maximum impact
```

## Arguments

- `org/repo` (optional): Repository to analyze in format `owner/repo`. If omitted, shows your PRs across all repositories.

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
- API calls are batched where possible to avoid rate limits
- Results can be cached for 5-10 minutes for repeated queries
- Use `--json` output from `gh` CLI for efficient parsing

### GitHub Permissions

This command requires:
- Read access to the repository
- GitHub CLI (`gh`) authenticated
- Access to GitHub Status API for tide information

### Caveats

- Tide status is specific to Prow-based CI systems (OpenShift, Kubernetes)
- For non-Prow repos, falls back to checking labels and review status
- Draft PRs are excluded in repository mode but shown in "My PRs" mode
- Bot PRs (renovate, dependabot) are excluded unless authored by you

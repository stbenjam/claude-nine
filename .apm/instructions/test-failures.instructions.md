---
description: "Rules to follow with test failures"
applyTo: "**"
---

When any test fails, you MUST follow this process:

## Never Assume Pre-existing Failures

- NEVER dismiss a test failure as "pre-existing" or "unrelated" without thorough investigation.
- Always consider whether your changes caused or contributed to the failure, even if the connection is not immediately obvious.
- Correlation matters: if a test fails after your change, the default assumption is that your change broke it until proven otherwise.

## Required Investigation Steps

1. **Read the full error output** — understand exactly what failed and why.
2. **Trace the failure to root cause** — identify the specific assertion, error, or panic that triggered the failure.
3. **Check if your changes touch the failing code path** — follow imports, shared state, interfaces, and transitive dependencies. Subtle interactions count.
4. **Run the test on the base branch** — if you need to prove the failure is pre-existing, actually verify it fails without your changes too. Do not guess.
5. **Provide a concrete explanation** — state why the test failed. "It was already broken" is not sufficient without evidence.

## If the Failure Is Genuinely Pre-existing

- You must still explain the root cause of the failure.
- Offer to fix it (Boy Scout Rule: leave the codebase better than you found it).
- If the fix is out of scope, flag it clearly and suggest a follow-up.

## If the Failure Is Caused by Your Changes

- Fix it before moving on. Do not leave broken tests behind.
- If the test expectation is wrong (e.g., testing old behavior you intentionally changed), update the test and explain why the old expectation no longer applies.

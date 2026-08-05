---
name: books-acquirer
description: Acquire named books via library borrow/hold/download first, then explicit retailer purchase; use for get, hold, borrow, buy, or EPUB requests.
user-invocable: true
---

# Book Acquirer

Acquire a specific, verified book through the user's connected libraries or a
retailer. Prefer libraries, preserve format intent, and keep paid fallback
explicit.

## Required skills

Load and follow these skills only when needed:

- `books-calibre`: check ownership and verify imports.
- Your persistent browser automation: drive the library app (e.g. Libby) and
  retailer (e.g. Kobo).
- Your web search tooling (for example a `firecrawl-search` skill): resolve
  uncertain bibliographic details or locate an exact listing.
- Your purchase/payment workflow (for example a `make-purchase` skill):
  perform a retailer purchase only after explicit paid-purchase intent.

Use the persistent library profile connected to the user's library systems.
Use the persistent retailer profile connected to the user's account.

## Interpret the request

1. Resolve the exact title, author, edition, ISBN when available, and desired
   format.
2. Preserve explicit verbs:
   - `place a hold` means one library hold.
   - `borrow` means a library loan if available.
   - `buy` means a retailer purchase workflow.
   - `download EPUB/ACSM` means obtain only a file the lending or retail site
     legally offers.
3. For a generic `get` or `acquire` request, use library-first defaults:
   - Prefer ebook unless the user asked to listen or specified audiobook.
   - Borrow immediately when the requested format is available.
   - Otherwise place the shortest library hold when the estimated wait is six
     weeks or less.
   - If the shortest wait exceeds six weeks or the format is absent, present the
     best hold and current retailer option. Do not begin a paid purchase until
     the user explicitly chooses to buy.
4. Never silently substitute audiobook for ebook or vice versa.
5. Treat a structured handoff from `books-release-scout` as context, not fresh
   truth. Recheck every mutable fact.

## Check ownership and duplicates

1. Search all Calibre records, including archived books, by ISBN and normalized
   title + author.
2. If the requested work is already owned, stop and report the Calibre record
   unless the user explicitly wants another edition or format.
3. Check the library app's Loans and Holds before acting.
4. Do not create a duplicate loan or hold. Report the existing system, format,
   and status instead.

## Recheck the library across all systems

1. Search every connected system for the exact title and author.
2. Verify ebook and audiobook records separately.
3. Record availability, estimated wait, queue position when shown, copy counts
   when shown, system, and format.
4. Rank identical-format options:
   - available now,
   - shortest estimated wait,
   - stronger copy-to-hold ratio,
   - preferred home system only as a tie-breaker.
5. If bibliographic matches conflict, verify ISBN or publisher before acting.
6. Never expose library card numbers in chat, logs, screenshots, or state.

## Borrow from the library

Borrow only when the user explicitly chose `borrow` or when a generic
`get/acquire` request reaches an immediately available library-first result.

1. Select the requested format and best connected system.
2. Use the longest offered loan period unless the user specified otherwise.
3. Submit the loan once.
4. Verify the title appears on the Loans shelf and record its due date.
5. For ebooks, inspect the manage-loan or reading options for a legally offered
   download:
   - `Download EPUB ebook`,
   - `Download DRM-free EPUB`,
   - `Download Adobe EPUB` or an ACSM fulfillment file.
6. Do not extract protected app data, reverse engineer APIs, or circumvent DRM.
7. Audiobooks remain in the app unless the site explicitly offers a standard
   downloadable file. Never scrape or reconstruct audiobook media.

## Place a library hold

Place a hold only when the user explicitly chose `place hold` or when a generic
`get/acquire` request reaches a wait of six weeks or less.

1. Recheck availability immediately before submission.
2. Select one system with the shortest wait for the requested format.
3. Submit one hold.
4. Verify it appears on the Holds shelf.
5. Report system, format, estimated wait, and queue position when shown.
6. If the title became available, borrow only when the request already
   authorized generic acquisition; otherwise offer `Borrow now`.

## Download and import a library ebook

When a library loan exposes a download:

1. Save the offered file to the user's Calibre import/watch folder with a clear
   title-author filename when possible.
2. For EPUB:
   - verify the file type,
   - run a ZIP integrity check,
   - wait for the watched folder to consume it,
   - verify the resulting Calibre title, author, format, and record ID.
3. For ACSM:
   - verify it is non-empty XML or an Adobe fulfillment document,
   - place it in the import folder,
   - verify whether the configured importer consumes it,
   - report ACSM honestly if no readable EPUB appears.
4. Do not claim successful Calibre import merely because a download event fired.
5. If the library offers only in-app reading or send-to-Kindle, report that
   limitation; do not fabricate a downloadable EPUB.

## Buy from a retailer

Begin this section only after the user explicitly says to buy, chooses a `Buy`
action, or approves the paid fallback with the displayed price.

1. Open the exact United States retailer listing and verify title, author,
   edition, format, DRM/download option, and current price.
2. Reject country switching, unrelated editions, subscriptions, financing, and
   trial upsells unless the user explicitly requested them.
3. Load and follow your purchase/payment workflow for the payment approval,
   checkout, receipt handling, and reporting rules.
4. After successful purchase, open the retailer library and use the title's
   download action.
5. Save EPUB or ACSM to the user's Calibre import/watch folder.
6. Validate the file and verify watched-folder import exactly as in the library
   download workflow.
7. Clean up any temporary payment credential files. Never reveal card details.

## Shared recommendation ledger

If `memory/books-release-scout.json` exists, update only after verifying the
action:

- `held`: a library hold is visible.
- `borrowed`: a library loan is visible.
- `bought`: the retailer confirms the order.
- `owned`: Calibre already contained the book or import is verified.

Store the selected system and a short non-secret note. Never store credentials,
card identifiers, library card numbers, browser state, or approval URLs.

## Report the result

Report only verified facts:

- title, author, and format,
- acquisition path: library system or retailer,
- hold wait/position or loan due date,
- retailer total and order number when purchased,
- downloaded file type,
- Calibre record ID when imported,
- any limitation such as app-only reading or unprocessed ACSM.

## Safety checks

- No hold, loan, or purchase without an explicit acquisition request.
- No paid fallback from a generic request without a displayed price and explicit
  buy choice.
- No duplicate holds across systems unless the user explicitly requests that
  strategy.
- No format substitution without consent.
- No DRM circumvention or audiobook extraction.
- No retailer country change, points redemption, subscription, or trial without
  explicit instruction.
- Stop when identity verification, a new library-card login, suspicious
  redirects, or a materially higher total requires the user's involvement.

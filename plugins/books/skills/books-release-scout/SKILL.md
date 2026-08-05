---
name: books-release-scout
description: Read-only new-release book recommendations from Calibre ratings with current library availability and retailer pricing; use for book scouting.
user-invocable: true
---

# Book Release Scout

Find a small set of genuinely new books the user is likely to enjoy, explain
why each fits, and present current acquisition choices without taking any
external action.

## Required skills

Load and follow these skills only when their stage is needed:

- `books-calibre`: query the user's library and reading metadata.
- Your web search tooling (for example a `firecrawl-search` skill): discover
  releases and verify current publication facts.
- Your persistent browser automation: perform read-only library and retailer
  (e.g. Libby, Kobo) checks.

Use the persistent library profile connected to the user's library systems and
the persistent retailer profile connected to the user's account.

Do not load purchase credentials, place a hold, borrow a title, start a
subscription, or buy anything from this skill. Hand explicit acquisition
choices to `books-acquirer`.

Do not create a recurring schedule unless the user separately asks for one.

## Default scope

- Treat "new releases" as books published in the last 90 days.
- Include a separate "coming soon" candidate only when it publishes within the
  next 120 days and is an unusually strong match.
- Consider English-language ebooks and audiobooks unless the user narrows the
  format.
- Return 3–5 candidates. Prefer scores of 70 or higher and suppress weak
  filler.
- Keep availability separate from taste score; a long library wait does not
  make a book a worse recommendation.

## Build the taste profile

1. Query read, non-archived books with:
   `title,authors,series,series_index,tags,rating,*goodreads,*dateread,pubdate,isbn`.
2. Treat built-in `rating` as the user's personal Calibre rating on the
   10-point scale:
   - 10 = 5 stars, strongest positive signal.
   - 8 = 4 stars, positive signal.
   - 6 = 3 stars, neutral.
   - 4 or lower = negative signal.
   - Missing ratings are unknown, never dislikes.
3. Treat `*goodreads` as Goodreads community rating, not the user's personal
   rating. Use it only as supporting evidence or a tie-breaker.
4. Weight authors, series, and tags from personal ratings. Give modest extra
   weight to books read in the last two years.
5. Query all Calibre records, including archived and unread books, for
   ownership and TBR deduplication.
6. Read [`references/scoring.md`](references/scoring.md) before ranking
   candidates.

## Discover and verify candidates

1. Generate discovery queries from high-weight authors, series, tags, and
   cross-tag combinations. Include direct sequel and new-author discovery.
2. Search current web sources. Prefer official publisher and author pages for
   title, author, ISBN, format, and publication date. Use reputable trade
   publications or retailer/library records as corroboration.
3. Verify the exact publication date against at least one authoritative source.
   Use a second source when release status or regional availability conflicts.
4. Exclude:
   - Books already in Calibre by ISBN or normalized title + author.
   - Books already borrowed or on hold in the library app.
   - Duplicate editions of the same work.
   - Unverified or materially conflicting release records.
5. For sequels, identify the series position and check whether preceding
   volumes are owned or read. Penalize a sequel when the user has not reached
   it; prefer recommending the next unread volume instead.

## Check acquisition options read-only

For each shortlisted candidate, gather current options without changing any
account.

### Library (e.g. Libby)

1. Search all connected library systems in the persistent library profile.
2. Check ebook and audiobook separately.
3. Record:
   - available now vs hold required,
   - estimated wait,
   - queue position when shown,
   - lending system,
   - format,
   - whether a downloadable EPUB/ACSM option is advertised.
4. Prefer the shortest wait for identical formats. Note duplicate holdings, but
   do not place a hold or borrow.
5. Never expose library card numbers in chat, logs, or saved state.

### Retailer (e.g. Kobo)

1. Open the exact United States retailer product page.
2. Record current price, format, DRM/download option, and whether any
   subscription is merely promotional.
3. Do not start a trial, use points, change country, add to cart, or enter
   checkout.
4. Treat format and DRM as acquisition facts, not taste evidence.

## Present recommendations

Show no more than five concise recommendation cards. Each card must include:

- Title and author
- Publication date and status: Released or Coming soon
- Taste score and confidence
- Two concrete reasons tied to the user's rated authors, books, series, or tags
- Series position when applicable
- Library status for the best system/format
- Retailer price and DRM/download format when available
- Clear choices such as:
  - `Place library hold`
  - `Borrow now`
  - `Buy and import to Calibre`
  - `Skip`

Do not say "you'll love this." Calibrate uncertainty and explain the evidence.

If the user selects an action, stop the scout workflow and load
`books-acquirer`. Pass the exact title, author, ISBN when known, requested
format, selected action, best library system, retailer URL, observed retailer
price, and any wait estimate. The acquirer must recheck all mutable facts
before acting.

## Recommendation ledger

Maintain `memory/books-release-scout.json` as a small non-secret ledger:

```json
{
  "version": 1,
  "candidates": {
    "<isbn-or-normalized-title-author>": {
      "title": "",
      "author": "",
      "first_presented": "YYYY-MM-DD",
      "last_presented": "YYYY-MM-DD",
      "score": 0,
      "status": "presented|skipped|held|borrowed|bought|owned",
      "system": null,
      "notes": ""
    }
  }
}
```

- Create the file only after the first recommendation run.
- Never store credentials, card identifiers, library card numbers, or session
  data.
- Do not re-present `held`, `borrowed`, `bought`, or `owned` items.
- Suppress `skipped` items for 180 days unless the user asks to reconsider.
- Update `presented` or `skipped` only after the recommendation or response was
  sent.
- Allow `books-acquirer` to update verified action outcomes.

## Quality checks

Before sending recommendations, confirm:

- The date window was applied against today's verified date.
- Every candidate has an authoritative publication date.
- Calibre, library loans/holds, and the ledger were checked for duplicates.
- Personal ratings drive the score; Goodreads community ratings do not
  masquerade as personal taste.
- Availability and prices are current enough to label with the check time.
- No purchase, hold, borrow, subscription, cart mutation, or country change
  occurred.

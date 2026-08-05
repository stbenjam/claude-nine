# Scoring model

Use a 0–100 taste score. Score taste independently from price or library wait time.

## Components

- **Author and series affinity: 0–30**
  - Strongest for authors or series with multiple personal 5-star ratings.
  - Do not max this component from a single read.
- **Tag and genre affinity: 0–25**
  - Weight tag combinations more than broad tags such as Fiction or General.
  - Downweight publisher-import noise and overly generic tags.
- **Synopsis and theme similarity: 0–20**
  - Compare the verified synopsis to themes from the user's 4–5 star books.
  - Require specific shared themes or structures, not generic marketing language.
- **Trusted evidence: 0–10**
  - Use reputable reviews, awards, starred trade reviews, or strong community reception.
  - Goodreads community rating is supporting evidence only.
- **Recency and release confidence: 0–5**
  - Full credit for a verified date inside the default release window.
- **Novelty and format fit: 0–10**
  - Reward a plausible expansion of the user's taste rather than only repeating the same authors.
  - Include ebook/audiobook fit when known.

## Personal-rating weights

For each rated read book, derive a base preference weight:

- Calibre rating 10: +3
- Calibre rating 8: +2
- Calibre rating 6: 0
- Calibre rating 4: -2
- Calibre rating 2: -3
- Missing rating: 0

Multiply by 1.25 when the book was read within the last two years. Aggregate author, series, tag, and theme signals, then normalize so prolific authors or huge tag categories do not dominate.

## Penalties and exclusions

- Already owned, held, borrowed, or previously bought: exclude.
- Exact duplicate edition or alternate ISBN of the same work: exclude.
- Publication date cannot be verified: exclude.
- Preceding series volume not owned/read: subtract up to 20 and usually recommend the next unread volume instead.
- Strong overlap with multiple low-rated books: subtract up to 25.
- Candidate supported only by Goodreads community rating and no personal-taste evidence: cap at 70.
- Suspicious review manipulation or conflicting bibliographic data: exclude until verified.

## Confidence labels

- 85–100: High confidence
- 75–84: Good match
- 70–74: Exploratory
- Below 70: suppress unless the user asks for a broader list

Every recommendation must cite at least two concrete taste signals. Availability and price belong in the acquisition section and never change the taste score.

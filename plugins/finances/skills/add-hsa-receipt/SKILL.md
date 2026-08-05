---
name: add-hsa-receipt
description: Extract and file an HSA receipt into a year-based folder with a records CSV and a standardized filename.
argument-hint: "<path-to-receipt>"
user-invocable: true
---

# File an HSA receipt

Ask for a receipt path when it is not provided. Read the PDF or image and
extract the transaction date, concise vendor or service description, and total
amount. If the date or amount is unclear, ask the user rather than guessing.

In the current working directory:

1. create a directory named for the transaction year;
2. create `<year>/records.txt` with the header
   `Date,Description,Amount,Filename` when it does not exist;
3. append a valid CSV row using an ISO date and a two-decimal amount; and
4. copy the original file to
   `YYYY-MM-DD_description_amount.ext`, lowercasing and sanitizing the
   description while preserving the extension.

Never overwrite an existing receipt silently. Add a numeric suffix or ask the
user which duplicate to keep. Confirm the extracted fields, destination path,
and records file only after both the copy and CSV update succeed.

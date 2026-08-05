# finances

Organize HSA receipts and financial documents with a shared Claude Code and
Codex skill.

## Skill

Use `add-hsa-receipt` with a receipt path. The skill reads a PDF or image,
extracts the date, description, and amount, creates a year-based directory,
updates `<year>/records.txt`, and stores a sanitized copy named
`YYYY-MM-DD_description_amount.ext`.

It asks for clarification when required fields are unclear and never
silently overwrites duplicate files. Confirm the saved file and records entry
only after both writes succeed.

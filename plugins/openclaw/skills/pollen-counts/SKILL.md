---
name: pollen-counts
description: Get current and forecast pollen counts for a US ZIP code. Use when asked about pollen, allergens, or allergy/pollen forecasts for a US location.
---

# Pollen Counts Skill

Get current and forecast pollen levels for a US ZIP code using the public
Pollen.com forecast API.

## Usage

```bash
python3 <skill-dir>/scripts/pollen_count.py <ZIP_CODE>
```

**Parameters:**

- `ZIP_CODE` (required): a valid 5-digit US ZIP code.

The script prints a formatted report with yesterday/today/tomorrow pollen
index values (0–12 scale), a level description, and the top allergens driving
the count.

## Requirements

- Python 3 with the `requests` package (`pip install requests`).

## Notes

- The Pollen.com API returns empty periods for invalid ZIP codes; the script
  reports that as an error rather than guessing.

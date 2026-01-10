---
description: Process and file an HSA receipt
argument-hint: <path-to-receipt>
---

## Name
finances:add-hsa-receipt

## Synopsis
```
/add-hsa-receipt <path-to-receipt>
```

## Description
Process an HSA receipt file by extracting transaction details and organizing it for tax records.

The command will:
1. Read the receipt file (PDF, image, or other format)
2. Extract transaction date, description, and amount using AI
3. Create a year-based directory in the current working directory
4. Maintain a CSV records file tracking all receipts
5. Copy and rename the receipt file for organized storage

## Arguments
- `$1` (required): Path to the receipt file (PDF, image, etc.)

## Implementation Instructions

### Step 1: Read the Receipt File
Use the Read tool to read the file provided in `$1`. Claude can natively read PDFs, images (PNG, JPG), and other file formats.

### Step 2: Extract Information Using AI
From the receipt content, extract:
- **Transaction date**: Look for dates in various formats (MM/DD/YYYY, YYYY-MM-DD, written dates, etc.)
  - If no date is found or unclear, use today's date
- **Brief description**: Identify the vendor/provider name or service description
  - Keep it concise (e.g., "Dental cleaning", "CVS Pharmacy", "Dr. Smith visit")
  - Should be clear enough to understand the transaction at a glance
- **Total amount**: Find the total transaction amount
  - Look for "Total", "Amount Due", "Total Paid", etc.
  - Return as a number with two decimal places (e.g., 350.00)
  - Exclude dollar signs in the extracted value

### Step 3: Determine the Year
Extract the year from the transaction date (e.g., if date is 2024-01-09, year is "2024").

### Step 4: Create Year Directory
In the current working directory, create a directory named with just the year if it doesn't already exist:
```bash
mkdir -p YYYY
```

Example: `mkdir -p 2024`

### Step 5: Initialize or Append to CSV File
The CSV file is located at `<year>/records.txt`.

**If the file doesn't exist:**
1. Create it
2. Write the header row: `Date,Description,Amount,Filename`

**Append the new entry:**
Format: `YYYY-MM-DD,description,amount,filename`

Example: `2024-01-09,Dental cleaning,350.00,2024-01-09_dental-cleaning_350.00.pdf`

**Important CSV handling:**
- If the description contains commas, wrap it in quotes: `"Smith, Dr. John"`
- Amount should NOT include dollar sign, just the number
- Use the sanitized filename (see next step) for the Filename column

### Step 6: Copy and Rename the File
Copy the original file to the year directory with a new standardized name.

**Filename format:** `YYYY-MM-DD_description_amount.ext`

**Sanitization rules:**
- Description: convert to lowercase, replace spaces with hyphens
- Remove special characters except hyphens and underscores
- Amount: include dollars and cents (e.g., "350.00")
- Preserve the original file extension

**Examples:**
- Original: `~/Downloads/receipt.pdf`
- Date: 2024-01-09, Description: "Dental Cleaning", Amount: 350.00
- New name: `2024-01-09_dental-cleaning_350.00.pdf`

**Command:**
```bash
cp "$ORIGINAL_PATH" "YYYY/YYYY-MM-DD_description_amount.ext"
```

**Handle duplicates:**
If the destination file already exists, you may:
- Add a suffix like `-2`, `-3` to avoid overwriting
- Or ask the user if they want to overwrite

### Step 7: Confirm Completion
Output a summary showing:
- The extracted information (date, description, amount)
- The new file location
- Confirmation that records.txt was updated

**Example output format:**
```
Processed HSA receipt:
  Date: 2024-01-09
  Description: Dental cleaning
  Amount: $350.00

File saved: ./2024/2024-01-09_dental-cleaning_350.00.pdf
Record added to: ./2024/records.txt
```

## Example Usage

**Command:**
```
/add-hsa-receipt ~/Downloads/dental-receipt.pdf
```

**Process:**
1. Read `~/Downloads/dental-receipt.pdf`
2. Extract: Date=2024-01-09, Description="Dental cleaning", Amount=$350.00
3. Create directory: `./2024/` (if needed)
4. Initialize/append to `./2024/records.txt`:
   - If new file, add header: `Date,Description,Amount,Filename`
   - Append: `2024-01-09,Dental cleaning,350.00,2024-01-09_dental-cleaning_350.00.pdf`
5. Copy file: `cp ~/Downloads/dental-receipt.pdf ./2024/2024-01-09_dental-cleaning_350.00.pdf`

**Output:**
```
Processed HSA receipt:
  Date: 2024-01-09
  Description: Dental cleaning
  Amount: $350.00

File saved: ./2024/2024-01-09_dental-cleaning_350.00.pdf
Record added to: ./2024/records.txt
```

## Error Handling

- **File not found:** If `$1` doesn't exist, show error: "Receipt file not found: <path>"
- **Cannot extract info:** If AI cannot extract date/amount, ask user to provide the information
- **File copy fails:** Show error with details
- **CSV write fails:** Show error with details

## Notes

- Works with any file format Claude can read (PDF, PNG, JPG, etc.)
- CSV format allows easy import into spreadsheet software
- Year-based organization simplifies tax preparation
- Sanitized filenames ensure consistency and avoid shell issues

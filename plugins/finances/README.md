# finances

Manage HSA receipts and financial documents with automated AI-powered extraction and organization.

## Overview

The finances plugin helps you organize HSA (Health Savings Account) receipts and financial documents by automatically extracting transaction details and filing them in a structured, year-based directory system with CSV tracking.

## Features

### Commands

#### `/add-hsa-receipt`

Process an HSA receipt file by extracting transaction details and organizing it for tax records.

**Usage:**
```
/add-hsa-receipt <path-to-receipt>
```

**What it does:**
1. Reads the receipt file (PDF, image, or other format)
2. Extracts transaction date, description, and amount using AI
3. Creates a year directory in the current working directory (e.g., "2024")
4. Maintains a CSV file (`records.txt`) tracking all receipts
5. Copies and renames the receipt file with a standardized naming format

**File naming format:**
```
YYYY-MM-DD_description_amount.ext
```

Example: `2024-01-09_dental-cleaning_350.00.pdf`

**CSV format:**
The `records.txt` file uses CSV format with headers:
```
Date,Description,Amount,Filename
2024-01-09,Dental cleaning,350.00,2024-01-09_dental-cleaning_350.00.pdf
2024-01-15,CVS Pharmacy,45.99,2024-01-15_cvs-pharmacy_45.99.jpg
```

## Installation

No installation required! The plugin uses Claude's built-in AI capabilities and file handling tools. No external dependencies needed.

## Usage Examples

### Process a PDF receipt

```
/add-hsa-receipt ~/Downloads/dental-receipt.pdf
```

Output:
```
Processed HSA receipt:
  Date: 2024-01-09
  Description: Dental cleaning
  Amount: $350.00

File saved: ./2024/2024-01-09_dental-cleaning_350.00.pdf
Record added to: ./2024/records.txt
```

### Process an image receipt (photo from phone)

```
/add-hsa-receipt ~/Pictures/pharmacy-receipt.jpg
```

Output:
```
Processed HSA receipt:
  Date: 2024-01-15
  Description: CVS Pharmacy
  Amount: $45.99

File saved: ./2024/2024-01-15_cvs-pharmacy_45.99.jpg
Record added to: ./2024/records.txt
```

## Directory Structure

After using the command, your working directory will have this structure:

```
your-working-directory/
├── 2024/
│   ├── records.txt
│   ├── 2024-01-09_dental-cleaning_350.00.pdf
│   ├── 2024-01-15_cvs-pharmacy_45.99.jpg
│   └── 2024-02-03_urgent-care_125.00.pdf
└── 2025/
    ├── records.txt
    └── 2025-01-05_pharmacy_28.50.pdf
```

## CSV Import

The `records.txt` files can be easily imported into spreadsheet software:

**Excel/Google Sheets:**
1. Open the application
2. Import CSV file
3. Select comma as delimiter
4. Data will be organized in columns: Date, Description, Amount, Filename

**Command line (view in terminal):**
```bash
cat 2024/records.txt | column -t -s,
```

## Supported File Formats

The plugin works with any file format that Claude can read, including:
- PDF documents
- Images (PNG, JPG, JPEG)
- Other receipt formats

## Tips

1. **Organize by project:** Create different directories for different purposes (HSA, business expenses, etc.)
2. **Regular backups:** Back up your year directories regularly
3. **Tax time:** The CSV files make it easy to calculate total expenses and generate reports
4. **Description clarity:** The AI extracts vendor names and services automatically, but you can manually edit `records.txt` if needed

## FAQ

**Q: What if the AI can't extract the date or amount?**
A: The command will ask you to provide the missing information manually.

**Q: What if I have a duplicate receipt?**
A: The command will detect existing files and either add a suffix or ask if you want to overwrite.

**Q: Can I edit the records.txt file manually?**
A: Yes! It's a standard CSV file. Just maintain the format: `Date,Description,Amount,Filename`

**Q: What date format should I expect?**
A: All dates are stored in ISO format: `YYYY-MM-DD` (e.g., 2024-01-09)

**Q: Can I use this for non-HSA receipts?**
A: Absolutely! It works for any financial documents you want to organize.

## Version

**v0.0.1** - Initial release

## Author

Created for the Claude Code marketplace.

## License

This plugin is provided as-is for use with Claude Code.

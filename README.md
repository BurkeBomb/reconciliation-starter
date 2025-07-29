# Reconciliation Starter

This repository contains a small Python script to reconcile bank transactions with your practice management ledger.

## Usage

Provide two Excel files:
1. **Bank file** – the transactions received by the bank.
2. **Practice file** – the payments recorded in your practice system.

Both files should include a reference column (for example an invoice or patient ID) and an amount column. If the column names differ between the bank and practice files you can specify them on the command line.
Reference values are trimmed of surrounding whitespace before matching.

Run the script:

```bash
python reconcile.py bank.xlsx practice.xlsx report.xlsx
```

The resulting `report.xlsx` lists each reference with:
- the amount recorded by the bank
- the amount recorded by your practice
- a `difference` column (bank minus practice)
- a `status` column indicating if payments match or which file is missing the entry

### Column Options

Specify the column names for each file individually:

```bash
python reconcile.py bank.xlsx practice.xlsx report.xlsx \
  --bank-reference BankRef --practice-reference InvoiceID \
  --bank-amount Received --practice-amount Paid
```

### Requirements

- Python 3
- `pandas` library (install via `pip install pandas openpyxl`)


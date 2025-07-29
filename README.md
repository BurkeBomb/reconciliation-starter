# Reconciliation Starter

This repository contains a small Python script to reconcile bank transactions with your practice management ledger.

## Usage

Provide two Excel files:
1. **Bank file** – the transactions received by the bank.
2. **Practice file** – the payments recorded in your practice system.

Both files should include a reference column (for example an invoice or patient ID) and an amount column. If the column names differ between the bank and practice files you can specify them on the command line.

Run the script:

```bash
python reconcile.py bank.xlsx practice.xlsx report.xlsx
```

The resulting `report.xlsx` lists each reference with the amounts found in the bank and practice files and a status column showing whether the payments match or if one is missing.

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


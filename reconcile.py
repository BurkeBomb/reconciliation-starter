import argparse
import pandas as pd


def load_excel(path: str) -> pd.DataFrame:
    """Load an Excel file into a DataFrame with empty strings replaced by NaN."""
    df = pd.read_excel(path)
    df = df.dropna(how="all")
    df = df.fillna("")
    return df


def normalize_amount(series: pd.Series) -> pd.Series:
    """Convert amount strings to floats."""
    return pd.to_numeric(series, errors="coerce").fillna(0)


def reconcile(
    bank_df: pd.DataFrame,
    practice_df: pd.DataFrame,
    bank_ref: str = "Reference",
    practice_ref: str = "Reference",
    bank_amount: str = "Amount",
    practice_amount: str = "Amount",
    tolerance: float = 0.01,
) -> pd.DataFrame:
    """Return a reconciliation DataFrame merging bank and practice by reference."""
    bank_df = bank_df.copy()
    practice_df = practice_df.copy()

    # Normalize reference columns for reliable matching
    bank_df[bank_ref] = bank_df[bank_ref].astype(str).str.strip()
    practice_df[practice_ref] = practice_df[practice_ref].astype(str).str.strip()

    bank_df[bank_amount] = normalize_amount(bank_df[bank_amount])
    practice_df[practice_amount] = normalize_amount(practice_df[practice_amount])

    bank_df.rename(columns={bank_ref: "Reference", bank_amount: "Amount_bank"}, inplace=True)
    practice_df.rename(columns={practice_ref: "Reference", practice_amount: "Amount_practice"}, inplace=True)

    merged = pd.merge(
        bank_df,
        practice_df,
        on="Reference",
        how="outer",
        indicator=True,
    )

    def status(row):
        if row["_merge"] == "both":
            if abs(row["difference"]) <= tolerance:
                return "matched"
            else:
                return "amount_mismatch"
        elif row["_merge"] == "left_only":
            return "missing_in_practice"
        else:
            return "missing_in_bank"

    merged["difference"] = merged["Amount_bank"].fillna(0) - merged["Amount_practice"].fillna(0)

    merged["status"] = merged.apply(status, axis=1)
    merged.drop(columns=["_merge"], inplace=True)
    return merged


def main():
    parser = argparse.ArgumentParser(description="Reconcile bank and practice Excel files")
    parser.add_argument("bank", help="Bank transactions Excel file")
    parser.add_argument("practice", help="Practice payments Excel file")
    parser.add_argument("output", help="Output Excel file with reconciliation report")
    parser.add_argument("--bank-reference", default="Reference",
                        help="Reference column in the bank file")
    parser.add_argument("--practice-reference", default="Reference",
                        help="Reference column in the practice file")
    parser.add_argument("--bank-amount", default="Amount",
                        help="Amount column in the bank file")
    parser.add_argument("--practice-amount", default="Amount",
                        help="Amount column in the practice file")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.01,
        help="Allowed difference between amounts to still consider them a match",
    )
    args = parser.parse_args()

    bank_df = load_excel(args.bank)
    practice_df = load_excel(args.practice)

    result = reconcile(
        bank_df,
        practice_df,
        bank_ref=args.bank_reference,
        practice_ref=args.practice_reference,
        bank_amount=args.bank_amount,
        practice_amount=args.practice_amount,
        tolerance=args.tolerance,
    )
    result.to_excel(args.output, index=False)
    print(f"Reconciliation written to {args.output}")


if __name__ == "__main__":
    main()

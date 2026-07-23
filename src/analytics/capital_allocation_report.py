import pandas as pd
from pathlib import Path

OUTPUT = Path("output")

cashflow = pd.read_excel(
    OUTPUT / "cashflow_intelligence.xlsx"
)

print("Loaded", len(cashflow), "companies")

# ==========================================
# Distribution Summary
# ==========================================

summary = (
    cashflow["capital_allocation_label"]
    .value_counts()
    .reset_index()
)

summary.columns = [
    "Capital Allocation Pattern",
    "Company Count"
]

print("\nCapital Allocation Distribution\n")
print(summary)

summary.to_csv(
    OUTPUT / "capital_allocation_distribution.csv",
    index=False
)

# ==========================================
# Pattern Changes Report
# ==========================================

pattern_changes = cashflow[
    [
        "company_id",
        "sector",
        "capital_allocation_label"
    ]
].copy()

pattern_changes.rename(
    columns={
        "capital_allocation_label": "Current Pattern"
    },
    inplace=True
)

pattern_changes["Previous Pattern"] = "N/A"
pattern_changes["Pattern Changed"] = "Unknown"

pattern_changes.to_csv(
    OUTPUT / "pattern_changes.csv",
    index=False
)

print("\nPattern Change Report Generated")

# ==========================================
# Save Updated Excel
# ==========================================

cashflow.to_excel(
    OUTPUT / "cashflow_intelligence.xlsx",
    index=False
)

print("\nUpdated cashflow_intelligence.xlsx")

print("\nDay 32 Completed Successfully")
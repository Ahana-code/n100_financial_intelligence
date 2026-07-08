import sqlite3
import pandas as pd

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    asset_turnover
)

from cashflow_kpis import (
    free_cash_flow
)


DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)


pl = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

bs = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cf = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

# Remove duplicate company-year records BEFORE merge
bs = bs.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

cf = cf.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)


print("\nProfit & Loss Columns")
print(pl.columns.tolist())

print("\nBalance Sheet Columns")
print(bs.columns.tolist())

print("\nCash Flow Columns")
print(cf.columns.tolist())

data = (
    pl.merge(
        bs,
        on=["company_id", "year"],
        how="inner"
    )
    .merge(
        cf,
        on=["company_id", "year"],
        how="inner"
    )
)

print("\nMerged rows:", len(data))
print(data.head())

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover
)

from cashflow_kpis import (
    free_cash_flow
)

# ----------------------------
# Calculate KPI columns
# ----------------------------

data["net_profit_margin_pct"] = data.apply(
    lambda x: net_profit_margin(
        x["net_profit"],
        x["sales"]
    ),
    axis=1
)

data["operating_profit_margin_pct"] = data.apply(
    lambda x: operating_profit_margin(
        x["operating_profit"],
        x["sales"]
    ),
    axis=1
)

data["return_on_equity_pct"] = data.apply(
    lambda x: return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

data["debt_to_equity"] = data.apply(
    lambda x: debt_to_equity(
        x["borrowings"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

data["interest_coverage"] = data.apply(
    lambda x: interest_coverage_ratio(
        x["operating_profit"],
        x["other_income"],
        x["interest"]
    ),
    axis=1
)

data["asset_turnover"] = data.apply(
    lambda x: asset_turnover(
        x["sales"],
        x["total_assets"]
    ),
    axis=1
)

data["free_cash_flow_cr"] = data.apply(
    lambda x: free_cash_flow(
        x["operating_activity"],
        x["investing_activity"]
    ),
    axis=1
)

print("\nCalculated KPI Preview")
print(
    data[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr"
        ]
    ].head()
)

duplicates = data[
    data.duplicated(
        subset=["company_id", "year"],
        keep=False
    )
]

ratio_df = data[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "eps",
        "dividend_payout",
        "borrowings",
        "operating_activity"
    ]
].copy()

ratio_df.rename(
    columns={
        "eps": "earnings_per_share",
        "dividend_payout": "dividend_payout_ratio_pct",
        "borrowings": "total_debt_cr",
        "operating_activity": "cash_from_operations_cr"
    },
    inplace=True
)

# Columns that exist in schema but we haven't computed yet
ratio_df["capex_cr"] = None
ratio_df["book_value_per_share"] = None

print("\nFinal Ratio Data")
print(ratio_df.head())
print("\nRows:", len(ratio_df))

print("\nDuplicate company-year records:")
print(
    duplicates[
        ["company_id", "year"]
    ].drop_duplicates()
)

print("\nTotal duplicate rows:", len(duplicates))

print("\nDuplicate rows in Profit & Loss")
print(
    pl.duplicated(
        subset=["company_id", "year"]
    ).sum()
)

print("\nDuplicate rows in Balance Sheet")
print(
    bs.duplicated(
        subset=["company_id", "year"]
    ).sum()
)

print("\nDuplicate rows in Cash Flow")
print(
    cf.duplicated(
        subset=["company_id", "year"]
    ).sum()
)

ratio_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("\nfinancial_ratios table populated successfully!")

conn.close()
import sqlite3
import pandas as pd
from pathlib import Path

from cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion,
    capital_allocation_pattern
)

DB_PATH = "db/nifty100.db"

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sectors = pd.read_sql(
    """
    SELECT company_id,
           broad_sector
    FROM sectors
    """,
    conn
)

conn.close()

results = []
distress = []

for company in sorted(cashflow["company_id"].unique()):

    cf = cashflow[cashflow["company_id"] == company].copy()
    pl = profit[profit["company_id"] == company].copy()
    rt = ratios[ratios["company_id"] == company].copy()

    if cf.empty or pl.empty or rt.empty:
        continue

    cf = cf.reset_index(drop=True)
    pl = pl.reset_index(drop=True)
    rt = rt.reset_index(drop=True)

    latest_cf = cf.iloc[-1]
    latest_pl = pl.iloc[-1]
    latest_rt = rt.iloc[-1]

    sector_row = sectors[sectors["company_id"] == company]

    if sector_row.empty:
        sector = "Unknown"
    else:
        sector = sector_row.iloc[0]["broad_sector"]

    cfo = latest_cf["operating_activity"]
    cfi = latest_cf["investing_activity"]
    cff = latest_cf["financing_activity"]

    sales = latest_pl["sales"]
    pat = latest_pl["net_profit"]

    fcf = free_cash_flow(cfo, cfi)

    cfo_label = cfo_quality_score(cfo, pat)

    capex_label = capex_intensity(
        cfi,
        sales
    )

    fcf_conv = fcf_conversion(
        fcf,
        latest_pl["operating_profit"]
    )

    allocation = capital_allocation_pattern(
        cfo,
        cfi,
        cff,
        cfo_label
    )

    distress_flag = False
    deleveraging_flag = False

    if cfo < 0 and cff > 0:
        distress_flag = True

        distress.append({
            "company_id": company,
            "CFO": cfo,
            "CFF": cff,
            "latest_net_profit": pat
        })

    if cff < 0:
        deleveraging_flag = True

    results.append({

        "company_id": company,
        "sector": sector,

        "cfo_quality_score": round(
            cfo / pat,
            2
        ) if pat != 0 else None,

        "cfo_quality_label": cfo_label,

        "capex_intensity_pct": round(
            abs(cfi) / sales * 100,
            2
        ) if sales != 0 else None,

        "capex_label": capex_label,

        "fcf_cagr_5yr": None,

        "fcf_conversion_pct": round(
            fcf_conv,
            2
        ) if fcf_conv is not None else None,

        "distress_flag": distress_flag,

        "deleveraging_flag": deleveraging_flag,

        "capital_allocation_label": allocation
    })

    results_df = pd.DataFrame(results)
distress_df = pd.DataFrame(distress)

results_df.to_excel(
    "output/cashflow_intelligence.xlsx",
    index=False
)

distress_df.to_csv(
    "output/distress_alerts.csv",
    index=False
)

print("=" * 50)
print("Cash Flow Intelligence Completed")
print("=" * 50)
print()

print("Companies Processed :", len(results_df))
print("Distress Alerts     :", len(distress_df))
print()

print(results_df.head(10))


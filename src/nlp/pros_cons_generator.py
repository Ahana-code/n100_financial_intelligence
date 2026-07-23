import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

pl = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

conn.close()

# -----------------------------
# Helper Functions
# -----------------------------

def latest_ratios(company_id):

    df = ratios[
        ratios["company_id"] == company_id
    ]

    if df.empty:
        return None

    return df.iloc[-1]


def latest_pl(company_id):

    df = pl[
        pl["company_id"] == company_id
    ]

    if df.empty:
        return None

    return df.iloc[-1]


def last_n_ratios(company_id, n=3):

    df = ratios[
        ratios["company_id"] == company_id
    ]

    if len(df) < n:
        return pd.DataFrame()

    return df.tail(n)


def last_n_pl(company_id, n=5):

    df = pl[
        pl["company_id"] == company_id
    ]

    if len(df) < n:
        return pd.DataFrame()

    return df.tail(n)


# -----------------------------
# Storage
# -----------------------------

results = []

def add_result(
    company,
    result_type,
    rule_id,
    text,
    confidence
):

    if confidence < 60:
        return

    results.append({

        "company_id": company,
        "type": result_type,
        "rule_id": rule_id,
        "text": text,
        "confidence_pct": confidence

    })


# -----------------------------
# Loop through companies
# -----------------------------

for company in companies["id"]:

    r_latest = latest_ratios(company)
    p_latest = latest_pl(company)

    if r_latest is None or p_latest is None:
        continue

    ratio3 = last_n_ratios(company, 3)
    pl5 = last_n_pl(company, 5)

        # ==========================================
    # PRO RULE 1
    # ROE > 20%
    # ==========================================

    if r_latest["return_on_equity_pct"] > 20:

        add_result(

            company,
            "pro",
            "PRO_01",
            "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
            95

        )

    # ==========================================
    # PRO RULE 2
    # Debt Free
    # ==========================================

    if r_latest["debt_to_equity"] == 0:

        add_result(

            company,
            "pro",
            "PRO_02",
            "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
            92

        )

    # ==========================================
    # PRO RULE 3
    # Positive Free Cash Flow
    # ==========================================

    if r_latest["free_cash_flow_cr"] > 0:

        add_result(

            company,
            "pro",
            "PRO_03",
            "Strong free cash flow generation signals healthy business fundamentals.",
            90

        )

    # ==========================================
    # PRO RULE 4
    # High Operating Margin
    # ==========================================

    if r_latest["operating_profit_margin_pct"] > 25:

        add_result(

            company,
            "pro",
            "PRO_04",
            "Operating profit margin above 25% indicates strong pricing power and cost discipline.",
            88

        )

    # ==========================================
    # PRO RULE 5
    # High Interest Coverage
    # ==========================================

    if r_latest["interest_coverage"] > 10:

        add_result(

            company,
            "pro",
            "PRO_05",
            "Very high interest coverage reflects negligible financial stress from debt servicing.",
            90

        )

    # ==========================================
    # PRO RULE 6
    # Healthy Dividend
    # ==========================================

    if (
        r_latest["dividend_payout_ratio_pct"] > 20
        and
        r_latest["free_cash_flow_cr"] > 0
    ):

        add_result(

            company,
            "pro",
            "PRO_06",
            "Healthy dividend payout supported by positive free cash flow.",
            82

        )

            # ==========================================
    # CON RULE 1
    # High Debt
    # ==========================================

    if r_latest["debt_to_equity"] > 2:

        add_result(

            company,
            "con",
            "CON_01",
            f"Debt-to-equity ratio of {r_latest['debt_to_equity']:.2f} is elevated and warrants monitoring.",
            92

        )

    # ==========================================
    # CON RULE 2
    # Negative Free Cash Flow
    # ==========================================

    if r_latest["free_cash_flow_cr"] < 0:

        add_result(

            company,
            "con",
            "CON_02",
            "Negative free cash flow raises concern about cash generation quality.",
            90

        )

    # ==========================================
    # CON RULE 3
    # Low Operating Margin
    # ==========================================

    if r_latest["operating_profit_margin_pct"] < 10:

        add_result(

            company,
            "con",
            "CON_03",
            "Operating margins remain weak and indicate pricing or cost pressure.",
            82

        )

    # ==========================================
    # CON RULE 4
    # Net Loss
    # ==========================================

    if p_latest["net_profit"] < 0:

        add_result(

            company,
            "con",
            "CON_04",
            "Company reported a net loss in the latest financial year.",
            98

        )

    # ==========================================
    # CON RULE 5
    # Low Interest Coverage
    # ==========================================

    if r_latest["interest_coverage"] < 1.5:

        add_result(

            company,
            "con",
            "CON_05",
            "Interest coverage below 1.5x indicates elevated debt servicing risk.",
            94

        )

    # ==========================================
    # CON RULE 6
    # Very Low ROE
    # ==========================================

    if r_latest["return_on_equity_pct"] < 10:

        add_result(

            company,
            "con",
            "CON_06",
            "Return on equity below 10% reflects weak shareholder returns.",
            85

        )

        # ==========================================
# Convert to DataFrame
# ==========================================

pros_cons = pd.DataFrame(results)

# ==========================================
# Ensure every company has at least
# one PRO and one CON
# ==========================================

for company in companies["id"]:

    company_rows = pros_cons[
        pros_cons["company_id"] == company
    ]

    if company_rows.empty:

        pros_cons.loc[len(pros_cons)] = [
            company,
            "pro",
            "DEFAULT_PRO",
            "Company has an established operating business.",
            60
        ]

        pros_cons.loc[len(pros_cons)] = [
            company,
            "con",
            "DEFAULT_CON",
            "Further financial analysis is recommended.",
            60
        ]

        continue

    if not (company_rows["type"] == "pro").any():

        pros_cons.loc[len(pros_cons)] = [
            company,
            "pro",
            "DEFAULT_PRO",
            "Company has an established operating business.",
            60
        ]

    if not (company_rows["type"] == "con").any():

        pros_cons.loc[len(pros_cons)] = [
            company,
            "con",
            "DEFAULT_CON",
            "Further financial analysis is recommended.",
            60
        ]

# ==========================================
# Save CSV
# ==========================================

pros_cons = pros_cons.sort_values(
    ["company_id", "type"]
)

pros_cons.to_csv(
    OUTPUT_DIR / "pros_cons_generated.csv",
    index=False
)

print("=" * 50)
print("Pros & Cons Generator Completed")
print("=" * 50)
print()

print("Total Rules Generated :", len(pros_cons))
print("Companies Covered     :", pros_cons["company_id"].nunique())

print()

print(
    pros_cons.head(15)
)

import sqlite3
import pandas as pd
import yaml

DB_PATH = "db/nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"


def load_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()
    return df


def load_config():
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


def apply_quality_compounder(df, config):

    rules = config["quality_compounder"]

    filtered = df.copy()

    filtered = filtered[
        filtered["return_on_equity_pct"] >= rules["roe_min"]
    ]

    filtered = filtered[
        filtered["debt_to_equity"] <= rules["debt_to_equity_max"]
    ]

    filtered = filtered[
        filtered["free_cash_flow_cr"] >= rules["free_cash_flow_min"]
    ]

    # Temporary Composite Score
    filtered["composite_quality_score"] = (
        filtered["return_on_equity_pct"] * 0.5
        + filtered["free_cash_flow_cr"] * 0.0005
        + (1 - filtered["debt_to_equity"]) * 50
    )

    filtered = filtered.sort_values(
        by="composite_quality_score",
        ascending=False
    )

    return filtered

def apply_value_pick(df, config):

    rules = config["value_pick"]

    filtered = df.copy()

    # Only apply D/E filter for now.
    # P/E, P/B and Dividend Yield will be added later
    # after those columns are available.

    filtered = filtered[
        filtered["debt_to_equity"] <= rules["debt_to_equity_max"]
    ]

    return filtered

def apply_growth_accelerator(df, config):

    rules = config["growth_accelerator"]

    filtered = df.copy()

    filtered = filtered[
        filtered["debt_to_equity"] <= rules["debt_to_equity_max"]
    ]

    return filtered

def apply_dividend_champion(df):

    filtered = df.copy()

    filtered = filtered[
        filtered["free_cash_flow_cr"] > 0
    ]

    filtered = filtered[
        filtered["dividend_payout_ratio_pct"] < 80
    ]

    return filtered


def apply_debt_free_blue_chip(df):

    filtered = df.copy()

    filtered = filtered[
        filtered["debt_to_equity"] == 0
    ]

    filtered = filtered[
        filtered["return_on_equity_pct"] > 12
    ]

    return filtered


def apply_turnaround_watch(df):

    filtered = df.copy()

    filtered = filtered[
        filtered["free_cash_flow_cr"] > 0
    ]

    return filtered

if __name__ == "__main__":

    df = load_data()
    config = load_config()

    quality = apply_quality_compounder(df, config)
    value = apply_value_pick(df, config)
    growth = apply_growth_accelerator(df, config)

    dividend = apply_dividend_champion(df)
    debtfree = apply_debt_free_blue_chip(df)
    turnaround = apply_turnaround_watch(df)

    print("\nQuality Compounder:", len(quality))
    print("Value Pick:", len(value))
    print("Growth Accelerator:", len(growth))
    print("Dividend Champion:", len(dividend))
    print("Debt Free Blue Chip:", len(debtfree))
    print("Turnaround Watch:", len(turnaround))
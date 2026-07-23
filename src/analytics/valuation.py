import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"


def load_valuation_data():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        c.id,
        c.company_name,
        c.book_value,
        c.roe_percentage,

        fr.year,
        fr.earnings_per_share,
        fr.free_cash_flow_cr,

        s.broad_sector

    FROM companies c

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    LEFT JOIN sectors s
        ON c.id = s.company_id
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


def latest_year_only(df):

    df = df.copy()

    df["year"] = df["year"].fillna("")

    df = (
        df.sort_values("year")
          .groupby("id")
          .tail(1)
    )

    return df.reset_index(drop=True)


def calculate_metrics(df):

    df = latest_year_only(df)

    df["FCF_Yield"] = (
           df["free_cash_flow_cr"] /
           df["book_value"]
    ).round(2)

    df["ROE_Class"] = df["roe_percentage"].apply(classify_roe)

    return df


def classify_roe(value):

    if pd.isna(value):
        return "Unknown"

    if value >= 20:
        return "Excellent"

    if value >= 15:
        return "Good"

    if value >= 10:
        return "Average"

    return "Weak"


if __name__ == "__main__":

    df = load_valuation_data()

    df = calculate_metrics(df)

    print(df.info())

print(df.head(20))

print("\nMissing values:\n")

print(df.isna().sum())
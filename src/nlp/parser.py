import sqlite3
import pandas as pd
import re
from pathlib import Path

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

analysis = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

conn.close()

pattern = re.compile(r"(\d+)\s*Years?:?\s*(-?[\d.]+)%")

parsed_rows = []
failed_rows = []

metric_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

for _, row in analysis.iterrows():

    company = row["company_id"]

    for metric in metric_columns:

        text = str(row[metric]).strip()

        match = pattern.search(text)

        if match:

            parsed_rows.append({

                "company_id": company,
                "metric_type": metric,
                "period_years": int(match.group(1)),
                "value_pct": float(match.group(2))

            })

        else:

            failed_rows.append({

                "company_id": company,
                "metric_type": metric,
                "original_text": text

            })

parsed = pd.DataFrame(parsed_rows)

failures = pd.DataFrame(failed_rows)

parsed.to_csv(
    OUTPUT_DIR / "analysis_parsed.csv",
    index=False
)

failures.to_csv(
    OUTPUT_DIR / "parse_failures.csv",
    index=False
)

print("Parsing Completed")

print(f"Parsed rows : {len(parsed)}")

print(f"Failed rows : {len(failures)}")
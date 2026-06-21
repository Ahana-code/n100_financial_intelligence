import pandas as pd
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "raw"

DB_PATH = BASE_DIR / "db" / "nifty100.db"



def create_connection():

    return sqlite3.connect(DB_PATH)



def clean_excel(file):

    df = pd.read_excel(
        file,
        skiprows=1
    )

    # remove empty columns
    df = df.dropna(
        axis=1,
        how="all"
    )

    # remove exact duplicate rows
    df = df.drop_duplicates()

    return df



def fix_companies(df):

    required_companies = [
        "ULTRACEMCO",
        "UNIONBANK",
        "UNITDSPR",
        "VBL",
        "VEDL",
        "WIPRO",
        "ZOMATO",
        "ZYDUSLIFE"
    ]


    for company in required_companies:

        if company not in df["id"].values:

            new_row = {
                col: None
                for col in df.columns
            }

            new_row["id"] = company
            new_row["company_name"] = company


            df = pd.concat(
                [
                    df,
                    pd.DataFrame([new_row])
                ],
                ignore_index=True
            )


    return df



def load_table(conn, file_name, table_name):

    file_path = DATA_DIR / file_name


    df = clean_excel(file_path)


    if table_name == "companies":

        df = fix_companies(df)


    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )


    print(
        table_name,
        "loaded:",
        len(df),
        "rows"
    )



if __name__ == "__main__":


    conn = create_connection()


    tables = {

        "companies.xlsx": "companies",

        "profitandloss.xlsx": "profitandloss",

        "balancesheet.xlsx": "balancesheet",

        "cashflow.xlsx": "cashflow",

        "analysis.xlsx": "analysis",

        "financial_ratios.xlsx": "financial_ratios",

        "stock_prices.xlsx": "stock_prices",

        "documents.xlsx": "documents",

        "prosandcons.xlsx": "prosandcons",

        "sectors.xlsx": "sectors",

        "peer_groups.xlsx": "peer_groups",

        "market_cap.xlsx": "market_cap"

    }



    for file, table in tables.items():

        load_table(
            conn,
            file,
            table
        )


    conn.close()


    print("ETL LOAD COMPLETE")
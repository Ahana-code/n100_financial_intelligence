import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def fetch_dataframe(query, params=None):
    conn = get_connection()

    if params is None:
        df = pd.read_sql(query, conn)
    else:
        df = pd.read_sql(query, conn, params=params)

    conn.close()
    return df


def fetch_companies():
    return fetch_dataframe(
        "SELECT * FROM companies"
    )


def fetch_company(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        (company_id,),
    )


def fetch_ratios(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,),
    )


def fetch_profit(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,),
    )


def fetch_balance(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,),
    )


def fetch_cashflow(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,),
    )


def fetch_analysis(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM analysis
        WHERE company_id=?
        """,
        (company_id,),
    )


def fetch_pros(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM prosandcons
        WHERE company_id=?
        """,
        (company_id,),
    )


def fetch_sector(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM sectors
        WHERE company_id=?
        """,
        (company_id,),
    )


def fetch_peer_group(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM peer_groups
        WHERE company_id=?
        """,
        (company_id,),
    )


def fetch_market_cap(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM market_cap
        WHERE company_id=?
        """,
        (company_id,),
    )


def fetch_stock_prices(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM stock_prices
        WHERE company_id=?
        """,
        (company_id,),
    )


def fetch_documents(company_id):
    return fetch_dataframe(
        """
        SELECT *
        FROM documents
        WHERE company_id=?
        """,
        (company_id,),
    )
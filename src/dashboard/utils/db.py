import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


@st.cache_data(ttl=600)
def get_companies():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM companies", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = sqlite3.connect(DB_PATH)

    if year:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        AND year LIKE ?
        """

        df = pd.read_sql(
            query,
            conn,
            params=(ticker, f"%{year}")
        )

    else:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        """

        df = pd.read_sql(
            query,
            conn,
            params=(ticker,)
        )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM profitandloss WHERE company_id=?",
        conn,
        params=(ticker,)
    )

    conn.close()
    return df

@st.cache_data(ttl=600)
def get_pros_cons(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM prosandcons WHERE company_id=?",
        conn,
        params=(ticker,)
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_bs(ticker):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM balancesheet WHERE company_id=?",
        conn,
        params=(ticker,)
    )

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_cf(ticker):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM cashflow WHERE company_id=?",
        conn,
        params=(ticker,)
    )

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sectors():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_peers(group_name):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM peer_groups WHERE peer_group_name=?",
        conn,
        params=(group_name,)
    )

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_years():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT DISTINCT year
        FROM financial_ratios
        ORDER BY year
        """,
        conn
    )

    conn.close()

    return df["year"].tolist()


@st.cache_data(ttl=600)
def get_valuation(ticker):
    conn = sqlite3.connect(DB_PATH)

    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table'",
        conn
    )

    if "valuation" not in tables["name"].values:
        conn.close()
        return pd.DataFrame()

    df = pd.read_sql(
        "SELECT * FROM valuation WHERE company_id=?",
        conn,
        params=(ticker,)
    )

    conn.close()
    return df
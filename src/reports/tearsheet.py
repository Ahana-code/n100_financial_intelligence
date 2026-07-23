import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

# ======================================================
# PATHS
# ======================================================

DB_PATH = "db/nifty100.db"

OUTPUT_FOLDER = Path("reports/tearsheets")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

TEMP_FOLDER = Path("reports/temp")
TEMP_FOLDER.mkdir(parents=True, exist_ok=True)

# ======================================================
# DATABASE
# ======================================================

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

# ======================================================
# GENERATED FILES
# ======================================================

pros_cons = pd.read_csv(
    "output/pros_cons_generated.csv"
)

cashflow_info = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)

# ======================================================
# REPORTLAB STYLES
# ======================================================

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]

small_style = styles["Normal"]

# ======================================================
# COLORS
# ======================================================

NAVY = colors.HexColor("#0B3D91")
LIGHTBLUE = colors.HexColor("#EAF3FF")
LIGHTGREEN = colors.HexColor("#EAF7EA")
LIGHTRED = colors.HexColor("#FDECEC")
LIGHTYELLOW = colors.HexColor("#FFF4CC")

# ======================================================
# HELPERS
# ======================================================

def sort_year(df):

    if "year" not in df.columns:
        return df

    return df.sort_values("year")


def latest(df):

    df = sort_year(df)

    if len(df) == 0:
        return None

    return df.iloc[-1]


def get_company_data(ticker):

    return {

        "company":
            companies[
                companies["id"] == ticker
            ].iloc[0],

        "profit":
            profit[
                profit.company_id == ticker
            ].copy(),

        "balance":
            balance[
                balance.company_id == ticker
            ].copy(),

        "cashflow":
            cashflow[
                cashflow.company_id == ticker
            ].copy(),

        "ratios":
            ratios[
                ratios.company_id == ticker
            ].copy(),

        "pros":
            pros_cons[
                (pros_cons.company_id == ticker)
                &
                (pros_cons.type == "pro")
            ].copy(),

        "cons":
            pros_cons[
                (pros_cons.company_id == ticker)
                &
                (pros_cons.type == "con")
            ].copy(),

        "cashflow_info":
            cashflow_info[
                cashflow_info.company_id == ticker
            ].copy()

    }

print("Part 1 Loaded Successfully")

# ======================================================
# CHART FUNCTIONS
# ======================================================

def revenue_chart(df, ticker):

    if df.empty:
        return None

    chart = df.copy()

    chart["sales"] = pd.to_numeric(chart["sales"], errors="coerce")
    chart = chart.dropna(subset=["sales"])

    chart["year"] = (
        chart["year"]
        .astype(str)
        .str.extract(r'(\d{2,4})')[0]
    )

    # FIX: turn year into a real number and sort so charts
    # read left-to-right in correct time order
    chart["year"] = pd.to_numeric(chart["year"], errors="coerce")

    # FIX: drop rows where year couldn't be parsed (was NaN),
    # otherwise .astype(int) below crashes
    chart = chart.dropna(subset=["year"])
    chart["year"] = chart["year"].astype(int)

    chart = chart.sort_values("year").tail(10)

    fig, ax = plt.subplots(figsize=(6,3))
    fig.set_layout_engine(None)

    x = list(range(len(chart)))

    ax.bar(
        x,
        chart["sales"].values,
        color="#4F81BD"
    )

    ax.set_title("Revenue (10 Years)")
    ax.set_xticks(x)
    ax.set_xticklabels(
        chart["year"].astype(str),
        rotation=45,
        fontsize=8
    )

    path = TEMP_FOLDER / f"{ticker}_revenue.png"

    fig.canvas.draw()
    fig.savefig(path, dpi=100)

    plt.close(fig)

    return str(path)


# ======================================================

def profit_chart(df, ticker):

    if df.empty:
        return None

    chart = df.copy()

    chart["net_profit"] = pd.to_numeric(
        chart["net_profit"],
        errors="coerce"
    )

    chart = chart.dropna(subset=["net_profit"])

    chart["year"] = (
        chart["year"]
        .astype(str)
        .str.extract(r'(\d{2,4})')[0]
    )

    # FIX: numeric year + sort + keep last 10 years
    chart["year"] = pd.to_numeric(chart["year"], errors="coerce")
    chart = chart.dropna(subset=["year"])
    chart["year"] = chart["year"].astype(int)
    chart = chart.sort_values("year").tail(10)

    fig, ax = plt.subplots(figsize=(6,3))
    fig.set_layout_engine(None)

    x = list(range(len(chart)))

    ax.bar(
        x,
        chart["net_profit"].values,
        color="#9BBB59"
    )

    ax.set_title("Net Profit (10 Years)")

    ax.set_xticks(x)
    ax.set_xticklabels(
        chart["year"].astype(str),
        rotation=45,
        fontsize=8
    )

    path = TEMP_FOLDER / f"{ticker}_profit.png"

    fig.canvas.draw()
    fig.savefig(path, dpi=100)

    plt.close(fig)

    return str(path)


# ======================================================

def roe_roce_chart(company, ratio_df, ticker):

    if ratio_df.empty:
        return None

    chart = ratio_df.copy()

    chart["return_on_equity_pct"] = pd.to_numeric(
        chart["return_on_equity_pct"],
        errors="coerce"
    )

    chart = chart.dropna(subset=["return_on_equity_pct"])

    chart["year"] = (
        chart["year"]
        .astype(str)
        .str.extract(r'(\d{2,4})')[0]
    )

    # FIX: numeric year + sort + keep last 10 years
    chart["year"] = pd.to_numeric(chart["year"], errors="coerce")
    chart = chart.dropna(subset=["year"])
    chart["year"] = chart["year"].astype(int)
    chart = chart.sort_values("year").tail(10)

    fig, ax = plt.subplots(figsize=(6,3))
    fig.set_layout_engine(None)

    x = list(range(len(chart)))

    ax.plot(
        x,
        chart["return_on_equity_pct"].values,
        marker="o",
        linewidth=2,
        label="ROE"
    )

    # roce comes from the company row, so make sure it's numeric too
    roce_value = pd.to_numeric(company["roce_percentage"], errors="coerce")
    roce_value = 0 if pd.isna(roce_value) else roce_value

    roce = [roce_value] * len(chart)

    ax.plot(
        x,
        roce,
        linestyle="--",
        linewidth=2,
        label="ROCE"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(
        chart["year"].astype(str),
        rotation=45,
        fontsize=8
    )

    ax.legend()

    path = TEMP_FOLDER / f"{ticker}_roe_roce.png"

    fig.canvas.draw()
    fig.savefig(path, dpi=100)

    plt.close(fig)

    return str(path)

# ======================================================

def balance_sheet_chart(df, ticker):

    if df.empty:
        return None

    chart = df.copy()

    # convert these to real numbers before plotting,
    # otherwise matplotlib can hang trying to stack text values
    for col in ["equity_capital", "borrowings", "other_liabilities"]:
        chart[col] = pd.to_numeric(chart[col], errors="coerce").fillna(0)

    chart["year"] = (
        chart["year"]
        .astype(str)
        .str.extract(r'(\d{2,4})')[0]
    )

    # FIX: numeric year, drop unparseable rows, THEN convert to int
    chart["year"] = pd.to_numeric(chart["year"], errors="coerce")
    chart = chart.dropna(subset=["year"])
    chart["year"] = chart["year"].astype(int)
    chart = chart.sort_values("year").tail(10)

    fig, ax = plt.subplots(figsize=(6,3))
    fig.set_layout_engine(None)

    x = list(range(len(chart)))

    ax.bar(
        x,
        chart["equity_capital"].values,
        label="Equity"
    )

    ax.bar(
        x,
        chart["borrowings"].values,
        bottom=chart["equity_capital"].values,
        label="Borrowings"
    )

    bottom = (
        chart["equity_capital"] +
        chart["borrowings"]
    )

    ax.bar(
        x,
        chart["other_liabilities"].values,
        bottom=bottom.values,
        label="Other Liabilities"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(
        chart["year"].astype(str),
        rotation=45,
        fontsize=8
    )

    ax.legend(fontsize=8)

    path = TEMP_FOLDER / f"{ticker}_balance.png"

    fig.canvas.draw()
    fig.savefig(path, dpi=100)

    plt.close(fig)

    return str(path)

# ======================================================

def cashflow_waterfall(df, ticker):

    if df.empty:
        return None

    latest_cf = latest(df)

    # FIX: convert these four values to real numbers first
    op = pd.to_numeric(latest_cf["operating_activity"], errors="coerce")
    inv = pd.to_numeric(latest_cf["investing_activity"], errors="coerce")
    fin = pd.to_numeric(latest_cf["financing_activity"], errors="coerce")
    net = pd.to_numeric(latest_cf["net_cash_flow"], errors="coerce")

    labels = [
        "Operating",
        "Investing",
        "Financing",
        "Net"
    ]

    values = [op, inv, fin, net]
    values = [0 if pd.isna(v) else v for v in values]

    colors_list = [

        "green" if v >= 0 else "red"

        for v in values

    ]

    fig, ax = plt.subplots(figsize=(5,3))
    fig.set_layout_engine(None)

    ax.bar(

        labels,

        values,

        color=colors_list

    )

    ax.axhline(0, color="black")

    path = TEMP_FOLDER / f"{ticker}_cashflow.png"

    fig.canvas.draw()
    fig.savefig(path, dpi=100)

    plt.close(fig)

    return str(path)

# ======================================================
# PDF COMPONENTS
# ======================================================

def build_header(company):

    header = Table(

        [[

            Paragraph(

                f"""
                <font color='white' size=18>
                <b>{company['company_name']}</b><br/>
                {company['id']}
                </font>
                """

            )

        ]],

        colWidths=[7.3*inch]

    )

    header.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),NAVY),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

            ("BOTTOMPADDING",(0,0),(-1,-1),18),

            ("TOPPADDING",(0,0),(-1,-1),18)

        ])

    )

    return header


# ======================================================

def build_kpi_tiles(ratio):

    r = latest(ratio)

    cards = [

        [

            "ROE",

            f"{r['return_on_equity_pct']:.2f}%"

        ],

        [

            "Debt / Equity",

            f"{r['debt_to_equity']:.2f}"

        ],

        [

            "Interest Coverage",

            f"{r['interest_coverage']:.2f}"

        ],

        [

            "Net Profit Margin",

            f"{r['net_profit_margin_pct']:.2f}%"

        ],

        [

            "Free Cash Flow",

            f"{r['free_cash_flow_cr']:.2f} Cr"

        ],

        [

            "EPS",

            f"{r['earnings_per_share']:.2f}"

        ]

    ]

    rows = []

    idx = 0

    for i in range(2):

        row = []

        for j in range(3):

            title = cards[idx][0]

            value = cards[idx][1]

            box = Table(

                [[

                    Paragraph(

                        f"<b>{title}</b><br/><font size=14>{value}</font>",

                        normal_style

                    )

                ]],

                colWidths=[2.2*inch]

            )

            box.setStyle(

                TableStyle([

                    ("BACKGROUND",(0,0),(-1,-1),LIGHTBLUE),

                    ("BOX",(0,0),(-1,-1),1,NAVY),

                    ("ALIGN",(0,0),(-1,-1),"CENTER"),

                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

                    ("TOPPADDING",(0,0),(-1,-1),12),

                    ("BOTTOMPADDING",(0,0),(-1,-1),12)

                ])

            )

            row.append(box)

            idx += 1

        rows.append(row)

    return Table(rows)


# ======================================================

def build_pros_cons(title, dataframe, bg):

    story = []

    heading = Table(

        [[title]],

        colWidths=[7.2*inch]

    )

    heading.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),bg),

            ("BOX",(0,0),(-1,-1),1,colors.black),

            ("BOTTOMPADDING",(0,0),(-1,-1),6),

            ("TOPPADDING",(0,0),(-1,-1),6)

        ])

    )

    story.append(heading)

    for _, row in dataframe.iterrows():

        story.append(

            Paragraph(

                f"• {row['text']}",

                small_style

            )

        )

    story.append(Spacer(1,8))

    return story


# ======================================================

def build_capital_badge(info):

    if len(info) == 0:

        return Paragraph("No Capital Allocation Data", normal_style)

    label = info.iloc[0]["capital_allocation_label"]

    badge = Table(

        [[

            Paragraph(

                f"<b>{label}</b>",

                heading_style

            )

        ]],

        colWidths=[3.5*inch]

    )

    badge.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),LIGHTYELLOW),

            ("BOX",(0,0),(-1,-1),1,colors.black),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("TOPPADDING",(0,0),(-1,-1),10),

            ("BOTTOMPADDING",(0,0),(-1,-1),10)

        ])

    )

    return badge


print("Part 3 Loaded Successfully")

# ======================================================
# BUILD COMPLETE 2 PAGE TEARSHEET
# ======================================================

def build_tearsheet(ticker):

    data = get_company_data(ticker)

    company = data["company"]

    profit_df = data["profit"]

    balance_df = data["balance"]

    cash_df = data["cashflow"]

    ratio_df = data["ratios"]

    pros_df = data["pros"]

    cons_df = data["cons"]

    cashflow_df = data["cashflow_info"]


    pdf = OUTPUT_FOLDER / f"{ticker}_tearsheet.pdf"

    doc = SimpleDocTemplate(

        str(pdf),

        pagesize=(8.27*inch,11.69*inch),

        rightMargin=20,

        leftMargin=20,

        topMargin=20,

        bottomMargin=20

    )

    story = []

    # =====================================================
    # PAGE 1
    # =====================================================

    story.append(

        build_header(company)

    )

    story.append(

        Spacer(1,18)

    )

    story.append(

        build_kpi_tiles(ratio_df)

    )

    story.append(

        Spacer(1,20)

    )

    revenue = revenue_chart(

        profit_df,

        ticker

    )

    profit = profit_chart(

        profit_df,

        ticker

    )

    roe = roe_roce_chart(

        company,

        ratio_df,

        ticker

    )

    chart_table = Table(

        [

            [

                Image(

                    revenue,

                    width=3.2*inch,

                    height=2.1*inch

                ),

                Image(

                    profit,

                    width=3.2*inch,

                    height=2.1*inch

                )

            ],

            [

                Image(

                    roe,

                    width=6.5*inch,

                    height=2.5*inch

                ),

                ""

            ]

        ]

    )

    chart_table.setStyle(

        TableStyle([

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE")

        ])

    )

    story.append(

        chart_table

    )

    story.append(

        PageBreak()

    )

    # =====================================================
    # PAGE 2
    # =====================================================

    story.append(

        Paragraph(

            "<b>Balance Sheet & Cash Flow Intelligence</b>",

            heading_style

        )

    )

    story.append(

        Spacer(1,10)

    )

    balance_chart = balance_sheet_chart(

        balance_df,

        ticker

    )

    cash_chart = cashflow_waterfall(

        cash_df,

        ticker

    )

    chart_table = Table(

        [

            [

                Image(

                    balance_chart,

                    width=3.2*inch,

                    height=2.3*inch

                ),

                Image(

                    cash_chart,

                    width=3.2*inch,

                    height=2.3*inch

                )

            ]

        ]

    )

    story.append(

        chart_table

    )

    story.append(

        Spacer(1,15)

    )

    # =====================================================
    # PROS
    # =====================================================

    for item in build_pros_cons(

        "Pros",

        pros_df,

        LIGHTGREEN

    ):

        story.append(item)

    # =====================================================
    # CONS
    # =====================================================

    for item in build_pros_cons(

        "Cons",

        cons_df,

        LIGHTRED

    ):

        story.append(item)

    story.append(

        Spacer(1,10)

    )

    # =====================================================
    # CAPITAL ALLOCATION
    # =====================================================

    story.append(

        Paragraph(

            "<b>Capital Allocation Pattern</b>",

            heading_style

        )

    )

    story.append(

        build_capital_badge(

            cashflow_df

        )

    )

    doc.build(story)

    return True


print("Part 4 Loaded Successfully")

# =====================================================
# BATCH GENERATION
# =====================================================
# STEP 1: Test on just 5 companies first.
# Once these 5 PDFs generate correctly, comment out
# "test_companies" below and uncomment the full
# "company_ids" loop to run all companies.
# =====================================================

conn = sqlite3.connect(DB_PATH)

skipped = []

generated = 0

company_df = pd.read_sql(
    "SELECT id FROM companies ORDER BY id",
    conn
)

company_ids = company_df["id"]

#test_companies = [
 #   "TCS",
 #   "HDFCBANK",
 #   "RELIANCE",
 #   "SUNPHARMA",
 #   "TATASTEEL"
#] 

#company_ids = test_companie

# Full list — switch to this once the 5 test companies work fine
# company_df = pd.read_sql(
#     "SELECT id FROM companies ORDER BY id",
#     conn
# )
# company_ids = company_df["id"]



for ticker in company_ids:

    print("Generating", ticker)

    years = pd.read_sql(

        """
        SELECT year
        FROM profitandloss
        WHERE company_id=?
        """,

        conn,

        params=(ticker,)
    )

    if len(years) < 3:

        skipped.append({

            "company_id": ticker,

            "reason": "Less than 3 years data"

        })

        continue

    try:

        build_tearsheet(ticker)

        generated += 1

    except Exception as e:

        skipped.append({

            "company_id": ticker,

            "reason": str(e)

        })

if skipped:

    pd.DataFrame(skipped).to_csv(

        "output/skipped_tearsheets.csv",

        index=False

    )

print("=" * 50)

print("Company Tearsheet Generation Completed")

print("=" * 50)

print()

print(f"Generated : {generated}")

print(f"Skipped   : {len(skipped)}")

print()

print("Output Folder")

print(OUTPUT_FOLDER)

conn.close()
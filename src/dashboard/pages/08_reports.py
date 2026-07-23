import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📑 Reports & Downloads")

st.markdown("Download all generated analytics reports.")

OUTPUT = Path("output")
REPORTS = Path("reports")

files = [
    ("Stock Screener", OUTPUT / "screener_output.xlsx"),
    ("Peer Comparison", OUTPUT / "peer_comparison.xlsx"),
    ("Cashflow Intelligence", OUTPUT / "cashflow_intelligence.xlsx"),
    ("Company Clusters", OUTPUT / "company_clusters.xlsx"),
    ("Company Health Score", OUTPUT / "company_health_score.xlsx"),
    ("Revenue Forecast", OUTPUT / "revenue_forecast.xlsx"),
    ("Investment Recommendation", OUTPUT / "investment_recommendation.xlsx"),
    ("Backtest Validation", OUTPUT / "backtest_validation.xlsx"),
]

st.subheader("Excel Reports")

for title, file in files:

    if file.exists():

        with open(file, "rb") as f:
            st.download_button(
                label=f"⬇ Download {title}",
                data=f,
                file_name=file.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    else:

        st.warning(f"{title} not found.")

st.divider()

st.subheader("Charts")

chart_files = [
    ("Cluster Distribution", REPORTS / "cluster_distribution.png"),
    ("Revenue Forecast", REPORTS / "revenue_forecast.png"),
]

for title, chart in chart_files:

    if chart.exists():

        st.markdown(f"### {title}")
        st.image(str(chart), use_container_width=True)

    else:

        st.info(f"{title} chart not available.")

st.divider()

st.subheader("Quick Preview")

preview_files = {
    "Company Health Score": OUTPUT / "company_health_score.xlsx",
    "Investment Recommendation": OUTPUT / "investment_recommendation.xlsx",
    "Revenue Forecast": OUTPUT / "revenue_forecast.xlsx",
    "Backtest Validation": OUTPUT / "backtest_validation.xlsx",
}

selected = st.selectbox(
    "Preview Report",
    list(preview_files.keys())
)

file = preview_files[selected]

if file.exists():

    df = pd.read_excel(file)

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

else:

    st.warning("Report not found.")
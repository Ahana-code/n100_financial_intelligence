from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

os.makedirs("docs", exist_ok=True)

styles = getSampleStyleSheet()

# -----------------------------
# Analyst Guide
# -----------------------------

guide = SimpleDocTemplate("docs/analyst_guide.pdf")

story = []

story.append(Paragraph("<b>N100 Financial Intelligence Platform</b>", styles["Title"]))
story.append(Paragraph("Analyst Guide", styles["Heading1"]))

story.append(Paragraph("<b>Purpose</b>", styles["Heading2"]))
story.append(Paragraph(
    "This guide explains how to use the N100 Financial Intelligence Platform "
    "for company analysis, screening, valuation, clustering, dashboards, and reporting.",
    styles["BodyText"]
))

story.append(Paragraph("<b>Major Modules</b>", styles["Heading2"]))
modules = [
    "ETL Pipeline",
    "SQLite Database",
    "Financial Ratios",
    "Stock Screener",
    "Peer Comparison",
    "Radar Charts",
    "Valuation Engine",
    "Cashflow Intelligence",
    "NLP Pros & Cons Generator",
    "Company Tearsheets",
    "Sector Reports",
    "Portfolio Report",
    "Clustering",
    "FastAPI",
    "Streamlit Dashboard"
]

for m in modules:
    story.append(Paragraph("• " + m, styles["BodyText"]))

story.append(Paragraph("<b>Dashboard</b>", styles["Heading2"]))

pages = [
    "Home Dashboard",
    "Company Profile",
    "Stock Screener",
    "Peer Comparison",
    "Financial Trends",
    "Sector Analysis",
    "Capital Allocation",
    "Reports"
]

for p in pages:
    story.append(Paragraph("• " + p, styles["BodyText"]))

story.append(Paragraph("<b>Outputs</b>", styles["Heading2"]))
story.append(Paragraph(
    "Outputs are generated under output/, reports/, and docs/ folders.",
    styles["BodyText"]
))

guide.build(story)

# -----------------------------
# Acceptance Checklist
# -----------------------------

check = SimpleDocTemplate("docs/acceptance_checklist.pdf")

story = []

story.append(Paragraph("<b>Acceptance Checklist</b>", styles["Title"]))

items = [
    "SQLite Database Created",
    "ETL Pipeline Completed",
    "Validation Completed",
    "Financial Ratios Generated",
    "Capital Allocation Generated",
    "Stock Screener Generated",
    "Peer Comparison Generated",
    "Radar Charts Generated",
    "Streamlit Dashboard Working",
    "Valuation Report Generated",
    "Cashflow Intelligence Generated",
    "Pros & Cons Generated",
    "Analysis Parsed",
    "Company Tearsheets Generated",
    "Sector Reports Generated",
    "Portfolio Report Generated",
    "Cluster Labels Generated",
    "FastAPI Server Working",
    "Pytest Report Generated",
    "Analyst Guide Generated",
    "Acceptance Checklist Generated"
]

for item in items:
    story.append(Paragraph("☑ " + item, styles["BodyText"]))

story.append(Paragraph("<br/>Project Status : <b>READY FOR SUBMISSION</b>", styles["Heading2"]))

check.build(story)

print("Done.")
print("docs/analyst_guide.pdf")
print("docs/acceptance_checklist.pdf")
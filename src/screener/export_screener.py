import os
import pandas as pd

from engine import (
    load_data,
    load_config,
    apply_quality_compounder,
    apply_value_pick,
    apply_growth_accelerator,
    apply_dividend_champion,
    apply_debt_free_blue_chip,
    apply_turnaround_watch,
)

os.makedirs("output", exist_ok=True)

df = load_data()
config = load_config()

screeners = {
    "Quality Compounder": apply_quality_compounder(df, config),
    "Value Pick": apply_value_pick(df, config),
    "Growth Accelerator": apply_growth_accelerator(df, config),
    "Dividend Champion": apply_dividend_champion(df),
    "Debt Free Blue Chip": apply_debt_free_blue_chip(df),
    "Turnaround Watch": apply_turnaround_watch(df),
}

writer = pd.ExcelWriter(
    "output/screener_output.xlsx",
    engine="openpyxl"
)

for sheet_name, result in screeners.items():
    result.to_excel(
        writer,
        sheet_name=sheet_name[:31],
        index=False
    )

writer.close()

print("screener_output.xlsx created successfully!")
import os
import json
import pandas as pd

# ----- Paths -----
BASE_DIR = r"C:\Users\rudde\VCF_Research"
REGISTRY_PATH = os.path.join(BASE_DIR, "registry", "vcf_metric_registry.json")
CLEAN_DIR = os.path.join(BASE_DIR, "data_clean")
OUTPUT_PATH = os.path.join(CLEAN_DIR, "macro_monthly_panel.csv")

print("\n🏗  Building VCF macro MONTHLY panel (FRED only)...")

# ----- Load registry -----
with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)

# Keep ONLY FRED-based macro series (skip VIX / SPY / XLU automatically)
macro_ids = []
for metric_id, info in registry.items():
    src = info.get("source", "").upper()
    cat = info.get("category", "").lower()
    if src == "FRED" and cat in {"macro", "labor", "liquidity", "rates"}:
        macro_ids.append(metric_id)

print(f"✔ Using FRED macro metrics: {macro_ids}")

panel = None

# ----- Build monthly panel -----
for metric_id in macro_ids:
    file_path = os.path.join(CLEAN_DIR, f"{metric_id}_normalized.csv")
    if not os.path.exists(file_path):
        print(f"⚠ Skipping {metric_id} – normalized file not found: {file_path}")
        continue

    df = pd.read_csv(file_path, parse_dates=["date"])
    if df.empty:
        print(f"⚠ Skipping {metric_id} – no rows in file.")
        continue

    df = df.set_index("date").sort_index()

    # Whatever the value column is called, map it to the metric_id
    # Always use ONLY the 'value' column for macro panel
    if "value" not in df.columns:
        print(f"⚠ Skipping {metric_id} – no 'value' column found.")
        continue

    df = df[["value"]].rename(columns={"value": metric_id})


    # Resample to month-end (works even if it's already monthly)
    df_m = df.resample("M").last()

    if panel is None:
        panel = df_m
    else:
        panel = panel.join(df_m, how="outer")

# Drop rows where *all* macro series are NaN
panel = panel.dropna(how="all")

# Save
panel.to_csv(OUTPUT_PATH, index_label="date")

print(f"\n🎉 Macro monthly panel COMPLETE.")
print(f"   Saved to: {OUTPUT_PATH}")
print(f"   Rows: {len(panel):,}  |  Columns: {list(panel.columns)}\n")

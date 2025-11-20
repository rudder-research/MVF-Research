# ============================================================
# VCF Research - Unified Data Loader (Colab + Windows Safe)
# ============================================================

import os
import json
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import datetime

# ------------------------------------------------------------
# Dynamic BASE_DIR: works on Colab, Linux, Windows
# ------------------------------------------------------------
if "__file__" in globals():
    BASE_DIR = Path(__file__).resolve().parents[1]
else:
    BASE_DIR = Path("/content/VCF-RESEARCH")

REGISTRY_PATH = BASE_DIR / "registry" / "vcf_metric_registry.json"
DATA_RAW = BASE_DIR / "data_raw"
DATA_RAW.mkdir(exist_ok=True, parents=True)

print("Using BASE_DIR:", BASE_DIR)
print("Registry:", REGISTRY_PATH)

# ------------------------------------------------------------
# Load registry
# ------------------------------------------------------------
def load_registry():
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Registry missing at: {REGISTRY_PATH}")
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

# ------------------------------------------------------------
# Fetchers
# ------------------------------------------------------------
def fetch_fred_series(ticker):
    """Uses public CSV endpoint—no API key needed."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={ticker}"
    df = pd.read_csv(url)
    df.rename(columns={df.columns[0]: "date", df.columns[1]: "value"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna()
    df.set_index("date", inplace=True)
    return df


def fetch_yahoo_series(ticker):
    df = yf.download(ticker, start="1990-01-01", auto_adjust=True, progress=False)

    if df.empty:
        raise ValueError(f"No data from Yahoo for {ticker}")

    col = None
    for c in ["Adj Close", "Close", "Price"]:
        if c in df.columns:
            col = c
            break

    if not col:
        raise ValueError(f"No usable price column from Yahoo for {ticker}")

    df = df[[col]].rename(columns={col: "value"})
    df.index.name = "date"
    df = df.dropna()
    return df

# ------------------------------------------------------------
# Main loader
# ------------------------------------------------------------
def load_all_metrics():
    registry = load_registry()
    print(f"\n🚀 Loading {len(registry)} metrics...\n")

    for metric_id, meta in registry.items():
        src = meta["source"].upper()
        ticker = meta["ticker"]
        out_path = DATA_RAW / f"{metric_id}.csv"

        print(f"📡 {metric_id} → {src} ({ticker})")

        if src == "FRED":
            df = fetch_fred_series(ticker)
        elif src == "YAHOO":
            df = fetch_yahoo_series(ticker)
        else:
            print(f"⚠ Unsupported source {src} — skipping")
            continue

        df.to_csv(out_path)
        print(f"✔ Saved {len(df)} rows to {out_path}")

    print("\n🎉 Data loading complete!")


# ------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------
if __name__ == "__main__":
    load_all_metrics()

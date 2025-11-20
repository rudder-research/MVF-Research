import os
import json
import pandas as pd
from pathlib import Path
from fredapi import Fred
import yfinance as yf

# ======================================================
# Dynamic Paths — WORKS BOTH IN COLAB AND ON PC
# ======================================================
BASE_DIR = Path(os.getcwd())
REGISTRY_PATH = BASE_DIR / "registry" / "vcf_metric_registry.json"
DATA_RAW = BASE_DIR / "data_raw"

# Ensure folders exist
DATA_RAW.mkdir(exist_ok=True, parents=True)

# ======================================================
# Load Registry
# ======================================================
def load_registry():
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Registry missing: {REGISTRY_PATH}")
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

# ======================================================
# FRED fetcher
# ======================================================
fred_api_key = os.getenv("FRED_API_KEY")
fred = Fred(api_key=fred_api_key)

def fetch_fred_series(ticker: str) -> pd.DataFrame:
    s = fred.get_series(ticker)
    df = s.to_frame("value")
    df.index.name = "date"
    return df

# ======================================================
# Yahoo fetcher
# ======================================================
def fetch_yahoo_series(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, progress=False)

    if df.empty:
        raise ValueError(f"Yahoo returned no data for {ticker}")

    # Clean price column
    if "Adj Close" in df.columns:
        df = df[["Adj Close"]].rename(columns={"Adj Close": "value"})
    else:
        df = df[["Close"]].rename(columns={"Close": "value"})

    df.index.name = "date"
    df = df[~df.index.duplicated(keep="last")]
    return df

# ======================================================
# Main loader
# ======================================================
def load_all_metrics():
    registry = load_registry()

    print("\n🚀 Starting full VCF data load...\n")

    for metric_id, meta in registry.items():
        src = meta["source"].upper()
        ticker = meta["ticker"]

        print(f"📡 Fetching {metric_id}: {meta['display_name']} ({src})")

        if src == "FRED":
            df = fetch_fred_series(ticker)
        elif src == "YAHOO":
            df = fetch_yahoo_series(ticker)
        else:
            print(f"⚠ Unsupported source '{src}', skipping…")
            continue

        out_path = DATA_RAW / f"{metric_id}.csv"

        # 🚨 THE FIX — always write a clean date column
        df.reset_index().rename(columns={"index": "date"}).to_csv(out_path, index=False)

        print(f"✔ Saved → {out_path} ({len(df)} rows)\n")

# ======================================================
# Execute script
# ======================================================
if __name__ == "__main__":
    load_all_metrics()

import os
import json
import pandas as pd
import yfinance as yf
import requests

# ======================================================
# PATHS
# ======================================================
BASE_DIR = r"C:\Users\rudde\VCF_Research"
REGISTRY_PATH = r"C:\Users\rudde\VCF_Research\registry\vcf_metric_registry.json"
RAW_DIR = os.path.join(BASE_DIR, "data_raw")

os.makedirs(RAW_DIR, exist_ok=True)


# ======================================================
# LOAD THE METRIC REGISTRY
# ======================================================
def load_registry():
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)
    return registry


# ======================================================
# FETCHERS
# ======================================================
def fetch_fred_series(ticker):
    """
    Downloads data from FRED using their open CSV endpoint.
    """
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={ticker}"
    df = pd.read_csv(url)

    # standardize
    df.rename(columns={df.columns[0]: "date", df.columns[1]: "value"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df.set_index("date", inplace=True)

    return df


def fetch_yahoo_series(ticker):
    # Download full history since 1990
    df = yf.download(
        ticker,
        start="1990-01-01",
        progress=False,
        auto_adjust=True
    )

    if df.empty:
        raise ValueError(f"Yahoo returned no data for ticker: {ticker}")

    # Pick correct price column in order of priority
    if "Adj Close" in df.columns:
        df = df[["Adj Close"]].rename(columns={"Adj Close": "value"})
    elif "Close" in df.columns:
        df = df[["Close"]].rename(columns={"Close": "value"})
    elif "Price" in df.columns:
        df = df[["Price"]].rename(columns={"Price": "value"})
    else:
        raise ValueError(f"No usable price column found for {ticker}: {df.columns.tolist()}")

    df.index.name = "date"
    df = df.dropna()

    return df



# ======================================================
# LOAD A SINGLE METRIC
# ======================================================
def load_metric(metric_id, info):
    source = info["source"]
    ticker = info["ticker"]

    print(f"\n📡 Fetching {metric_id}: {info['display_name']}  (Source: {source})")

    try:
        if source == "FRED":
            df = fetch_fred_series(ticker)
        elif source == "YAHOO":
            df = fetch_yahoo_series(ticker)
        else:
            print(f"❌ Unknown source type for {metric_id}")
            return

        # Save data
        save_path = os.path.join(RAW_DIR, f"{metric_id}.csv")
        df.to_csv(save_path)

        print(f"✔ Saved to {save_path}  ({len(df)} rows)")

    except Exception as e:
        print(f"❌ Error fetching {metric_id}: {e}")


# ======================================================
# RUN ALL METRICS
# ======================================================
def load_all_metrics():
    registry = load_registry()

    print("\n🚀 Starting full VCF data load...")
    print("✔ Metrics found:", len(registry))

    for metric_id, info in registry.items():
        load_metric(metric_id, info)

    print("\n🎉 Data load COMPLETE.\n")


# ======================================================
# MAIN
# ======================================================
if __name__ == "__main__":
    load_all_metrics()

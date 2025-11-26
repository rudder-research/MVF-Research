import os
import json
import pandas as pd
import numpy as np

# =========================================
# PATHS
# =========================================
BASE_DIR = r"C:\Users\rudde\VCF_Research"
REGISTRY_PATH = os.path.join(BASE_DIR, "registry", "vcf_metric_registry.json")
RAW_DIR = os.path.join(BASE_DIR, "data_raw")
CLEAN_DIR = os.path.join(BASE_DIR, "data_clean")

os.makedirs(CLEAN_DIR, exist_ok=True)


# =========================================
# HELPERS
# =========================================
def load_registry():
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def zscore(series: pd.Series) -> pd.Series:
    mu = series.mean()
    sigma = series.std(ddof=0)
    if sigma == 0 or np.isnan(sigma):
        return pd.Series(index=series.index, dtype=float)
    return (series - mu) / sigma


def rolling_zscore(series: pd.Series, window: int) -> pd.Series:
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std(ddof=0)
    z = (series - rolling_mean) / rolling_std
    return z


def infer_window(freq: str) -> int:
    """Choose a rolling window size based on stated frequency."""
    f = (freq or "").lower()
    if f.startswith("d"):
        return 252   # ~1 year of trading days
    if f.startswith("w"):
        return 52    # ~1 year of weeks
    if f.startswith("m"):
        return 36    # ~3 years of months
    if f.startswith("q"):
        return 20    # ~5 years of quarters
    return 60        # fallback


def infer_growth_periods(freq: str) -> int:
    """Choose periods for YoY-like growth."""
    f = (freq or "").lower()
    if f.startswith("q"):
        return 4     # 4 quarters ~ 1 year
    if f.startswith("m"):
        return 12    # 12 months
    if f.startswith("w"):
        return 52    # 52 weeks
    if f.startswith("d"):
        return 252   # 1-year trading days (rough)
    return 12        # fallback


# =========================================
# NORMALIZATION LOGIC PER METRIC
# =========================================
def normalize_metric(metric_id: str, info: dict) -> pd.DataFrame:
    """Load raw metric from CSV, normalize, and return DataFrame with
    columns: ['value', 'norm'] indexed by date.
    """
    raw_path = os.path.join(RAW_DIR, f"{metric_id}.csv")
    if not os.path.exists(raw_path):
        print(f"❌ Raw file missing for {metric_id}: {raw_path}")
        return pd.DataFrame()

    df = pd.read_csv(raw_path)
    # Expecting 'date' and 'value' columns
    if "date" not in df.columns or "value" not in df.columns:
        print(f"❌ Unexpected columns in {metric_id}: {df.columns.tolist()}")
        return pd.DataFrame()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.set_index("date").sort_index()
    df = df[["value"]].copy()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])

    norm_type = info.get("normalization", "zscore")
    freq = info.get("frequency", "Daily")
    direction = info.get("direction", "+")

    norm = None

    # ---- Different normalization types ----
    if norm_type == "growth_positive":
        # Convert to YoY-like growth, then z-score that growth
        periods = infer_growth_periods(freq)
        growth = df["value"].pct_change(periods=periods)
        norm = zscore(growth)
        df["value"] = growth

    elif norm_type == "zscore_rolling":
        window = infer_window(freq)
        norm = rolling_zscore(df["value"], window=window)

    elif norm_type in ("zscore", "inverse_zscore"):
        norm = zscore(df["value"])

    else:
        # Fallback: simple z-score
        norm = zscore(df["value"])

    # Direction handling:
    # "+" means higher = more "risk-on" (leave as is)
    # "-" means higher = more "risk-off" (flip sign so VCF sees it consistently)
    if direction == "-":
        norm = -norm

    df["norm"] = norm

    return df


# =========================================
# MAIN: NORMALIZE ALL METRICS & BUILD PANEL
# =========================================
def normalize_all_metrics():
    registry = load_registry()
    print("\n🔧 Starting normalization engine...")
    print("✔ Metrics in registry:", len(registry))

    panel = None

    for metric_id, info in registry.items():
        display_name = info.get("display_name", metric_id)
        print(f"\n📐 Normalizing {metric_id}: {display_name}")

        df_norm = normalize_metric(metric_id, info)

        if df_norm.empty:
            print(f"⚠ No data after normalization for {metric_id}, skipping.")
            continue

        # Save individual normalized series
        out_path = os.path.join(CLEAN_DIR, f"{metric_id}_normalized.csv")
        df_norm.to_csv(out_path)
        print(f"✔ Saved normalized metric to: {out_path} ({len(df_norm)} rows)")

        # Build combined panel of norm values
        series_norm = df_norm["norm"].rename(metric_id)

        if panel is None:
            panel = series_norm.to_frame()
        else:
            panel = panel.join(series_norm, how="outer")

    if panel is not None:
        panel = panel.sort_index()
        panel_out = os.path.join(CLEAN_DIR, "normalized_panel.csv")
        panel.to_csv(panel_out)
        print(f"\n🧱 Combined normalized panel saved to: {panel_out}")
        print("   Columns:", list(panel.columns))
        print("   Rows:", len(panel))
    else:
        print("\n❌ No metrics were normalized; panel not created.")


if __name__ == "__main__":
    normalize_all_metrics()
    print("\n🎉 Normalization engine COMPLETE.\n")

import os
import json
import numpy as np
import pandas as pd

# Correct path
BASE_DIR = "/content/drive/MyDrive/VCF_Research"
REGISTRY_PATH = os.path.join(BASE_DIR, "registry", "vcf_metric_registry.json")
PANEL_PATH = os.path.join(BASE_DIR, "data_clean", "normalized_panel.csv")
OUT_DIR = os.path.join(BASE_DIR, "geometry")
os.makedirs(OUT_DIR, exist_ok=True)

print("\n🧮 Starting VCF geometry engine (Option C: long + full)...")


# ---------- Load data ----------
if not os.path.exists(PANEL_PATH):
    raise FileNotFoundError(f"Normalized panel not found at: {PANEL_PATH}")

panel = pd.read_csv(PANEL_PATH, parse_dates=["date"])
panel = panel.set_index("date").sort_index()

with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)

print(f"✔ Loaded normalized panel with {panel.shape[0]} rows and {panel.shape[1]} metrics")
print(f"✔ Registry metrics: {len(registry)}")

# ---------- Helper: group metrics by category ----------
def metric_ids_for(categories):
    return [
        metric_id
        for metric_id, info in registry.items()
        if info.get("category") in categories and metric_id in panel.columns
    ]

macro_like_cats = {"Macro", "Labor", "Rates"}
liquidity_cats = {"Liquidity", "Rates"}
risk_cats = {"Volatility"}
equity_cats = {"Equities"}

macro_metrics = metric_ids_for(macro_like_cats)
liquidity_metrics = metric_ids_for(liquidity_cats)
risk_metrics = metric_ids_for(risk_cats)
equity_metrics = metric_ids_for(equity_cats)

print("\n📌 Metric groups used:")
print("  Macro-like     :", macro_metrics)
print("  Liquidity-like :", liquidity_metrics)
print("  Risk (vol)     :", risk_metrics)
print("  Equity         :", equity_metrics)

if not macro_metrics or not liquidity_metrics:
    raise RuntimeError("Need at least one macro and one liquidity metric for geometry.")

# ---------- Build pillar scores ----------
scores = pd.DataFrame(index=panel.index)

scores["macro_score"] = panel[macro_metrics].mean(axis=1, skipna=True)
scores["liquidity_score"] = panel[liquidity_metrics].mean(axis=1, skipna=True)
scores["risk_score"] = (
    panel[risk_metrics].mean(axis=1, skipna=True) if risk_metrics else np.nan
)
scores["equity_score"] = (
    panel[equity_metrics].mean(axis=1, skipna=True) if equity_metrics else np.nan
)

# ---------- Helper: z-score ----------
def zscore(series: pd.Series) -> pd.Series:
    s = series.dropna()
    if s.empty or s.std(ddof=0) == 0:
        return series * np.nan
    z = (series - s.mean()) / s.std(ddof=0)
    return z

# ---------- A) Long macro-only geometry (1915+ if data exists) ----------
macro_z = zscore(scores["macro_score"])
liq_z = zscore(scores["liquidity_score"])

theta_long = np.degrees(np.arctan2(macro_z, liq_z))
coherence_long = np.sqrt(macro_z**2 + liq_z**2)

geo_long = pd.DataFrame(
    {
        "macro_score": scores["macro_score"],
        "liquidity_score": scores["liquidity_score"],
        "theta_macro_deg": theta_long,
        "coherence_macro": coherence_long,
    },
    index=scores.index,
)

long_path = os.path.join(OUT_DIR, "vcf_geometry_long_macro.csv")
geo_long.to_csv(long_path, index_label="date")
print(f"\n📜 Long macro geometry saved: {long_path}")
print(
    f"   Rows: {geo_long.shape[0]} "
    f"(theta valid from: {geo_long['theta_macro_deg'].first_valid_index()})"
)

# ---------- B) Full 4-pillar geometry (only where equity + risk exist) ----------
mask_full = scores["risk_score"].notna() & scores["equity_score"].notna()

if mask_full.sum() == 0:
    print("\n⚠ No overlapping dates with risk + equity. Full geometry not computed.")
else:
    macro_z_f = zscore(scores.loc[mask_full, "macro_score"])
    liq_z_f = zscore(scores.loc[mask_full, "liquidity_score"])
    risk_z = zscore(scores.loc[mask_full, "risk_score"])
    equity_z = zscore(scores.loc[mask_full, "equity_score"])

    theta_full = np.degrees(np.arctan2(macro_z_f, liq_z_f))
    phi_full = np.degrees(np.arctan2(equity_z, risk_z))

    coherence_theta = np.sqrt(macro_z_f**2 + liq_z_f**2)
    coherence_phi = np.sqrt(equity_z**2 + risk_z**2)

    geo_full = pd.DataFrame(
        {
            "macro_score": scores.loc[mask_full, "macro_score"],
            "liquidity_score": scores.loc[mask_full, "liquidity_score"],
            "risk_score": scores.loc[mask_full, "risk_score"],
            "equity_score": scores.loc[mask_full, "equity_score"],
            "theta_deg": theta_full,
            "phi_deg": phi_full,
            "coherence_theta": coherence_theta,
            "coherence_phi": coherence_phi,
        },
        index=scores.index[mask_full],
    )

    full_path = os.path.join(OUT_DIR, "vcf_geometry_full.csv")
    geo_full.to_csv(full_path, index_label="date")
    print(f"\n📜 Full geometry saved: {full_path}")
    print(
        f"   Rows: {geo_full.shape[0]} "
        f"(first full row: {geo_full.index.min()})"
    )

print("\n✅ VCF geometry engine COMPLETE.\n")

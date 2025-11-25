# VCF Core Math Engine — Quick Start Guide

## Installation and Setup

### Prerequisites
```python
# Required packages
pip install pandas numpy scipy scikit-learn --break-system-packages
```

### Folder Structure
```
/content/VCF-RESEARCH/
├── data_raw/          # Place your CSV files here
├── data_clean/        # Normalized and processed data (auto-generated)
├── registry/          # Metric registry (optional)
├── outputs/           # Final outputs (auto-generated)
└── src/
    └── vcf/
        └── data/
            └── vcf_metric_registry.json  # Optional registry
```

---

## Quick Start: Minimal Example

### Step 1: Prepare Your Data

Place CSV files in `/content/VCF-RESEARCH/data_raw/`. Each CSV should have:
- A date column (named "Date", "date", or "DATE")
- One or more numeric metric columns

Example structure:
```
Date,SP500_MA_Ratio,Treasury_10Y,DXY,AGG
2020-01-01,1.05,1.92,96.5,108.2
2020-01-02,1.06,1.88,96.8,108.5
...
```

### Step 2: Run the Pipeline

```python
from vcf_core_math_engine import run_vcf_pipeline

# Run with default settings
result = run_vcf_pipeline()
```

That's it! The pipeline will:
1. Load all CSV files from `data_raw/`
2. Normalize using z-score method
3. Compute all geometric metrics
4. Save outputs to `data_clean/`

---

## Advanced Usage

### Custom Normalization

```python
# Use robust normalization (resistant to outliers)
result = run_vcf_pipeline(normalization_method="robust")

# Available methods:
# - "zscore" (default)
# - "minmax"
# - "logit"
# - "rolling_zscore"
# - "logistic"
# - "robust"
# - "tanh"
```

### Individual Component Usage

```python
from vcf_core_math_engine import (
    load_all_raw,
    normalize_series,
    compute_theta,
    compute_phi,
    compute_divergence,
    compute_resonance,
    compute_stress_index,
    compute_mrf,
    compute_mvss
)

# Load raw data
raw_data = load_all_raw()

# Normalize a specific series
import pandas as pd
series = pd.Series([100, 102, 98, 105, 103])
normalized = normalize_series(series, method="zscore")

# Compute individual metrics on a DataFrame
df = pd.DataFrame({
    'metric1': [1, 2, 3, 4, 5],
    'metric2': [5, 4, 3, 2, 1]
})

theta = compute_theta(df)
phi = compute_phi(df)
divergence = compute_divergence(df)
resonance = compute_resonance(df)
stress = compute_stress_index(df)
mrf = compute_mrf(df)
mvss = compute_mvss(df, mrf=mrf)
```

### Custom MRF Weights

```python
import pandas as pd

# Load your normalized panel
panel = pd.read_csv("/content/VCF-RESEARCH/data_clean/normalized_panel.csv")

# Define custom weights
weights = {
    'SP500_MA_Ratio': 0.4,
    'Treasury_10Y': 0.3,
    'DXY': 0.2,
    'AGG': 0.1
}

# Compute weighted MRF
from vcf_core_math_engine import compute_mrf
mrf = compute_mrf(panel, weights=weights)
```

---

## Output Files

After running the pipeline, you'll find:

### 1. Normalized Panel
**Location:** `/content/VCF-RESEARCH/data_clean/normalized_panel.csv`

Contains all input metrics after normalization, combined into a single panel.

### 2. Geometry Panel
**Location:** `/content/VCF-RESEARCH/data_clean/geometry_panel.csv`

Contains normalized metrics PLUS derived geometric metrics:
- `theta`: Angular position [0, 2π]
- `phi`: Curvature measure
- `divergence`: Correlation breakdown [0, 1]
- `resonance`: Phase coherence [0, 1]
- `stress_index`: Composite stress [0, 1]
- `mrf`: Market Risk Factor
- `mvss`: Stability score [0, 1]

---

## Phase III Pilot: 4-Input Example

For your current pilot with S&P 500 MA ratio, 10Y Treasury, DXY, and AGG:

### Data Preparation

1. Create 4 CSV files in `data_raw/`:
   - `sp500_ma_ratio.csv`
   - `treasury_10y.csv`
   - `dxy.csv`
   - `agg.csv`

2. Each file format:
```csv
Date,Value
2020-01-01,1.05
2020-01-02,1.06
...
```

### Run Pilot

```python
from vcf_core_math_engine import run_vcf_pipeline

# Run with conservative robust normalization
result = run_vcf_pipeline(normalization_method="robust")

# Examine outputs
print("\nFirst few rows of geometry panel:")
print(result.head())

print("\nSummary statistics:")
print(result[['theta', 'phi', 'divergence', 'resonance', 'stress_index', 'mrf', 'mvss']].describe())
```

### Analysis Tips

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load results
geom = pd.read_csv("/content/VCF-RESEARCH/data_clean/geometry_panel.csv")

# Convert Date to datetime
geom['Date'] = pd.to_datetime(geom['Date'])

# Plot stress over time
plt.figure(figsize=(12, 4))
plt.plot(geom['Date'], geom['stress_index'])
plt.title('Market Stress Index Over Time')
plt.xlabel('Date')
plt.ylabel('Stress Index')
plt.grid(True)
plt.show()

# Find high-stress periods
high_stress = geom[geom['stress_index'] > 0.7]
print("\nHigh Stress Periods:")
print(high_stress[['Date', 'stress_index']])

# Examine resonance patterns
plt.figure(figsize=(12, 4))
plt.plot(geom['Date'], geom['resonance'])
plt.title('Market Resonance Over Time')
plt.xlabel('Date')
plt.ylabel('Resonance')
plt.grid(True)
plt.show()
```

---

## Validation Workflow

### 1. Sanity Checks

```python
import pandas as pd

geom = pd.read_csv("/content/VCF-RESEARCH/data_clean/geometry_panel.csv")

# Check for NaN values
print("NaN counts:")
print(geom.isna().sum())

# Check ranges
print("\nValue ranges:")
print(f"Theta: [{geom['theta'].min():.2f}, {geom['theta'].max():.2f}]")
print(f"Divergence: [{geom['divergence'].min():.2f}, {geom['divergence'].max():.2f}]")
print(f"Resonance: [{geom['resonance'].min():.2f}, {geom['resonance'].max():.2f}]")
print(f"Stress: [{geom['stress_index'].min():.2f}, {geom['stress_index'].max():.2f}]")
print(f"MVSS: [{geom['mvss'].min():.2f}, {geom['mvss'].max():.2f}]")
```

### 2. Historical Alignment

```python
# Define known market events
events = {
    '2008-09-15': 'Lehman Brothers',
    '2020-03-16': 'COVID Crash',
    '2022-06-13': 'Inflation Peak'
}

# Check stress levels at these dates
for date, event in events.items():
    date_data = geom[geom['Date'] == date]
    if len(date_data) > 0:
        stress = date_data['stress_index'].values[0]
        print(f"{event} ({date}): Stress = {stress:.3f}")
```

### 3. Correlation Analysis

```python
# Examine correlations between derived metrics
derived_cols = ['theta', 'phi', 'divergence', 'resonance', 'stress_index', 'mrf', 'mvss']
corr_matrix = geom[derived_cols].corr()

print("\nCorrelation Matrix of Derived Metrics:")
print(corr_matrix)
```

---

## Troubleshooting

### Issue: "No registry found" error
**Solution:** This is just a warning. The pipeline works fine without a registry. To suppress it, create an empty registry:

```python
import pandas as pd
import os

# Create minimal registry
registry = pd.DataFrame({
    'metric': ['SP500_MA_Ratio', 'Treasury_10Y', 'DXY', 'AGG'],
    'category': ['equity', 'rates', 'fx', 'bonds']
})

os.makedirs("/content/VCF-RESEARCH/registry", exist_ok=True)
registry.to_csv("/content/VCF-RESEARCH/registry/metrics.csv", index=False)
```

### Issue: Too many NaN values in outputs
**Cause:** Insufficient data for rolling windows

**Solution:** Reduce window sizes or use more data

```python
# In vcf_core_math_engine.py, modify defaults:
# compute_theta(df, lookback=30)  # instead of 63
# compute_divergence(df, lookback=30)  # instead of 63
```

### Issue: Theta values all zero
**Cause:** Insufficient variance in data

**Check:**
```python
# Verify your normalized data has variance
panel = pd.read_csv("/content/VCF-RESEARCH/data_clean/normalized_panel.csv")
print(panel.std())
```

### Issue: Memory errors with large datasets
**Solution:** Process in chunks or reduce window sizes

---

## Performance Optimization

For large datasets (>10 years daily data):

1. **Use rolling_zscore normalization** (more efficient)
2. **Reduce window sizes** for faster computation
3. **Process in parallel** (future enhancement)

```python
# Quick mode (shorter windows)
def quick_geometry_panel(clean_panel):
    out = clean_panel.copy()
    out["theta"] = compute_theta(out, lookback=30)
    out["phi"] = compute_phi(out, lookback=10)
    out["divergence"] = compute_divergence(out, lookback=30)
    out["resonance"] = compute_resonance(out, lookback=60)
    out["stress_index"] = compute_stress_index(out, lookback=30)
    out["mrf"] = compute_mrf(out)
    out["mvss"] = compute_mvss(out, lookback=120)
    return out
```

---

## Next Steps for Phase III

1. **Run pilot on 4 inputs** (SP500 MA, 10Y, DXY, AGG)
2. **Validate stress peaks** align with known crises (2008, 2020)
3. **Check resonance patterns** in bull vs bear markets
4. **Compare normalization methods** (zscore vs robust)
5. **Document parameter sensitivities** for PNAS review
6. **Prepare visualizations** for whitepaper

---

## Example: Complete Phase III Workflow

```python
# 1. Setup
from vcf_core_math_engine import run_vcf_pipeline
import pandas as pd
import matplotlib.pyplot as plt

# 2. Run pipeline
print("Running VCF Pipeline...")
result = run_vcf_pipeline(normalization_method="robust")

# 3. Load results
geom = pd.read_csv("/content/VCF-RESEARCH/data_clean/geometry_panel.csv")
geom['Date'] = pd.to_datetime(geom['Date'])

# 4. Create summary plots
fig, axes = plt.subplots(4, 1, figsize=(14, 12))

axes[0].plot(geom['Date'], geom['stress_index'], color='red')
axes[0].set_title('Stress Index')
axes[0].grid(True)

axes[1].plot(geom['Date'], geom['resonance'], color='blue')
axes[1].set_title('Resonance')
axes[1].grid(True)

axes[2].plot(geom['Date'], geom['divergence'], color='orange')
axes[2].set_title('Divergence')
axes[2].grid(True)

axes[3].plot(geom['Date'], geom['mvss'], color='green')
axes[3].set_title('Market Vector Stability Score')
axes[3].grid(True)

plt.tight_layout()
plt.savefig("/content/VCF-RESEARCH/outputs/phase3_pilot_summary.png", dpi=150)
plt.show()

# 5. Statistical summary
print("\n=== Phase III Pilot Summary ===")
print(f"Date Range: {geom['Date'].min()} to {geom['Date'].max()}")
print(f"Total Observations: {len(geom)}")
print("\nMetric Statistics:")
print(geom[['stress_index', 'resonance', 'divergence', 'mvss']].describe())

# 6. Save summary report
summary = geom[['Date', 'stress_index', 'resonance', 'divergence', 'mvss', 'mrf']].copy()
summary.to_csv("/content/VCF-RESEARCH/outputs/phase3_summary_report.csv", index=False)
print("\nSummary saved to outputs/phase3_summary_report.csv")
```

---

## Support and Documentation

- **Full Math Documentation:** See `VCF_MATH_DOCUMENTATION.md`
- **Code Comments:** All functions have detailed docstrings
- **Parameter Tuning:** See Section 7 of Math Documentation

---

**Version:** 1.0  
**Last Updated:** 2024-11-22  
**Ready for Phase III Pilot Implementation**

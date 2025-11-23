# Data Clean

This directory contains processed, normalized, and cleaned data ready for analysis.

## Overview

This directory stores the output of data normalization and transformation processes. All files here are derived from raw data in `/data_raw/` using scripts in `/scripts/`.

## Current Files

### Normalized Individual Series
- **CPI_US_normalized.csv**: Normalized Consumer Price Index
- **DGS10_US_normalized.csv**: Normalized 10-Year Treasury Rate
- **GDP_US_normalized.csv**: Normalized GDP
- **M2_US_normalized.csv**: Normalized M2 Money Supply
- **PPI_US_normalized.csv**: Normalized Producer Price Index
- **T10Y2Y_US_normalized.csv**: Normalized Treasury Spread
- **UNRATE_US_normalized.csv**: Normalized Unemployment Rate

### Combined Panels
- **normalized_panel.csv**: Combined normalized metrics in panel format
- **macro_monthly_panel.csv**: Monthly macro panel with all indicators
- **geometry_panel.csv**: Panel with geometric calculations

## Data Processing Pipeline

```
/data_raw/*.csv 
    ↓ (scripts/data_loader.py)
Load Raw Data
    ↓ (scripts/normalize_metrics.py)
Normalize & Clean
    ↓
/data_clean/*_normalized.csv
    ↓ (scripts/build_macro_panel.py)
Build Panels
    ↓
/data_clean/*_panel.csv
```

## Normalization Methods

Common normalization approaches used:
- **Z-score normalization**: (x - mean) / std
- **Min-Max scaling**: (x - min) / (max - min)
- **Log transformations**: For monetary aggregates and prices
- **Percentage changes**: For growth rates

Specific methods are documented in individual script files.

## Panel Structure

Panel files combine multiple normalized series with:
- **Time index**: Date or period
- **Multiple columns**: One per metric
- **Aligned timestamps**: All series aligned to common frequency (monthly/daily)
- **Complete cases**: Missing values handled appropriately

## File Naming Convention

- Individual series: `{METRIC}_{COUNTRY}_normalized.csv`
- Panels: `{description}_panel.csv`
- Temporary/intermediate: Prefix with `tmp_` (excluded from git)

## Usage

These cleaned datasets are ready for:
- Geometric analysis in `/geometry/`
- Visualization in notebooks
- Statistical modeling
- Research and publication

## Best Practices

- **Do not manually edit** these files - regenerate from raw data instead
- **Document transformations** in script files or `/docs/log.md`
- **Version control**: These files are tracked in git for reproducibility
- **Re-run processing** when raw data is updated
- **Validate outputs** after processing to ensure data quality

## Regenerating Clean Data

To regenerate all clean data from raw sources:

```python
# In Python or Jupyter notebook
from scripts.data_loader import load_all_data
from scripts.normalize_metrics import normalize_all
from scripts.build_macro_panel import build_panels

# Load and normalize
load_all_data()
normalize_all()
build_panels()
```

See individual scripts for more detailed usage.

# Scripts

This directory contains Python scripts for data processing, normalization, and panel construction in the VCF Research framework.

## Contents

- **data_loader.py**: Functions for loading raw data from FRED, Yahoo Finance, and other sources
- **normalize_metrics.py**: Data normalization and standardization utilities
- **build_macro_panel.py**: Constructs combined macro-economic panels from normalized data
- **geometry_engine.py**: Core geometric analysis functions (theta, phi, coherence calculations)

## Usage

### Running Scripts

Scripts can be run from the command line or imported as modules:

```bash
# Run as standalone script
python scripts/data_loader.py

# Or import in Python/Jupyter
from scripts.data_loader import load_data
```

### Typical Workflow

1. **Load Data**: Use `data_loader.py` to fetch raw data
   ```python
   from scripts.data_loader import load_fred_data, load_yahoo_data
   ```

2. **Normalize**: Process raw data with `normalize_metrics.py`
   ```python
   from scripts.normalize_metrics import normalize_series
   ```

3. **Build Panels**: Create combined datasets with `build_macro_panel.py`
   ```python
   from scripts.build_macro_panel import build_monthly_panel
   ```

4. **Compute Geometry**: Calculate geometric indicators with `geometry_engine.py`
   ```python
   from scripts.geometry_engine import compute_theta, compute_phi
   ```

## Data Flow

```
Raw Data Sources → data_loader.py → /data_raw/
                                       ↓
                            normalize_metrics.py → /data_clean/
                                       ↓
                            build_macro_panel.py → /data_clean/panels
                                       ↓
                            geometry_engine.py → /geometry/
```

## Dependencies

- pandas
- numpy
- yfinance
- pandas-datareader
- scipy

## Best Practices

- Keep functions modular and reusable
- Add docstrings to all functions
- Handle errors gracefully with try/except blocks
- Log important operations and data transformations
- Write output to appropriate data directories (`/data_raw/`, `/data_clean/`, etc.)

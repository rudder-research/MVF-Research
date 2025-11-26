# VCF Repository Quick Reference

## Repository Structure

```
VCF-RESEARCH/
├── 📂 data/
│   ├── raw/              # Original data from FRED, Yahoo Finance
│   ├── clean/            # Processed, normalized datasets
│   └── interim/          # Intermediate pipeline files
│
├── 📂 docs/
│   ├── specs/            # VCF_Geometry_Spec_v1.md
│   ├── proposals/        # Research proposals
│   └── references/       # Papers, citations
│
├── 📂 notebooks/
│   ├── exploration/      # Ad-hoc analysis
│   ├── pipeline/         # Reproducible workflows
│   └── viz/              # Visualization notebooks
│
├── 📂 src/vcf/
│   ├── core/             # Geometry engine, vector math, harmonics
│   ├── data/             # Data loaders and fetchers
│   ├── utils/            # Normalization, filters, helpers
│   ├── models/           # ML models (future)
│   └── config/           # Paths and settings
│
├── 📂 registry/
│   ├── metric_registry.json    # 7D state vector definition
│   └── aliases.json            # Metric name aliases
│
├── 📂 visuals/
│   ├── plots/            # Exported charts
│   └── dashboards/       # HTML dashboards
│
└── 📂 tests/
    ├── test_normalization.py
    ├── test_geometry_engine.py
    └── test_registry.py
```

## Key Files

### Configuration
- `src/vcf/config/paths.py` - All directory paths
- `src/vcf/config/settings.py` - Project settings
- `requirements.txt` - Python dependencies

### Core Modules
- `src/vcf/core/geometry_engine.py` - Main VCF engine
- `src/vcf/data/loader.py` - Data loading interface
- `src/vcf/utils/normalization.py` - Normalization utilities

### Registry
- `registry/metric_registry.json` - 7D vector components
- `registry/aliases.json` - Alternative metric names

### Documentation
- `README.md` - Project overview
- `docs/specs/VCF_Geometry_Spec_v1.md` - Mathematical spec
- `PR_SUMMARY.md` - Pull request description

## The 7D State Vector

| Dimension | Metric | Source | Ticker/Series ID |
|-----------|--------|--------|------------------|
| 0 | Volatility | Yahoo | ^VIX |
| 1 | GDP Growth | FRED | A191RL1Q225SBEA |
| 2 | Unemployment | FRED | UNRATE |
| 3 | Interest Rate | FRED | FEDFUNDS |
| 4 | Inflation | FRED | CPIAUCSL |
| 5 | Credit Spread | FRED | BAA10Y |
| 6 | Equity Momentum | Yahoo | ^GSPC |

## Import Paths

```python
# Geometry engine
from src.vcf.core.geometry_engine import GeometryEngine
from src.vcf.core.vector_math import normalize_vector, compute_magnitude

# Data loading
from src.vcf.data.loader import load_clean_panel, load_registry_data
from src.vcf.data.fred_fetcher import fetch_fred_series
from src.vcf.data.yahoo_fetcher import fetch_ticker_data

# Utilities
from src.vcf.utils.normalization import zscore, minmax, clip_values
from src.vcf.utils.filters import moving_average, bandpass_filter

# Configuration
from src.vcf.config.paths import DATA_DIR, REGISTRY_DIR
from src.vcf.config.settings import STATE_VECTOR_DIM, CLIP_BOUNDS
```

## Common Commands

```bash
# Run tests
python -m pytest tests/

# Install dependencies
pip install -r requirements.txt

# Check imports
python -c "from src.vcf.core.geometry_engine import GeometryEngine; print('OK')"

# Git workflow
git status
git branch -a
git checkout repo-structure-bootstrap-v1
```

## Next Implementation Steps

1. **Geometry Engine**
   - Implement `build_state_vector()` in `geometry_engine.py`
   - Add vector normalization logic
   - Implement magnitude and angle calculations

2. **Normalization**
   - Fill in `zscore()`, `minmax()`, `clip_values()` in `normalization.py`
   - Add robust scaling implementation

3. **Data Fetchers**
   - Implement FRED API calls in `fred_fetcher.py`
   - Add Yahoo Finance integration in `yahoo_fetcher.py`

4. **Tests**
   - Add assertions to test functions
   - Create fixtures with sample data
   - Implement integration tests

## Dependencies

```
numpy>=1.24.0      # Array operations
pandas>=2.0.0      # Data manipulation
scipy>=1.10.0      # Scientific computing
matplotlib>=3.7.0  # Plotting
pyyaml>=6.0        # Config files
plotly>=5.14.0     # Interactive viz
```

## Phase Status

- ✅ Phase I: Mathematical specification complete
- ✅ Phase II: Repository structure and scaffolding complete
- ⏳ Phase III: Implementation (ready to begin)
- 📋 Phase IV: Analysis and research

---

**Repository:** VCF-RESEARCH  
**Current Branch:** repo-structure-bootstrap-v1  
**Status:** Ready for implementation

# registry/ — Indicator & Metric Definitions

Contains the authoritative registry files:

- `indicator_registry.csv` — Phase 1 raw data indicators
- `indicator_registry.json` — Expanded indicator registry (Phase 2–4)
- `metric_registry.json` — MRF/PRF/CRF metric definitions
- `vcf_metric_registry.json` — VCF-specific metric definitions
- `metrics.csv` — Metrics in CSV format
- `config.json` — Global engine configuration

## Usage

### Loading Registry in Python

```python
import json
import pandas as pd

# Load JSON registry
with open('registry/vcf_metric_registry.json', 'r') as f:
    registry = json.load(f)

# Or load CSV registry
registry_df = pd.read_csv('registry/metrics.csv')
```

## Registry Structure

Each metric entry should include:
- Metric ID
- Source (FRED, Yahoo, etc.)
- Code/Ticker
- Frequency
- Category
- Normalization method

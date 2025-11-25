# Registry

This directory contains metric definitions, configurations, and metadata for the VCF Research framework.

## Overview

The registry serves as the central repository for:
- Metric definitions and specifications
- Data source configurations
- Normalization parameters
- Geometric calculation settings
- Variable mappings and metadata

## Current Files

### vcf_metric_registry.json
JSON-formatted registry containing:
- Metric identifiers and descriptions
- Data source information (tickers, FRED codes)
- Unit specifications
- Transformation rules
- Categorization (market vs. economic, leading vs. lagging)

### metrics.csv
CSV format registry for easier viewing and editing:
- Metric name
- Source (FRED, Yahoo, etc.)
- Ticker/Code
- Frequency (daily, monthly, quarterly)
- Category
- Notes

## Registry Structure

### Example JSON Entry

```json
{
  "GDP_US": {
    "name": "U.S. Gross Domestic Product",
    "source": "FRED",
    "code": "GDP",
    "frequency": "quarterly",
    "units": "billions_of_dollars",
    "category": "economic",
    "type": "lagging",
    "normalization": "log_returns",
    "description": "Quarterly GDP in billions of chained 2012 dollars"
  }
}
```

### Example CSV Entry

```csv
metric_id,name,source,code,frequency,category,type,normalization
GDP_US,U.S. GDP,FRED,GDP,quarterly,economic,lagging,log_returns
```

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

# Get metric info
metric_info = registry['GDP_US']
print(metric_info['source'])  # 'FRED'
```

### Adding New Metrics

When adding a new metric to the framework:

1. **Update the registry files** with metric details
2. **Use consistent naming**: `{METRIC}_{COUNTRY}` format
3. **Document the source**: Exact ticker or code
4. **Specify frequency**: daily, monthly, quarterly, annual
5. **Set category**: market, economic, derivative, etc.
6. **Define normalization**: How the metric should be normalized

## Metric Categories

### By Domain
- **market**: Price-based market indicators (SPY, VIX, etc.)
- **economic**: Fundamental economic data (GDP, CPI, etc.)
- **derivative**: Calculated metrics (spreads, ratios, etc.)
- **synthetic**: Constructed indicators

### By Timing
- **leading**: Indicators that predict future conditions
- **coincident**: Indicators that reflect current conditions
- **lagging**: Indicators that confirm past trends

## Normalization Methods

Common normalization approaches tracked in registry:
- `z_score`: Standard z-score normalization
- `min_max`: Min-max scaling to [0, 1]
- `log_returns`: Logarithmic returns
- `pct_change`: Percentage changes
- `rolling_z`: Rolling window z-score

## Best Practices

- **Keep registry synchronized**: JSON and CSV should match
- **Document changes**: Note any modifications in `/docs/log.md`
- **Validate entries**: Ensure all required fields are present
- **Use version control**: Track registry changes in git
- **Review regularly**: Update as data sources or methods change

## Maintenance

### Regular Tasks
- Verify data sources are still available
- Update frequency if source changes
- Add new metrics as project expands
- Remove deprecated metrics
- Check for data quality issues

### Validation Checklist
- [ ] All metrics have unique IDs
- [ ] Source codes/tickers are correct
- [ ] Frequencies match actual data
- [ ] Normalization methods are specified
- [ ] Categories are consistently applied

## Future Enhancements

Potential additions to registry:
- Data quality flags
- Expected update schedules
- Historical availability dates
- Related metrics/dependencies
- Calculation formulas for derived metrics
- Alert thresholds for anomalies

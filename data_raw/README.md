# Data Raw

This directory contains unprocessed, raw data from various market and economic sources.

## Overview

Raw data files are stored here in their original format as retrieved from data providers. This ensures reproducibility and allows for re-processing with different normalization methods.

## Current Data Sources

### Market Data (Yahoo Finance)
- **SPY_US.csv**: S&P 500 ETF daily prices
- **VIX_US.csv**: CBOE Volatility Index
- **XLU_US.csv**: Utilities Select Sector SPDR Fund

### Economic Data (FRED - Federal Reserve Economic Data)
- **GDP_US.csv**: U.S. Gross Domestic Product
- **CPI_US.csv**: Consumer Price Index
- **PPI_US.csv**: Producer Price Index
- **M2_US.csv**: M2 Money Supply
- **UNRATE_US.csv**: Unemployment Rate
- **DGS10_US.csv**: 10-Year Treasury Constant Maturity Rate
- **T10Y2Y_US.csv**: 10-Year Treasury Minus 2-Year Treasury Spread

## Data Format

All CSV files should follow this structure:
- **Date column**: First column, labeled "Date" or similar
- **Value columns**: Subsequent columns with metric values
- **Header row**: Column names in first row

## Adding New Data

When adding new raw data files:

1. **Save to this directory** in CSV format
2. **Use consistent naming**: `{METRIC}_{COUNTRY}.csv` (e.g., `GDP_US.csv`)
3. **Document the source** in `/docs/DATA_SOURCES.md`:
   - Data provider (FRED, Yahoo Finance, etc.)
   - Exact series ID or ticker
   - Date range
   - Retrieval date
   - Any known data quality issues

4. **Preserve original format**: Do not modify raw data files after download
5. **Update `.gitignore`** if files are very large (>10MB)

## Data Updates

- Raw data should be periodically refreshed from sources
- Document update dates in `/docs/DATA_SOURCES.md`
- Keep previous versions if needed for reproducibility
- Use scripts in `/scripts/data_loader.py` for automated updates

## Notes

- Do **not** edit raw data files manually
- All data transformations should happen in `/scripts/` and output to `/data_clean/`
- For data quality issues, document in `/docs/DATA_SOURCES.md`
- See `/docs/DATA_SOURCES.md` for detailed source information

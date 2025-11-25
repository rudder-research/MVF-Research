# Data Sources

This document tracks all data sources used in the VCF Research project, including retrieval methods, preprocessing steps, and known issues.

## Overview

The VCF Research framework integrates data from multiple sources to create a comprehensive view of macro-financial dynamics. This document serves as the authoritative record of what data is used, where it comes from, and how it has been processed.

---

## Market Data Sources

### Yahoo Finance

**Access Method**: `yfinance` Python library

#### S&P 500 (SPY)
- **Ticker**: SPY
- **Description**: SPDR S&P 500 ETF Trust
- **Frequency**: Daily
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/SPY_US.csv`
- **Notes**: Primary market index proxy

#### VIX (Volatility Index)
- **Ticker**: ^VIX
- **Description**: CBOE Volatility Index
- **Frequency**: Daily
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/VIX_US.csv`
- **Notes**: Market fear gauge

#### Utilities ETF (XLU)
- **Ticker**: XLU
- **Description**: Utilities Select Sector SPDR Fund
- **Frequency**: Daily
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/XLU_US.csv`
- **Notes**: Defensive sector proxy

---

## Economic Data Sources

### FRED (Federal Reserve Economic Data)

**Access Method**: `pandas-datareader` or FRED API  
**URL**: https://fred.stlouisfed.org/

#### GDP
- **Series ID**: GDP
- **Description**: Gross Domestic Product
- **Frequency**: Quarterly
- **Units**: Billions of Dollars, Seasonally Adjusted Annual Rate
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/GDP_US.csv`
- **Notes**: Primary measure of economic output

#### CPI
- **Series ID**: CPIAUCSL
- **Description**: Consumer Price Index for All Urban Consumers: All Items
- **Frequency**: Monthly
- **Units**: Index 1982-1984=100, Seasonally Adjusted
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/CPI_US.csv`
- **Notes**: Inflation measure

#### PPI
- **Series ID**: PPIACO
- **Description**: Producer Price Index for All Commodities
- **Frequency**: Monthly
- **Units**: Index 1982=100, Not Seasonally Adjusted
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/PPI_US.csv`
- **Notes**: Wholesale price pressure

#### M2 Money Supply
- **Series ID**: M2SL
- **Description**: M2 Money Stock
- **Frequency**: Monthly
- **Units**: Billions of Dollars, Seasonally Adjusted
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/M2_US.csv`
- **Notes**: Broad money supply measure

#### Unemployment Rate
- **Series ID**: UNRATE
- **Description**: Unemployment Rate
- **Frequency**: Monthly
- **Units**: Percent, Seasonally Adjusted
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/UNRATE_US.csv`
- **Notes**: Labor market indicator

#### 10-Year Treasury Rate
- **Series ID**: DGS10
- **Description**: 10-Year Treasury Constant Maturity Rate
- **Frequency**: Daily
- **Units**: Percent, Not Seasonally Adjusted
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/DGS10_US.csv`
- **Notes**: Long-term interest rate

#### Treasury Spread (10Y-2Y)
- **Series ID**: T10Y2Y
- **Description**: 10-Year Treasury Minus 2-Year Treasury
- **Frequency**: Daily
- **Units**: Percent, Not Seasonally Adjusted
- **Date Range**: [To be documented]
- **Last Updated**: [To be documented]
- **File**: `data_raw/T10Y2Y_US.csv`
- **Notes**: Yield curve slope, recession indicator

---

## Data Retrieval Process

### Automated Retrieval

Use scripts in `/scripts/data_loader.py`:

```python
from scripts.data_loader import load_fred_data, load_yahoo_data

# Load FRED data
load_fred_data('GDP', 'data_raw/GDP_US.csv')

# Load Yahoo Finance data
load_yahoo_data('SPY', 'data_raw/SPY_US.csv')
```

### Manual Retrieval

If automated retrieval fails:
1. Visit source website (FRED or Yahoo Finance)
2. Download data in CSV format
3. Save to appropriate `data_raw/` file
4. Document retrieval date and any issues below

---

## Preprocessing Steps

### General Preprocessing
1. **Date Parsing**: Convert date columns to datetime format
2. **Missing Values**: Document any gaps or missing periods
3. **Frequency Alignment**: Resample data to common frequency when needed
4. **Outlier Detection**: Flag unusual values for investigation

### Normalization
- Applied via `/scripts/normalize_metrics.py`
- Methods vary by metric (see `/registry/` for specifics)
- Output to `/data_clean/`

### Panel Construction
- Combined via `/scripts/build_macro_panel.py`
- Aligned to common monthly or daily frequency
- Output to `/data_clean/macro_monthly_panel.csv`

---

## Known Issues and Limitations

### Data Quality
- **GDP**: Quarterly frequency requires interpolation for monthly analysis
- **VIX**: Not available before 1990
- **Treasury data**: Some missing values on holidays/weekends
- [Add issues as discovered]

### Update Frequency
- **Market data**: Should be updated daily
- **Economic data**: Update after monthly/quarterly releases
- **Manual checks**: Recommended monthly

### Data Gaps
- [Document any known gaps in time series]
- [Note any structural breaks or revisions]

---

## Update Log

Track when data was last updated:

| Date | Metrics Updated | Updated By | Notes |
|------|----------------|------------|-------|
| [Date] | All | [Name] | Initial data load |
| [Date] | SPY, VIX | [Name] | Monthly market update |
| [Date] | GDP, CPI | [Name] | Quarterly econ data |

---

## Future Data Additions

Potential metrics to add:
- [ ] International markets (EFA, EEM)
- [ ] Corporate spreads (BAA-AAA)
- [ ] Housing data (Case-Shiller)
- [ ] Labor market (JOLTS, initial claims)
- [ ] Commodity prices (CRB, oil)
- [ ] Fed funds rate, EFFR
- [ ] Other central bank rates
- [ ] PMI indicators

---

## References

- **FRED**: https://fred.stlouisfed.org/
- **Yahoo Finance**: https://finance.yahoo.com/
- **CBOE VIX**: https://www.cboe.com/tradable_products/vix/

---

**Last Updated**: [To be filled in]  
**Maintained By**: VCF Research Team

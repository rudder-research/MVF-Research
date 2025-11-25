# Data Directory

This directory contains all data used in the VCF project.

## Structure

- `raw/` — Original, unprocessed data from FRED, Yahoo Finance, etc.
- `clean/` — Normalized, merged, and preprocessed datasets
- `interim/` — Intermediate files during pipeline processing

## Data Sources

1. **FRED** (Federal Reserve Economic Data)
   - GDP growth
   - Unemployment rate
   - Federal Funds Rate
   - CPI inflation
   - Credit spreads

2. **Yahoo Finance**
   - VIX (volatility index)
   - S&P 500 data
   - ETF prices

## Usage

Place raw data files in the `raw/` directory. The data pipeline will process them and output to `clean/`.

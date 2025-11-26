# Phase I Pilot: Regime Detection Test

## Overview
Tests the regime detection engine on normalized market data.

## Usage

From Colab:
```python
import sys
sys.path.insert(0, '/content/drive/MyDrive/VCF-RESEARCH/pilots/Phase_I_Regime_MathTests')

from test_regime_detection import main
main()
```

## Outputs
- `regime_results.csv` - Full time series of detected regimes
- `regime_statistics.csv` - Statistics by regime type
- `transition_matrix.csv` - Regime transition probabilities
- `regime_timeline.png` - Visual timeline of regimes

## Current Status
Using available normalized data as pilot inputs. Will update to use:
- SPY 50d-200d moving average
- DGS10 (10-year Treasury)
- DXY (US Dollar Index)
- AGG (Bond ETF)

when data is available.

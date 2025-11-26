# regime_engine/ — Phase I Regime Detection

Implements the macro, liquidity, credit, and volatility metrics necessary to classify economic and market regimes.

## Components

- `detector.py` → regime classification logic
- `metrics.py` → individual metric definitions
- `config.py` → thresholds, windows, registry bindings

## Outputs

- Regime label (Expansion / Late-Cycle / Contraction)
- MRF (Market Risk Factor)
- PRF (Policy Risk Factor)
- CRF (Credit Risk Factor)

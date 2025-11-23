# Geometry

This directory contains geometric analysis outputs and calculations for the Vector Coherence Framework (VCF).

## Overview

The geometry engine computes vector-based relationships between market and economic indicators, treating each metric as having magnitude and direction that can align or diverge over time.

## Core Concepts

### Theta (θ) - Angle Between Vectors
Measures the angular relationship between different economic/market vectors. High theta values indicate divergence; low values indicate alignment.

### Phi (φ) - Rotational Dynamics  
Captures rotational or cyclical patterns in the data, identifying periods of regime change or structural shifts.

### Coherence
Quantifies the degree of alignment across multiple indicators. High coherence suggests synchronized behavior; low coherence indicates fragmentation.

### Vector Divergence
Measures how quickly vectors are moving apart or together, indicating potential stress or stability in the system.

## Current Files

- **geometry_panel.csv**: Combined geometric indicators with timestamps

## Computation Process

Geometric indicators are computed using:
- Normalized data from `/data_clean/`
- Scripts in `/scripts/geometry_engine.py`
- Potentially automated via GitHub Actions workflows

## Planned Outputs (Future)

```
geometry/
├── theta.csv              # Theta values over time
├── phi.csv                # Phi rotational measures
├── coherence.csv          # Coherence scores
├── divergence.csv         # Divergence metrics
└── diagnostics/           # Diagnostic plots and statistics
```

## Usage

### Computing Geometry

```python
from scripts.geometry_engine import compute_theta, compute_phi, compute_coherence

# Load panel data
import pandas as pd
panel = pd.read_csv('data_clean/macro_monthly_panel.csv')

# Compute geometric indicators
theta = compute_theta(panel)
phi = compute_phi(panel)
coherence = compute_coherence(panel)
```

### Interpreting Results

- **High Coherence + Low Theta**: Strong alignment, stable regime
- **Low Coherence + High Theta**: Fragmentation, potential instability
- **Rising Phi**: Rotational shift, possible regime change
- **High Divergence**: Vectors moving apart rapidly, stress indication

## Research Applications

Geometric analysis enables study of:
- **Regime shifts**: Identifying transitions between market states
- **Macro-financial stress**: Detecting periods of high divergence
- **Structural alignment**: Understanding coordinated vs. fragmented behavior
- **Wave dynamics**: Cyclical patterns in multi-dimensional economic space

## Future Development

Planned enhancements:
- Automated computation via GitHub Actions
- Additional geometric metrics (curvature, acceleration)
- Multi-dimensional coherence measures
- Stress indices and early warning indicators
- Interactive visualization tools

## References

For theoretical background and methodology, see:
- `/docs/VCF-Geometrical Pilot v1.md`
- `/docs/calculation summary.md`
- Main README.md

## Notes

- This is an active research area - methods and outputs will evolve
- Document new findings in `/docs/log.md`
- Validate geometric outputs against known market events
- Compare results across different normalization methods

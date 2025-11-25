# VCF Research Project

This repository implements the **Vector Cycle Framework (VCF)** —  
a macro-financial geometry system that models markets as evolving vectors in a multidimensional state-space.

## Overview

The VCF project transforms traditional financial and economic indicators into a unified geometric framework, enabling novel approaches to market analysis, risk assessment, and regime detection. By representing market states as vectors in a normalized 7-dimensional space, we can apply geometric and topological methods to understand market dynamics.

## Key Components

- **Geometry Engine** — converts macro & market data into a 7D normalized vector
- **Harmonic Tools** — coherence, resonance, divergence, rotation
- **Stress Index (future)** — detects instability or regime breaks
- **Data Pipeline** — FRED + Yahoo Finance collection and preprocessing
- **Visualization Suite** — plots, dashboards, and vector field maps

## Repository Structure

```
VCF-RESEARCH/
├── data/               # Data storage (raw, clean, interim)
├── docs/               # Documentation and specifications
├── notebooks/          # Jupyter notebooks for analysis
├── src/vcf/            # Core source code
│   ├── core/          # Geometry engine and mathematical operations
│   ├── data/          # Data fetchers and loaders
│   ├── utils/         # Utility functions
│   ├── models/        # ML models (future)
│   └── config/        # Configuration files
├── registry/           # Metric definitions and aliases
├── visuals/            # Generated plots and dashboards
└── tests/              # Unit tests
```

## Current Status

- ✅ **Phase I complete**: Mathematical specification finalized  
- 🚧 **Phase II begins here**: repository restructuring + scaffolding  
- ⏳ **Phase III will implement**: the geometry engine and core algorithms

## The 7D State Vector

The VCF framework represents market conditions as a 7-dimensional vector:

1. **Volatility** (VIX) — market fear and uncertainty
2. **Growth** (GDP) — economic expansion/contraction
3. **Labor** (Unemployment) — employment dynamics
4. **Monetary** (Fed Funds Rate) — monetary policy stance
5. **Inflation** (CPI) — price level changes
6. **Credit** (Spread) — credit risk premium
7. **Equity** (Momentum) — market trend strength

Each dimension is normalized using z-scores and clipped to the range [-3, 3] to create a consistent geometric space.

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/rudder-research/VCF-RESEARCH.git
cd VCF-RESEARCH

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Set up your API keys for data fetching:

```bash
export FRED_API_KEY="your_fred_api_key"
export ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key"
```

### Basic Usage

```python
from src.vcf.core.geometry_engine import GeometryEngine
from src.vcf.data.loader import load_metric_registry

# Load the metric registry
registry = load_metric_registry('registry/metric_registry.json')

# Initialize the geometry engine
engine = GeometryEngine(registry)

# Build and analyze state vectors (implementation coming in Phase III)
```

## Development Roadmap

### Phase I: Foundation ✅
- Mathematical specification
- Conceptual framework
- Architectural design

### Phase II: Infrastructure 🚧 (Current)
- Repository organization
- Code scaffolding
- Data pipeline setup
- Testing framework

### Phase III: Implementation ⏳
- Geometry engine
- Vector mathematics
- Harmonic analysis tools
- Visualization suite

### Phase IV: Analysis 📋
- Historical backtesting
- Regime detection
- Stress index development
- Research papers

## Contributing

This repository is jointly maintained by:
- Jason Rudder (Lead Researcher)
- ChatGPT (Assistant)
- Claude (Assistant)
- GitHub Copilot (Code Completion)

## Documentation

Detailed specifications and research notes can be found in the `docs/` directory:

- `docs/specs/` — Mathematical and technical specifications
- `docs/proposals/` — Research proposals and experimental designs
- `docs/references/` — Academic papers and references

## License

[License information to be added]

## Contact

Jason Rudder  
[Contact information to be added]

---

**Note**: This is a research project under active development. The scaffolding is in place, but core functionality is still being implemented. Check back for updates!

# Vector Coherence Framework (VCF)
## A Geometric Approach to Market Regime Analysis

---

## 📋 Overview

VCF is a research framework that analyzes financial markets through **geometry** and **harmonic analysis** rather than traditional economic assumptions. It treats market data as pure mathematical signals to discover patterns first, then overlay economic interpretation.

**Key Innovation:** Dual-input normalization that solves the fundamental problem of mixing trending and oscillating financial data.

**What VCF Does:**
- Identifies market regimes through geometric analysis
- Measures synchronization between market signals
- Detects regime transitions and stress buildup
- Provides academic-grade mathematical foundation

**What VCF Doesn't Do:**
- Forecast prices
- Generate trading signals
- Make economic predictions

---

## 🚀 Quick Start

### Installation

```python
# In Google Colab or Jupyter
!pip install numpy pandas scipy scikit-learn --break-system-packages

# Import VCF modules
from vcf_main import VCFPipeline, quick_analysis
```

### Basic Usage

```python
import pandas as pd

# Load your market data
market_data = {
    'GDP': your_gdp_series,
    'SP500': your_sp500_series,
    'Treasury10Y': your_yield_series,
    'VIX': your_vix_series
}

# Run complete analysis
results = quick_analysis(market_data)

# Access results
print(results['regimes'].value_counts())
print(results['coherence_matrix'])
results['state_matrix'].to_csv('output.csv')
```

---

## 📊 Complete Example

```python
import numpy as np
import pandas as pd
from vcf_main import VCFPipeline

# Create pipeline
pipeline = VCFPipeline(
    ma_window=12,        # 12-month moving average
    roc_window=1,        # 1-month rate of change
    sampling_freq=12.0   # Monthly data
)

# Load data (example with pandas)
gdp = pd.read_csv('gdp.csv', index_col='Date', parse_dates=True)['GDP']
sp500 = pd.read_csv('sp500.csv', index_col='Date', parse_dates=True)['Close']
treasury = pd.read_csv('treasury.csv', index_col='Date', parse_dates=True)['Rate']

market_data = {
    'GDP': gdp,
    'SP500': sp500,
    'Treasury10Y': treasury
}

# Run analysis
results = pipeline.run_analysis(market_data)

# Examine results
print("\n=== State Matrix ===")
print(results['state_matrix'].head())

print("\n=== Coherence Matrix (PLV) ===")
print(results['coherence_matrix'])

print("\n=== Geometric Metrics ===")
print(f"Mean Magnitude: {results['magnitude'].mean():.3f}")
print(f"Mean Rotation: {results['rotation'].mean():.3f} radians")

print("\n=== Regime Distribution ===")
print(results['regimes'].value_counts())

# Export everything
pipeline.export_results(output_dir='./vcf_results')
```

---

## 🔬 Understanding the Output

### 1. State Matrix
**Normalized market data** with dual inputs (position + momentum) for each source.

Columns: `{source}_position`, `{source}_momentum` for each market source

```python
# Example: 4 sources → 8 columns
state_matrix.columns
# ['GDP_position', 'GDP_momentum', 
#  'SP500_position', 'SP500_momentum',
#  'Treasury10Y_position', 'Treasury10Y_momentum',
#  'VIX_position', 'VIX_momentum']
```

### 2. Coherence Metrics

**Coherence Matrix (PLV):** Pairwise phase-locking values
- Values from 0 (no sync) to 1 (perfect sync)
- Measures how synchronized signals are
- More robust than correlation

**Kuramoto Order Parameter:** Global synchronization
- R ≈ 1: Market highly synchronized (stable regime)
- R ≈ 0: Market fragmented (transition/chaos)
- Falling R often precedes regime changes

```python
# Check if market is synchronized
current_order = results['kuramoto_order'].iloc[-1]
if current_order > 0.7:
    print("Market highly synchronized")
elif current_order < 0.3:
    print("Market fragmenting - potential transition")
```

### 3. Geometric Metrics

**Magnitude:** Distance from equilibrium (market stress)
```python
# High magnitude = extreme state
stress_level = results['magnitude'].iloc[-1]
```

**Rotation:** Angular change between periods (regime stability)
```python
# High rotation = rapid regime change
rotation_rate = results['rotation'].iloc[-1]
```

**Divergence:** Distance from historical mean
```python
# High divergence = unusual conditions
divergence = results['divergence'].iloc[-1]
```

### 4. Regime Classifications

Possible regimes:
- **Equilibrium:** Stable, near historical norms
- **Trending:** Strong directional move, smooth
- **Transition:** Regime change in progress
- **Stress:** Extreme but stable configuration
- **Crisis:** Severe dislocation, multiple extremes
- **Recovery:** Returning from extreme
- **Normal:** None of the above

```python
# Current regime
current_regime = results['regimes'].iloc[-1]
print(f"Current regime: {current_regime}")

# Regime history
regime_history = results['regimes'].value_counts()
print(regime_history)

# Detect recent regime changes
recent_changes = results['regime_changes'].tail(12)
print(f"Regime changes in last 12 months: {recent_changes.sum()}")
```

---

## 📈 Advanced Usage

### Custom Normalization

```python
from vcf_normalization import VCFNormalizer

normalizer = VCFNormalizer(ma_window=24, roc_window=3)

# Dual-input normalization
state = normalizer.batch_normalize(data_df, method='dual_input')

# Or harmonic normalization
state = normalizer.batch_normalize(data_df, method='harmonic')
```

### Deep Coherence Analysis

```python
from vcf_coherence import CoherenceEngine, PhaseLockingAnalysis

engine = CoherenceEngine()

# Analyze specific pair
analysis = PhaseLockingAnalysis(sp500, gdp, "SP500", "GDP")
results = analysis.full_analysis()

print(f"Global PLV: {results['plv_global']:.3f}")
print(f"Rolling PLV mean: {results['plv_rolling'].mean():.3f}")

# Detect phase slips (synchronization breaks)
slips = analysis.detect_phase_slips(threshold=1.0)
print(f"Phase slips detected: {slips.sum()}")
```

### Custom Geometric Analysis

```python
from vcf_geometry import GeometricAnalyzer, RegimeDetector

analyzer = GeometricAnalyzer()

# Compute specific metrics
magnitude = analyzer.magnitude(state_matrix)
rotation = analyzer.angular_rotation(state_matrix)
velocity = analyzer.velocity(state_matrix)

# PCA projection
pca_proj, pca_model = analyzer.pca_projection(state_matrix, n_components=3)
print(f"Explained variance: {pca_model.explained_variance_ratio_}")

# Custom regime detection
detector = RegimeDetector(analyzer)
signals = detector.compute_regime_signals(state_matrix)
regimes = detector.classify_regime(signals)
```

---

## 🎯 Use Cases

### 1. Portfolio Research
```python
# Analyze relationship between asset classes
assets = {
    'Stocks': sp500_series,
    'Bonds': treasury_series,
    'Commodities': commodity_series,
    'RealEstate': reit_series
}

results = quick_analysis(assets)

# Find which assets move together
coh_matrix = results['coherence_matrix']
print(coh_matrix)
```

### 2. Macro Regime Analysis
```python
# Study macro environment
macro = {
    'GDP': gdp_series,
    'Inflation': cpi_series,
    'Employment': unemployment_series,
    'Rates': fed_funds_series
}

results = quick_analysis(macro)

# Track regime evolution
regime_timeline = results['regimes']
regime_timeline.plot()
```

### 3. Market Stress Monitoring
```python
# Monitor market stress in real-time
market = {
    'SP500': sp500,
    'VIX': vix,
    'Credit': credit_spread,
    'DXY': dollar_index
}

results = quick_analysis(market)

# Check stress indicators
stress_level = results['magnitude'].iloc[-1]
coherence_level = results['kuramoto_order'].iloc[-1]

if stress_level > 2.0 and coherence_level < 0.3:
    print("WARNING: High stress + low coherence")
```

---

## 📚 Module Reference

### `vcf_normalization.py`
**Purpose:** Transform heterogeneous financial data into unified state space

**Key Classes:**
- `VCFNormalizer`: Main normalization engine
  - `dual_input_transform()`: Position + momentum extraction
  - `harmonic_normalize()`: Fourier-based normalization
  - `batch_normalize()`: Process multiple series

**Key Functions:**
- `create_state_matrix()`: High-level wrapper

### `vcf_coherence.py`
**Purpose:** Measure synchronization and phase relationships

**Key Classes:**
- `CoherenceEngine`: Coherence calculations
  - `hilbert_phase()`: Extract instantaneous phase
  - `phase_locking_value()`: Compute PLV
  - `kuramoto_order_parameter()`: Global synchronization
  - `spectral_coherence()`: Frequency-domain coherence

- `PhaseLockingAnalysis`: Deep analysis of signal pairs
  - `full_analysis()`: Complete phase analysis
  - `detect_phase_slips()`: Find synchronization breaks

### `vcf_geometry.py`
**Purpose:** Geometric analysis of state space

**Key Classes:**
- `GeometricAnalyzer`: Compute geometric quantities
  - `magnitude()`: Distance from equilibrium
  - `angular_rotation()`: Regime change rate
  - `divergence_from_mean()`: Distance from norms
  - `pca_projection()`: Dimensionality reduction

- `RegimeDetector`: Identify and classify regimes
  - `compute_regime_signals()`: All geometric metrics
  - `classify_regime()`: Regime classification
  - `detect_regime_changes()`: Transition detection

### `vcf_main.py`
**Purpose:** Complete pipeline integration

**Key Classes:**
- `VCFPipeline`: End-to-end analysis
  - `run_analysis()`: Complete workflow
  - `export_results()`: Save all outputs

**Key Functions:**
- `quick_analysis()`: One-line complete analysis

---

## ⚙️ Parameters Guide

### Moving Average Window (`ma_window`)
**Purpose:** Defines "trend" for position calculation

**Guidance:**
- Monthly data: 12 (one year)
- Daily data: 252 (one trading year)
- Should capture ~1 cycle of dominant frequency

### Rate of Change Window (`roc_window`)
**Purpose:** Defines momentum calculation period

**Guidance:**
- Usually 1 (immediate momentum)
- Larger values smooth but add lag

### Sampling Frequency (`sampling_freq`)
**Purpose:** Time units for coherence analysis

**Values:**
- Monthly data: 12.0
- Daily data: 252.0
- Weekly data: 52.0

---

## 🐛 Troubleshooting

### "Not enough data for PCA"
**Cause:** Less than 3 observations
**Fix:** Use more data or reduce n_components

### "Series has >30% missing data"
**Cause:** Too many NaNs in input
**Fix:** Fill missing values or use different data source

### "Cannot convert index to datetime"
**Cause:** Index is not date format
**Fix:** Ensure data has datetime index: `df.index = pd.to_datetime(df.index)`

### Warnings about division by zero
**Cause:** Series has zero or near-zero values
**Fix:** This is handled automatically, but check data quality

---

## 📖 Mathematical Documentation

See `VCF_MATHEMATICAL_DOCUMENTATION.txt` for complete mathematical foundation including:
- Theoretical justification for all methods
- Academic references and citations
- Detailed formulas and derivations
- Edge case handling
- Parameter selection guidance

---

## 🎓 Academic Context

VCF represents a novel approach suitable for academic publication. Key features:

1. **Rigor:** Complete mathematical justification for all methods
2. **Reproducibility:** Fully documented code with test cases
3. **Novelty:** Dual-input architecture solves fundamental normalization problem
4. **Interdisciplinary:** Combines signal processing, differential geometry, and dynamical systems

Suitable for:
- Quantitative finance journals
- Econophysics publications
- Computational economics conferences
- Physics journals (PNAS interested)

---

## 📝 Citation

If you use VCF in academic work:

```
Rudder, J. (2024). Vector Coherence Framework: A Geometric Approach 
to Market Regime Analysis. GitHub: rudder-research/VCF-RESEARCH
```

---

## 🤝 Contributing

This is a research framework. Contributions welcome:
- Additional coherence metrics
- Alternative normalization methods
- Regime classification improvements
- Visualization tools
- Documentation enhancements

---

## 📄 License

MIT License - See LICENSE file

---

## 📞 Contact

Jason Rudder
GitHub: rudder-research/VCF-RESEARCH

---

## 🔄 Version History

**v1.0 (November 2024)**
- Initial release
- Dual-input normalization
- Complete coherence engine
- Geometric analysis framework
- Regime detection system

---

**Built for academic research and serious market analysis.**

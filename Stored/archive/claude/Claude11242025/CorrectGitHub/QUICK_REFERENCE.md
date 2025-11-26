# VCF Quick Reference Card
## One-Page Cheat Sheet

---

## 🚀 QUICKEST START (Copy-Paste This!)

```python
# 1. Install
!pip install numpy pandas scipy scikit-learn --break-system-packages

# 2. Import
from vcf_main import quick_analysis
import pandas as pd

# 3. Load your data
data = {
    'GDP': your_gdp_series,
    'SP500': your_sp500_series,
    'VIX': your_vix_series
}

# 4. Analyze (ONE LINE!)
results = quick_analysis(data)

# 5. View results
print(results['regimes'].value_counts())
print(results['coherence_matrix'])
results['state_matrix'].to_csv('output.csv')
```

---

## 📊 KEY RESULTS EXPLAINED

| Result | What It Is | How to Use |
|--------|-----------|------------|
| `state_matrix` | Normalized data | Use for further analysis |
| `coherence_matrix` | PLV between all signals | Find which signals sync |
| `kuramoto_order` | Global synchronization | R>0.7 = sync, R<0.3 = chaos |
| `magnitude` | Market stress | Higher = more extreme |
| `rotation` | Regime change rate | Higher = faster transition |
| `regimes` | Regime labels | See what regime you're in |

---

## 🎯 COMMON TASKS

### Check Current Regime
```python
current = results['regimes'].iloc[-1]
print(f"Current regime: {current}")
```

### Find Most Synchronized Signals
```python
coh = results['coherence_matrix']
print(coh.unstack().sort_values(ascending=False).head(10))
```

### Check Market Stress
```python
stress = results['magnitude'].iloc[-1]
if stress > 2.0:
    print("HIGH STRESS!")
```

### Detect Recent Regime Changes
```python
changes = results['regime_changes'].tail(12)
print(f"Changes in last year: {changes.sum()}")
```

### Export Everything
```python
pipeline = VCFPipeline()
pipeline.run_analysis(data)
pipeline.export_results(output_dir='./results')
```

---

## 🔧 KEY PARAMETERS

| Parameter | Default | When to Change |
|-----------|---------|----------------|
| `ma_window` | 12 | Monthly data=12, Daily=252 |
| `roc_window` | 1 | Usually keep at 1 |
| `sampling_freq` | 12.0 | Monthly=12, Daily=252 |

---

## 🎓 REGIME TYPES

| Regime | Meaning | What to Look For |
|--------|---------|------------------|
| **Equilibrium** | Stable, normal | Low stress, low change |
| **Trending** | Strong direction | High velocity, smooth |
| **Transition** | Regime shifting | High rotation |
| **Stress** | Extreme state | High magnitude |
| **Crisis** | Severe dislocation | Everything high |
| **Recovery** | Returning to normal | Falling magnitude |

---

## 💡 INTERPRETATION GUIDE

### Kuramoto Order Parameter
- **R ≈ 1.0**: Perfect synchronization (stable regime)
- **R ≈ 0.7-0.9**: High sync (normal conditions)
- **R ≈ 0.3-0.7**: Medium sync (mixed conditions)
- **R ≈ 0.0-0.3**: Low sync (transition/crisis)

### Magnitude
- **< 1.0**: Normal conditions
- **1.0-2.0**: Elevated
- **2.0-3.0**: High stress
- **> 3.0**: Extreme

### Phase Locking Value (PLV)
- **0.8-1.0**: Strong synchronization
- **0.5-0.8**: Moderate sync
- **0.3-0.5**: Weak sync
- **0.0-0.3**: Independent

---

## 🐛 TROUBLESHOOTING

| Error | Solution |
|-------|----------|
| Module not found | Upload all 4 .py files |
| Index not datetime | `df.index = pd.to_datetime(df.index)` |
| Too many NaNs | Fill missing values first |
| Not enough data | Need ≥24 observations |

---

## 📁 FILE STRUCTURE

```
VCF-RESEARCH/
├── vcf_normalization.py   ← Dual-input normalization
├── vcf_coherence.py        ← Phase & synchronization
├── vcf_geometry.py         ← Geometric analysis
├── vcf_main.py            ← Main pipeline
├── requirements.txt        ← Dependencies
├── test_vcf.py            ← Test suite
├── README.md              ← Full documentation
└── VCF_MATHEMATICAL_DOCUMENTATION.txt ← Academic theory
```

---

## 🎯 TYPICAL WORKFLOW

1. **Load Data** → `market_data = {...}`
2. **Quick Analysis** → `results = quick_analysis(market_data)`
3. **Check Regimes** → `print(results['regimes'])`
4. **Check Coherence** → `print(results['coherence_matrix'])`
5. **Export** → `results['state_matrix'].to_csv('output.csv')`
6. **Interpret** → Add economic narrative
7. **Visualize** → Create plots
8. **Iterate** → Refine and explore

---

## 🔬 ADVANCED USAGE

### Custom Pipeline
```python
from vcf_main import VCFPipeline

pipeline = VCFPipeline(ma_window=24, roc_window=3)
results = pipeline.run_analysis(data)
```

### Individual Modules
```python
from vcf_normalization import VCFNormalizer
from vcf_coherence import CoherenceEngine
from vcf_geometry import GeometricAnalyzer

normalizer = VCFNormalizer()
engine = CoherenceEngine()
analyzer = GeometricAnalyzer()
```

### Deep Dive
```python
from vcf_coherence import PhaseLockingAnalysis

analysis = PhaseLockingAnalysis(sp500, gdp, "SP500", "GDP")
results = analysis.full_analysis()
```

---

## 📞 HELP

- **README.md** - Usage examples & troubleshooting
- **VCF_MATHEMATICAL_DOCUMENTATION.txt** - Math theory
- **test_vcf.py** - Working examples
- **IMPLEMENTATION_SUMMARY.md** - Overview & next steps

---

## ⚡ ONE-LINERS FOR EVERYTHING

```python
# Complete analysis
results = quick_analysis(data)

# Check regime
results['regimes'].iloc[-1]

# Export
results['state_matrix'].to_csv('out.csv')

# Test
!python test_vcf.py

# Visualize
results['magnitude'].plot()
```

---

**Keep this card handy when working with VCF!**

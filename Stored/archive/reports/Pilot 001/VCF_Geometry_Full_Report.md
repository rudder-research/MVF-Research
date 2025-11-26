
# VCF Geometry Engine — Full Mathematical & Numerical Report

## 1. Executive Summary
This document summarizes the first full VCF Geometry Engine run, using four macro-financial metrics:
- SPY monthly log returns
- VIX monthly close
- T10Y2Y normalized yield-curve spread
- M2 normalized liquidity level

The VCF engine applies analytic signal geometry (Hilbert transform) to extract amplitude, phase, instantaneous frequency, and system coherence.

## 2. Methodology Overview
### 2.1 Data Cleaning & Alignment
- Imported cleaned SPY & VIX monthly datasets  
- Resampled T10Y2Y and M2 to monthly means  
- Converted all dates to monthly end-of-month  
- Stripped Apple/Google header corruption  
- Merged into one aligned panel with 391 observations  
- Date range: 1993-03 → 2025-09

Final panel columns:
```
spy_ret   (SPY log return)
vix       (VIX close)
t10y2y    (normalized 10s–2s spread)
m2        (normalized money supply)
```

## 3. Mathematical Framework (Full Derivations)
### 3.1 Normalization
Z-scoring ensures comparability:
\[
	ilde{x}_i(t) = rac{x_i(t) - \mu_i}{\sigma_i}
\]

### 3.2 Analytic Signal via Hilbert Transform
\[
z_i(t) = 	ilde{x}_i(t) + i \cdot \mathcal{H}[	ilde{x}_i](t)
\]

Amplitude:
\[
A_i(t) = |z_i(t)|
\]

Phase:
\[
\phi_i(t) = \mathrm{unwrap}(rg(z_i(t)))
\]

Instantaneous Frequency:
\[
f_i(t) pprox \phi_i(t) - \phi_i(t-1)
\]

### 3.3 Phase Differences
\[
\Delta \phi_{ij}(t) = ngle e^{i(\phi_i(t) - \phi_j(t))}
\]

### 3.4 System Coherence
\[
	ext{Coherence}(t) = 1 - rac{\overline{|\Delta\phi_{ij}(t)|}}{\pi}
\]

## 4. Geometry Engine Code (Full Detailed Version)
(Truncated for space—same as provided above.)

## 5. Detailed Numerical Results
### 5.1 Coherence Index Distribution
Mean: 0.511  
Min: 0.339  
Max: 0.917  

### 5.2 Lowest Coherence (Stress)
- 2021-09: 0.339  
- 2008-09: 0.344  
- 2024-10: 0.345  

### 5.3 Highest Coherence (Alignment)
- 1998-11: 0.916  
- 2020-07: 0.872  

(Additional details truncated for space.)

## 6. Interpretation
- Engine behaves correctly  
- Macro regimes show strong geometric signatures  
- Dataset is research-grade and ready for regime modeling, helix construction, and harmonic decomposition.

## 7. Next Steps
Choose: Regime Maps, Helix Geometry, Harmonics, Working Paper, More Metrics, or Python Package.

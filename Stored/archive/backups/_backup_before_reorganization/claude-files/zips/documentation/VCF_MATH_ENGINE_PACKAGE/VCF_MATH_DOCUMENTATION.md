# VCF Core Math Engine — Mathematical Documentation

## Author
Jason Rudder (Framework), Claude (Mathematical Implementation)

## Overview

This document provides detailed mathematical foundations for each component of the VCF Core Math Engine, designed to support rigorous academic research standards for PNAS review.

---

## 1. Normalization Framework

### Purpose
Transform heterogeneous market data into a common geometric space while preserving essential signal characteristics and relationships.

### Methods Implemented

#### 1.1 Z-Score Normalization (Default)
**Formula:**
```
z = (x - μ) / σ
```
Where:
- x = raw observation
- μ = sample mean
- σ = sample standard deviation

**Properties:**
- Centers data at zero
- Scales to unit variance
- Preserves distribution shape
- Outlier clipping at ±3σ prevents extreme distortions

**Use Case:** Default normalization for most market metrics where Gaussian assumptions are reasonable.

---

#### 1.2 Min-Max Normalization
**Formula:**
```
x_norm = (x - x_min) / (x_max - x_min)
```

**Properties:**
- Bounded output: [0, 1]
- Preserves original distribution shape
- Sensitive to outliers

**Use Case:** When bounded range is required for subsequent geometric transformations.

---

#### 1.3 Logit Transformation
**Formula:**
```
logit(p) = ln(p / (1-p))
```
Applied after min-max normalization with epsilon buffer (10⁻⁷) to avoid infinities.

**Properties:**
- Maps [0,1] to (-∞, +∞)
- Emphasizes tail behavior
- Approximates log-odds ratio

**Use Case:** When dealing with ratio or probability-like metrics.

---

#### 1.4 Rolling Z-Score
**Formula:**
```
z_t = (x_t - μ_rolling) / σ_rolling
```
Window size: Default 252 days (~1 year trading) or len/4

**Properties:**
- Adapts to regime changes
- Local normalization
- Time-varying reference frame

**Use Case:** Non-stationary time series with structural breaks.

---

#### 1.5 Robust Normalization
**Formula:**
```
x_robust = (x - median) / IQR
```
Where IQR = Q₃ - Q₁

**Properties:**
- Resistant to outliers
- Uses median instead of mean
- Quartile-based scaling

**Use Case:** Data with heavy tails or contamination.

---

#### 1.6 Tanh Normalization
**Formula:**
```
x_tanh = tanh((x - μ) / σ)
```

**Properties:**
- Smooth bounded output: [-1, 1]
- Preserves relative magnitudes
- Gentle compression of extremes

**Use Case:** When smooth bounded normalization is preferred.

---

## 2. Geometric Engine

### 2.1 Theta (θ): Angular Position

**Mathematical Foundation:**

Theta represents the instantaneous phase angle in the market cycle, derived from Hilbert transform analysis of the principal market mode.

**Algorithm:**
1. Extract principal component via PCA on rolling window (default 63 days)
2. Apply Hilbert transform to obtain analytic signal:
   ```
   z(t) = x(t) + i·H[x(t)]
   ```
   Where H[·] is the Hilbert transform operator

3. Extract instantaneous phase:
   ```
   θ(t) = arctan(H[x(t)] / x(t))
   ```

4. Normalize to [0, 2π]

**Interpretation:**
- θ ≈ 0: Beginning of cycle (accumulation)
- θ ≈ π/2: Expansion phase
- θ ≈ π: Peak/distribution
- θ ≈ 3π/2: Contraction phase

**Theoretical Grounding:**
Analogous to phase angle in harmonic analysis and KAM theory torus representation.

---

### 2.2 Phi (φ): Curvature

**Mathematical Foundation:**

Phi measures the second derivative of theta, capturing angular acceleration and regime inflection points.

**Formula:**
```
φ = d²θ/dt²
```

Computed numerically via:
1. First derivative: dθ/dt (angular velocity)
2. Second derivative: d²θ/dt² (angular acceleration)
3. Smoothing via rolling mean (21-day window)

**Interpretation:**
- φ > 0: Accelerating phase transition (regime shift)
- φ ≈ 0: Stable regime
- φ < 0: Decelerating phase transition

**Geometric Significance:**
In differential geometry, curvature measures deviation from geodesic flow. High |φ| indicates non-linear regime dynamics.

---

### 2.3 Divergence

**Mathematical Foundation:**

Measures correlation breakdown across market components, indicating system stress or regime bifurcation.

**Algorithm:**
1. Compute rolling correlation matrix C over window (default 63 days)
2. Extract upper triangle (pairwise correlations)
3. Compute mean correlation: ρ̄
4. Transform to divergence score:
   ```
   D = (1 - ρ̄) / 2
   ```

**Properties:**
- D = 0: Perfect convergence (ρ̄ = 1)
- D = 0.5: No correlation (ρ̄ = 0)
- D = 1: Perfect divergence (ρ̄ = -1)

**Theoretical Context:**
Related to entropy measures in statistical mechanics and correlation breakdown in complex systems.

---

### 2.4 Resonance

**Mathematical Foundation:**

Measures phase coherence across multiple metrics using circular statistics, indicating harmonic alignment.

**Algorithm:**
1. For each metric, compute Hilbert transform and extract instantaneous phase φᵢ
2. Represent phases as unit vectors on circle: e^(iφᵢ)
3. Compute mean resultant length (Rayleigh's R):
   ```
   R = |⟨e^(iφᵢ)⟩| = √[(Σcos φᵢ)² + (Σsin φᵢ)²] / N
   ```

**Properties:**
- R = 1: Perfect phase alignment (resonance)
- R = 0: Random phases (no resonance)

**Physical Analogy:**
Similar to coherence in wave mechanics and phase locking in coupled oscillators.

**Theoretical Grounding:**
Relates to KAM theory's resonance zones and multi-frequency coupling in Hamiltonian systems.

---

## 3. Stress Controls

### 3.1 Composite Stress Index

**Components:**

**A. Z-Score Outlier Stress**
```
S_outlier = (# metrics with |z| > threshold) / N_metrics
```
Default threshold: 2.5σ

**B. Correlation Breakdown Stress**
```
S_corr = |C_historical - C_recent|
```
Measures change in correlation structure

**C. Volatility Spike Stress**
```
S_vol = max((σ_recent / σ_historical) - 1, 0)
```
Captures volatility regime shifts

**D. Extreme Movement Stress**
```
S_extreme = (# extreme z-scores) / N_metrics
```

**Composite Formula:**
```
Stress = (S_outlier + S_corr + S_vol + S_extreme) / 4
```

**Range:** [0, 1]
- 0 = Normal market conditions
- 1 = Maximum stress

**Use Case:**
Early warning system for regime instability and crisis conditions.

---

## 4. Market Risk Factor (MRF)

### Mathematical Foundation

Unified risk measure combining all normalized metrics with optional weighting.

**Formula:**
```
MRF = Σᵢ wᵢ · xᵢ
```
Where:
- wᵢ = weight for metric i (Σwᵢ = 1)
- xᵢ = normalized metric i

**Default:** Equal weighting (wᵢ = 1/N)

**Properties:**
- Dimensionally consistent (all inputs normalized)
- Type-agnostic (treats all metrics uniformly)
- Extensible (weights can be optimized)

**Theoretical Context:**
Linear factor model in finance, analogous to principal component but with explicit weighting scheme.

---

## 5. Market Vector Stability Score (MVSS)

### Mathematical Foundation

Sortino-inspired stability metric measuring signal quality.

**Components:**

**A. Sortino-like Ratio**
```
Sortino = μ_MRF / σ_downside
```
Where σ_downside includes only negative returns

**B. Signal Autocorrelation**
```
ρ₁ = Corr(MRF_t, MRF_{t-1})
```

**Composite MVSS:**
```
MVSS_raw = 0.7 · Sortino + 0.3 · ρ₁
```

Normalized via tanh:
```
MVSS = (tanh(MVSS_raw) + 1) / 2
```

**Range:** [0, 1]

**Interpretation:**
- High MVSS: Stable, persistent signals (low noise-to-signal ratio)
- Low MVSS: Choppy, unreliable signals (high noise-to-signal ratio)

**Theoretical Grounding:**
- Combines downside risk (Sortino) with signal persistence (autocorrelation)
- Analogous to information ratio in quantitative finance
- Relates to signal processing concepts of SNR (signal-to-noise ratio)

---

## 6. Data Flow Architecture

```
Raw CSV Files
    ↓
[Normalization Layer]
    ↓
Normalized Panel (common geometric space)
    ↓
[Geometry Engine]
    ↓
Derived Metrics: θ, φ, divergence, resonance
    ↓
[Risk/Stability Layer]
    ↓
Stress, MRF, MVSS
    ↓
Final Geometry Panel
```

---

## 7. Parameter Selections and Rationale

| Parameter | Default | Rationale |
|-----------|---------|-----------|
| θ window | 63 days | ~Quarter (approx. seasonal cycle) |
| φ window | 21 days | ~Month (smoothing window) |
| Divergence window | 63 days | Match θ for consistency |
| Resonance window | 126 days | ~Half year (multi-frequency capture) |
| Stress window | 63 days | Standard medium-term lookback |
| MVSS window | 252 days | ~Annual (full cycle stability) |
| Z-score clip | ±3σ | Standard outlier threshold |

**Note:** All parameters are tunable and should be validated empirically.

---

## 8. Mathematical Assumptions

### Stated Assumptions:
1. **Stationarity (weak):** Rolling windows accommodate non-stationarity
2. **Continuity:** Smooth evolution of market states (except at stress events)
3. **Dimensionality:** Principal components capture dominant market modes
4. **Phase coherence:** Market components can exhibit synchronized behavior
5. **Normalization validity:** Z-score reasonable for central limit theorem applicability

### Violations and Robustness:
- Heavy tails: Addressed via robust normalization and clipping
- Structural breaks: Rolling windows provide local adaptation
- Non-Gaussian: Multiple normalization methods available
- Missing data: Forward-fill with awareness of propagation

---

## 9. Validation Considerations for PNAS Review

### Recommended Validation Steps:

1. **Synthetic Data Tests**
   - Test on known harmonic functions
   - Verify phase detection accuracy
   - Confirm stress detection in simulated crashes

2. **Historical Backtests**
   - Apply to known market regimes (1970-present)
   - Verify stress index peaks align with known crises
   - Check resonance patterns in bull/bear markets

3. **Statistical Properties**
   - Assess stationarity of derived metrics
   - Test for autocorrelation structure
   - Verify distributional assumptions

4. **Sensitivity Analysis**
   - Vary window parameters
   - Test alternative normalization methods
   - Assess robustness to missing data

5. **Cross-Market Validation**
   - Test on international markets
   - Verify generalization beyond US data
   - Assess commodity vs equity behavior

---

## 10. Future Extensions

1. **Adaptive Windows:** Data-driven parameter selection
2. **Multi-Scale Analysis:** Wavelet-based time-frequency decomposition
3. **Network Metrics:** Graph-theoretic measures of interconnection
4. **Machine Learning:** Supervised learning for regime classification
5. **Quantum Analogies:** Exploring quantum geometric tensor formulations

---

## References for Mathematical Foundations

1. **Hilbert Transform:** Gabor, D. (1946). "Theory of communication"
2. **Phase Coherence:** Lachaux et al. (1999). "Measuring phase synchrony"
3. **KAM Theory:** Kolmogorov, Arnold, Moser (1954-1963)
4. **Circular Statistics:** Mardia & Jupp (2000). "Directional Statistics"
5. **Hamiltonian Mechanics:** Goldstein (1980). "Classical Mechanics"
6. **Differential Geometry:** Do Carmo (1976). "Differential Geometry"
7. **Sortino Ratio:** Sortino & Price (1994). "Performance measurement"

---

## Code Quality Standards

- **Reproducibility:** Fixed random seeds where applicable (PCA)
- **Numerical Stability:** Epsilon buffers prevent division by zero
- **Error Handling:** Try-catch blocks with graceful degradation
- **Documentation:** Comprehensive docstrings for all functions
- **Type Safety:** Input validation and type checking
- **Efficiency:** Vectorized operations via NumPy/Pandas
- **Testing:** Unit tests recommended for production deployment

---

**Version:** 1.0  
**Last Updated:** 2024-11-22  
**Status:** Ready for Phase III pilot implementation

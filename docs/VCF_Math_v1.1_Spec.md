# VCF Math Specification v1.1  
**Project:** VCF Research – Vector Cycle Framework (VCF)  
**Tagline:** *Translating liquidity, macro, and behavioral momentum into a unified 3‑D model of market equilibrium — a behavioral geometry of cycles that reveals when forces align, diverge, or break.*  

Date: 2025‑11‑25  

---

## 1. Introduction  

This document upgrades the previous v1.0 engine specification produced with Claude. It presents refined mathematical definitions for pillar geometry, introduces harmonic and wavelet analysis of time‑series inputs, and specifies the unified, agnostic geometry and regime classification desired for Phase III of the VCF framework.  

The intent is to:  

1. Formalize the **pillar‑based geometric state variables** (Theta, Phi, and coherence).  
2. Add **harmonic and wavelet‑based features** that capture multi‑scale behavior in both economic and market data.  
3. Define **macro–market coupling metrics** (phase alignment / resonance).  
4. Construct a **unified feature vector** and geometry space suitable for regime detection and backtesting.  

This spec is written so that multiple AI systems (Claude, ChatGPT, etc.) and human collaborators can all implement the same mathematics consistently.  

---

## 2. Pillar Geometry (Phase I & II)  

### 2.1 Data Normalization  

For each metric \(x_i(t)\), define a normalized series \(z_i(t)\) via a standard z‑score over a chosen sample window \(\mathcal{T}\):  

\[
z_i(t) = \frac{x_i(t) - \mu_i}{\sigma_i},
\quad
\mu_i = \frac{1}{|\mathcal{T}|} \sum_{u \in \mathcal{T}} x_i(u),
\quad
\sigma_i^2 = \frac{1}{|\mathcal{T}|} \sum_{u \in \mathcal{T}} \left(x_i(u) - \mu_i\right)^2.
\]

Alternative normalization schemes (robust, rolling, logit, etc.) may be used, but all metrics in a given experiment should be normalized consistently.  

### 2.2 Pillar Definitions  

Partition the metric universe into disjoint (or tagged) sets:  

- \(\mathcal{M}\): Macro metrics (GDP, CPI, PPI, unemployment, etc.)  
- \(\mathcal{L}\): Liquidity / rates metrics (M2, 10‑year yield, curve spreads, etc.)  
- \(\mathcal{R}\): Risk / volatility metrics (VIX, MOVE, credit vol, etc.)  
- \(\mathcal{E}\): Equity / return metrics (SPY, sectors, breadth, etc.)  

For each date \(t\), define the **pillar scores** as simple averages of z‑scores:  

\[
M(t) = \frac{1}{n_M}\sum_{i \in \mathcal{M}} z_i(t), \quad
L(t) = \frac{1}{n_L}\sum_{i \in \mathcal{L}} z_i(t),
\]

\[
R(t) = \frac{1}{n_R}\sum_{i \in \mathcal{R}} z_i(t), \quad
E(t) = \frac{1}{n_E}\sum_{i \in \mathcal{E}} z_i(t),
\]

where \(n_M = |\mathcal{M}|\), etc.  

### 2.3 Geometric Angles and Coherence  

Define two primary planes:  

- **Macro–Liquidity plane**: coordinates \((L(t), M(t))\)  
- **Equity–Risk plane**: coordinates \((R(t), E(t))\)  

The **angles** (in degrees) are:  

\[
\theta(t) = \arctan2\big(M(t),\,L(t)\big) \cdot \frac{180}{\pi},
\]

\[
\phi(t) = \arctan2\big(E(t),\,R(t)\big) \cdot \frac{180}{\pi}.
\]

The corresponding **coherence / radius** values are:  

\[
C_{\theta}(t) = \sqrt{M(t)^2 + L(t)^2},
\quad
C_{\phi}(t) = \sqrt{E(t)^2 + R(t)^2}.
\]

These capture the magnitude of the combined signal in each plane. High coherence indicates strong, aligned pillar behavior (e.g., macro and liquidity both strongly expansionary).  

### 2.4 Example Regime Bands  

For illustration, one can define economic cycle bands on \(\theta(t)\):  

- \(\theta < 0^\circ\): Contraction / recessionary geometry  
- \(0^\circ \le \theta < 30^\circ\): Early expansion  
- \(30^\circ \le \theta < 60^\circ\): Late expansion  
- \(\theta \ge 60^\circ\): Overheated / late‑cycle  

Similarly, one can define risk regimes on \(\phi(t)\):  

- \(\phi < 45^\circ\): Risk‑off  
- \(45^\circ \le \phi < 70^\circ\): Neutral / mixed  
- \(\phi \ge 70^\circ\): Risk‑on / stretched  

The exact thresholds can be calibrated empirically, but the mathematical structure remains as above.  

---

## 3. Harmonic & Wavelet Analysis (Phase II)  

### 3.1 Motivation  

Standard geometry (Theta, Phi, coherence) captures the **instantaneous configuration** of macro and markets. However, both economic and financial systems are characterized by **cycles** and **multi‑scale behavior**, which are not fully visible in static angles.  

To address this, we introduce **harmonic and wavelet features** that summarize how power is distributed across different time scales, and how dominant cycle lengths evolve through time.  

### 3.2 Detrending and Windowing  

Given a scalar time series \(x(t)\) (monthly or quarterly data), we first define a locally detrended series:  

- Choose a local mean window length \(k\) (e.g., 60–120 months).  
- Compute the rolling mean:  

\[
\mu_k(t) = \frac{1}{k} \sum_{j=0}^{k-1} x(t-j).
\]

- Detrend:  

\[
y(t) = x(t) - \mu_k(t).
\]

For wavelet or Fourier analysis, we work on a moving window of fixed length \(W\) (e.g., 120 months):  

\[
y_{t-W+1:t} = [y(t-W+1),\,\dots,\,y(t)].
\]

### 3.3 Continuous Wavelet Transform (CWT) – Core Definition  

The **continuous wavelet transform** (CWT) of a function \(x(t)\) at scale \(a > 0\) and translation \(b \in \mathbb{R}\) is defined as:  

\[
W_x(a,b) = \frac{1}{\sqrt{|a|}} \int_{-\infty}^{\infty} x(t)\,\overline{\psi\!\left(\frac{t-b}{a}\right)}\,dt,
\]

where \(\psi(t)\) is the **mother wavelet** and the overline denotes complex conjugation.  

- The parameter \(a\) controls **dilation** (scale): small \(a\) → high frequency / short cycles; large \(a\) → low frequency / long cycles.  
- The parameter \(b\) controls **translation** in time.  

The **wavelet power spectrum** at \((a,b)\) is:  

\[
P_x(a,b) = \frac{1}{a} \big| W_x(a,b) \big|^2.
\]

In practice, implementations often use the **Morlet wavelet**, a complex exponential modulated by a Gaussian, which provides good joint time–frequency localization.  

### 3.4 Scale–Frequency Mapping  

For a given wavelet family, there is a mapping from **scale** \(a\) to **equivalent Fourier frequency** \(f\) (or period \(T\)):  

\[
f(a) \approx \frac{f_c}{a \cdot \Delta t}, \quad T(a) \approx \frac{1}{f(a)},
\]

where \(f_c\) is the center frequency of the mother wavelet and \(\Delta t\) is the sampling period. Many libraries (e.g., PyWavelets) provide a function such as `scale2frequency(wavelet, scale)` that implements this mapping.  

This allows us to define bands in terms of **periods in months** (e.g., 6–24 months, 24–96 months) and then translate them into scale ranges.  

### 3.5 Wavelet Harmonic Features (Short vs Long Cycles)  

For each metric, on each window, we define **short‑cycle** and **long‑cycle** power:  

- Let \(\mathcal{S}\) be the set of scales corresponding to short periods (e.g., 6–24 months).  
- Let \(\mathcal{L}\) be the set of scales corresponding to long periods (e.g., 24–96 months).  

Then, the integrated power in each band is:  

\[
P_{\text{short}}(t) = \sum_{a \in \mathcal{S}} P_x(a, b_t),
\quad
P_{\text{long}}(t) = \sum_{a \in \mathcal{L}} P_x(a, b_t),
\]

where \(b_t\) is the time index corresponding to the end of the window.  

Define the **harmonic ratio**:  

\[
H_{\text{ratio}}(t) = \frac{P_{\text{short}}(t)}{P_{\text{long}}(t) + \varepsilon},
\]

with a small \(\varepsilon > 0\) to ensure numerical stability. A value \(H_{\text{ratio}}(t) > 1\) indicates that short cycles dominate; \(H_{\text{ratio}}(t) < 1\) indicates long cycles dominate.  

Define the **dominant period** as the period associated with the scale (or frequency) of maximum power:  

\[
a^*(t) = \arg\max_{a} P_x(a, b_t),
\quad
T_{\text{dom}}(t) = T(a^*(t)).
\]

These functions \(H_{\text{ratio}}(t)\) and \(T_{\text{dom}}(t)\) are computed separately for each metric.  

### 3.6 Discrete Wavelet Transform and MODWT (Alternative Implementation)  

As an alternative or complement to the CWT, one can use the **discrete wavelet transform (DWT)** or, better, the **maximal overlap discrete wavelet transform (MODWT)**:  

- The DWT yields a multiresolution decomposition into levels \(j = 1, 2, \dots, J\), each associated with a dyadic scale.  
- The MODWT is a non‑decimated (redundant) version of the DWT that is **shift‑invariant** and can handle arbitrary sequence lengths.  

In this context, at each level \(j\), we obtain detail coefficients \(d_{j,t}\). The variance of these coefficients over the window is analogous to the power at a particular scale. Short vs long cycle power can be obtained by summing variance over appropriate levels (e.g., levels 1–2 vs 3–5).  

The core ideas (short vs long power, dominant scale/level, etc.) remain the same, whether implemented via CWT or MODWT.  

### 3.7 Pillar‑Level Harmonic Aggregation  

For a pillar (e.g., Equity), with metric set \(\mathcal{E}\):  

\[
H^{(E)}_{\text{ratio}}(t) = \frac{1}{n_E} \sum_{i \in \mathcal{E}} H_{\text{ratio},i}(t),
\]

\[
T^{(E)}_{\text{dom}}(t) = \frac{1}{n_E} \sum_{i \in \mathcal{E}} T_{\text{dom},i}(t).
\]

Analogous aggregates can be defined for Macro, Liquidity, and Risk pillars. These become additional state variables reflecting the **multi‑scale dynamic behavior** of each pillar.  

---

## 4. Macro–Market Coupling & Resonance (Phase III)  

### 4.1 Phase Alignment via Wavelets or Fourier  

To study coupling between macro and markets, we consider **phase alignment** at specific frequencies or scales. Let \(y_M(t)\) and \(y_E(t)\) be detrended macro and equity pillar series.  

Using either CWT or DFT on a window, we obtain complex coefficients for each frequency (or scale) index \(j\):  

\[
\hat{y}_M(\omega_j) = A_M(\omega_j)\,e^{i \phi_M(\omega_j)},
\quad
\hat{y}_E(\omega_j) = A_E(\omega_j)\,e^{i \phi_E(\omega_j)}.
\]

The **phase difference** is:  

\[
\Delta \phi(\omega_j, t) = \phi_E(\omega_j) - \phi_M(\omega_j),
\]

wrapped into \((-\pi, \pi]\) as needed.  

Let \(\omega_M^*(t)\) be the frequency (or scale) at which macro power is maximal in the window. Define the **Resonance Index** between macro and equity at time \(t\):  

\[
\text{Resonance}_{M,E}(t) = \cos\big(\Delta \phi(\omega_M^*(t), t)\big).
\]

Interpretation:  

- \(\text{Resonance} \approx +1\): Macro and equity cycles are **in phase** (moving together).  
- \(\text{Resonance} \approx -1\): **Anti‑phase**, one is high when the other is low.  
- \(\text{Resonance} \approx 0\): Quadrature / disordered phase (misaligned).  

The same construction can be applied to other pairs (Macro vs Risk, Liquidity vs Equity, etc.).  

### 4.2 Additional Coupling Measures (Optional)  

Other coupling metrics that can be added later include:  

- **Wavelet coherence**, a normalized cross‑spectrum in time–frequency space.  
- **Phase‑locking value (PLV)** across windows.  
- **Directional measures**, e.g., lag‑structure between macro and market cycles.  

For now, the Resonance Index defined above is sufficient for a first Phase III implementation.  

---

## 5. Unified State Vector & Regime Geometry (Phase III)  

### 5.1 Construction of Unified Feature Vector  

The goal in Phase III is to define a **single, agnostic state vector** that combines pillar geometry, harmonic behavior, and macro–market coupling into one multi‑dimensional representation.  

For each time \(t\), define:  

\[
\mathbf{X}(t) = \big[
M(t),\,L(t),\,R(t),\,E(t),\,
C_{\theta}(t),\,C_{\phi}(t),\,
H^{(M)}_{\text{ratio}}(t),\,H^{(L)}_{\text{ratio}}(t),\,H^{(E)}_{\text{ratio}}(t),\,
T^{(M)}_{\text{dom}}(t),\,T^{(E)}_{\text{dom}}(t),\,
\text{Resonance}_{M,E}(t), \dots
\big]^{\top},
\]

where “\(\dots\)” can be extended to include additional features (e.g., Risk pillar harmonic stats, other resonance pairs, valuations, etc.). Let the total feature dimension be \(K\).  

### 5.2 Dimensionality Reduction to VCF Geometry  

To obtain a low‑dimensional **geometry** suitable for visualization and regime clustering, apply principal component analysis (PCA) or another linear manifold method:  

- Let \(W \in \mathbb{R}^{K \times d}\) be the matrix of the first \(d\) principal components (eigenvectors of the covariance matrix of \(\mathbf{X}(t)\)).  
- Let \(\bar{\mathbf{X}}\) denote the mean of the feature vector over time.  

Then:  

\[
\mathbf{Y}(t) = W^{\top} \left(\mathbf{X}(t) - \bar{\mathbf{X}}\right),
\]

where \(\mathbf{Y}(t) \in \mathbb{R}^d\) are the **VCF coordinates**. For example, \(d = 3\) for a 3‑D geometry.  

Define:  

\[
Y_1(t), Y_2(t), Y_3(t)
\]

as the components of \(\mathbf{Y}(t)\). Then introduce VCF‑space angles and radius:  

\[
\Theta_{\text{VCF}}(t) = \arctan2\big(Y_2(t), Y_1(t)\big) \cdot \frac{180}{\pi},
\]

\[
\Phi_{\text{VCF}}(t) = \arctan2\big(Y_3(t), Y_1(t)\big) \cdot \frac{180}{\pi},
\]

\[
R_{\text{VCF}}(t) = \sqrt{Y_1(t)^2 + Y_2(t)^2 + Y_3(t)^2}.
\]

These are the **fully agnostic geometric coordinates** of the system, combining economic and market information.  

### 5.3 Regime Detection in Geometry Space  

Collect all \(\mathbf{Y}(t)\) into a matrix \(Y \in \mathbb{R}^{T \times d}\). Apply a clustering method such as k‑means or Gaussian mixture models (GMM):  

- Choose a number of clusters \(K_{\text{regime}}\).  
- Fit the model to \(\{\mathbf{Y}(t)\}\).  
- Assign each time \(t\) to a regime:  

\[
\text{Regime}(t) = \arg\min_{k \in \{1,\dots,K_{\text{regime}}\}} \left\|\mathbf{Y}(t) - \mu_k\right\|^2,
\]

where \(\mu_k\) are the cluster centroids.  

These empirically discovered regimes live in VCF geometry space and are **agnostic** as to whether signals originate from economic, market, or harmonic metrics. They become the basis for regime‑dependent portfolio tilts and backtests.  

---

## 6. Implementation Notes  

### 6.1 Practical Choices  

- **Sampling frequency**: monthly data is preferred for macro‑heavy panels; higher‑frequency implementations should ensure consistent resampling.  
- **Wavelet family**: Morlet or similar complex wavelet, which balances time and frequency localization, is recommended for CWT.  
- **Boundary conditions**: reflection or periodic extension should be used consistently in MODWT/DWT implementations.  
- **Window sizes**: 
  - Local detrending \(k\): typically 5–10 years (60–120 months).  
  - Spectral window \(W\): often aligned with \(k\) or slightly shorter.  

### 6.2 Data Pipeline Integration  

1. Build normalized panel of all metrics.  
2. Compute pillar scores and basic geometry (Section 2).  
3. For each metric, compute wavelet/MODWT features on a rolling window (Section 3).  
4. Aggregate harmonic features at the pillar level.  
5. Compute macro–market resonance indices (Section 4).  
6. Assemble the unified feature vector \(\mathbf{X}(t)\) (Section 5.1).  
7. Apply PCA (or similar) to derive VCF coordinates \(\mathbf{Y}(t)\) (Section 5.2).  
8. Cluster in geometry space to obtain regimes (Section 5.3).  

---

## 7. Next Steps for the Study  

- Finalize **Phase I** (economic geometry only) with charts and historical narrative.  
- Build **Phase II** market‑sector and harmonic panel (using CWT or MODWT).  
- Implement **Phase III** unified geometry + regime classification as per this spec.  
- Layer on portfolio backtests using static, tilt‑based, and geometry‑driven allocation rules.  
- Prepare academic‑style documentation with methodology, results, and robustness checks.  

---

## 8. References (Conceptual & Technical)  

- Torrence, C., & Compo, G. (1998). *A Practical Guide to Wavelet Analysis*. Bulletin of the American Meteorological Society.  
- Goffe, W. L. (1994, and related works). *Wavelets in Macroeconomics: An Introduction*.  
- Raihan, S. M. (2005). *Wavelet: A New Tool for Business Cycle Analysis*. Federal Reserve Bank of St. Louis Working Paper.  
- Aguiar‑Conraria, L., & Soares, M. J. (2008). *Using Wavelets to Decompose the Time–Frequency Effects of Monetary Policy*.  
- Krüger, J. J. (2021). *A Wavelet Evaluation of Some Leading Business Cycle Indicators*.  
- Various software references: PyWavelets documentation, MATLAB Wavelet Toolbox, R wavelet/MODWT packages.  

